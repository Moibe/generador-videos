import os
from io import BytesIO
from typing import List
import funciones.motion as motion
import tempfile
from fastapi import FastAPI, Form
from fastapi import FastAPI, File, UploadFile, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import herramientas

app = FastAPI()

@app.get("/health",
         tags=["Monitoreo Server"],
         description="Verifica el estado de salud de la API.",
         summary="Health Check"
         )
async def health_check():
    """
    Este endpoint devuelve una respuesta 200 OK para indicar que la API está funcionando.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/echo-image/",
          tags=["Monitoreo Server"],
          description="Test endpoint para prueba de envío de imagenes.",
          summary="Mirror test para envío de imagenes"
          )
async def echo_image(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        return {"error": "El archivo no es una imagen"}
    contents = await image.read()
    return StreamingResponse(BytesIO(contents), media_type=image.content_type)

@app.post("/motion-image/")
async def motion_image(image: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Recibe una imagen, la procesa con motion(), le da movimiento y devuelve el resultado.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo no es una imagen. Por favor, suba una imagen."
        )

    temp_image_path = None # Inicializamos la variable para el bloque finally
    output_file_generated = False # Flag para saber si monomotion generó un archivo

    try:
        # 1. Guardar la imagen subida en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{image.filename}") as tmp_file:
            contents = await image.read()
            tmp_file.write(contents)
            temp_image_path = tmp_file.name
        
        print(f"Imagen subida guardada temporalmente en: {temp_image_path}")

        # 2. Ejecutar motion()
        # Asumimos que motion devuelve la ruta a un archivo de salida
        path_archivo = await motion.motion(temp_image_path)
        print("Salí de monomotion con resultado: ", path_archivo)
        output_file_generated = True # Si llegamos aquí, asumimos que se generó un archivo

        # 3. Determinar el tipo MIME del archivo de salida (si es diferente al de entrada)
        # Esto es importante si motion cambia el formato (ej. de JPG a MP4)
        import mimetypes
        mimetypes.add_type("video/mp4", ".mp4") # Asegúrate de añadir tipos si esperas video
        mime_type, _ = mimetypes.guess_type(path_archivo)
        if not mime_type:
             mime_type = "application/octet-stream" # Tipo genérico si no se puede adivinar

        # 4.5 Programar la eliminación de AMBOS archivos después de que la respuesta sea enviada
        # El archivo de entrada se borrará sí o sí.
        background_tasks.add_task(herramientas.delete_file_on_complete, temp_image_path)
        # El archivo de salida también se borrará, asumiendo que es temporal y solo para esta respuesta.
        background_tasks.add_task(herramientas.delete_file_on_complete, path_archivo)

        # 4. Devolver el archivo procesado al cliente
        return FileResponse(
            path=path_archivo,
            media_type=mime_type,
            filename=os.path.basename(path_archivo)
        )

    except HTTPException:
        # Re-lanza cualquier HTTPException ya creada (ej. el 400 inicial)
        raise
    except Exception as e:
        # Captura cualquier otro error inesperado durante el proceso
        print(f"Error inesperado en /generate-monomotion-image/: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ha ocurrido un error interno al procesar la imagen con monomotion: {e}"
        )
    finally:
        # 5. Limpieza: Eliminar archivos temporales
        # Eliminar la imagen de entrada temporal
        if temp_image_path and os.path.exists(temp_image_path):
            try:
                os.remove(temp_image_path)
                print(f"Archivo temporal de entrada eliminado: {temp_image_path}")
            except Exception as cleanup_e:
                print(f"Error al eliminar el archivo temporal de entrada {temp_image_path}: {cleanup_e}")

@app.post("/echo-random-file/")
async def echo_random_file(files: List[UploadFile] = File(...)):
    """
    Recibe múltiples archivos, selecciona uno al azar y lo devuelve.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron archivos."
        )
    
    temp_file_paths = [] # Lista para guardar las rutas de los archivos temporales
    try:
        # 1. Guardar cada UploadFile en un archivo temporal en disco
        for uploaded_file in files:
            # Creamos un archivo temporal con un sufijo para mantener la extensión
            # delete=False para que no se elimine inmediatamente al cerrar el archivo.
            # Lo eliminaremos explícitamente en el bloque finally.
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.filename}") as tmp_file:
                contents = await uploaded_file.read()
                tmp_file.write(contents)
                current_temp_path = tmp_file.name
                temp_file_paths.append(current_temp_path)
                print(f"Guardado temporalmente: {current_temp_path}")
        
        # 2. Pasar la lista de rutas de archivos temporales a tu función 'cinema'
        # ¡Ahora 'lista_rutas_archivos' es la "lista" que tu función cinema espera!
        resultado_cinema = await motion.cinema(temp_file_paths)

        # 3. Manejar el resultado de la función 'cinema'
        if isinstance(resultado_cinema, str):
            # Si cinema devuelve una ruta a un archivo (ej. un video generado)
            # Determinar el tipo MIME del archivo de salida
            import mimetypes
            mime_type, _ = mimetypes.guess_type(resultado_cinema)
            if not mime_type:
                 mime_type = "application/octet-stream" # Tipo genérico si no se puede adivinar

            # Devolver el archivo generado por cinema
            # Asegúrate de que este archivo también se gestione y elimine si es temporal
            return FileResponse(
                path=resultado_cinema,
                media_type=mime_type,
                filename=os.path.basename(resultado_cinema)
            )
        elif isinstance(resultado_cinema, dict) and "error" in resultado_cinema:
            # Si cinema devuelve un diccionario de error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en la función cinema: {resultado_cinema['error']}"
            )
        else:
            # Si cinema devuelve otra cosa (ej. un JSON de éxito sin archivo)
            return resultado_cinema # Asume que es un diccionario JSON serializable

    except HTTPException:
        # Re-lanza cualquier HTTPException que ya se haya levantado (ej. por validación de entrada)
        raise
    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error inesperado en /process-files-with-cinema/: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ha ocurrido un error interno al procesar los archivos con cinema: {e}"
        )
    finally:
        # 4. Limpiar los archivos temporales creados
        for path in temp_file_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"Archivo temporal eliminado: {path}")
                except Exception as cleanup_e:
                    print(f"Error al eliminar el archivo temporal {path}: {cleanup_e}")   