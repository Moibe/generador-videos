import subprocess
import herramientas
import os

def remux_video(input_path, output_path):
    """Re-muxea un archivo de video MP4."""
    ffmpeg_command_remux = [
        'ffmpeg',
        '-i', input_path,
        '-c', 'copy',
        '-movflags', '+faststart',
        output_path
    ]
    try:
        subprocess.run(ffmpeg_command_remux, check=True, capture_output=True)
        print(f"Re-muxing exitoso de: {input_path} a {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al re-muxear {input_path}: {e}")
        print(f"Salida de error de FFmpeg:\n{e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"Ocurrió un error durante el re-muxing: {e}")
        return False
    
def unirVideos():

    directorio_videos = 'resultados'
    lista_nombres_archivos = herramientas.lista_archivos(directorio_videos)
    archivos_remuxeados = []
    lista_archivo_temporal = 'lista_concat.txt'

    try:
        with open(lista_archivo_temporal, 'w') as f_lista:
            for nombre_archivo in lista_nombres_archivos:
                ruta_completa = os.path.join(directorio_videos, nombre_archivo)
                nombre_base, extension = os.path.splitext(nombre_archivo)
                ruta_temporal = os.path.join(directorio_videos, f"temp_{nombre_base}{extension}")
                if remux_video(ruta_completa, ruta_temporal):
                    archivos_remuxeados.append(ruta_temporal)
                    f_lista.write(f"file '{ruta_temporal}'\n")
                else:
                    print("Error al re-muxear un archivo. Abortando la creación de la lista.")
                    archivos_remuxeados = []
                    break
    except FileNotFoundError as e:
        print(f"Error al abrir o crear el archivo de lista temporal: {e}")
        archivos_remuxeados = []
    except Exception as e:
        print(f"Ocurrió un error al escribir en el archivo de lista temporal: {e}")
        archivos_remuxeados = []

    if archivos_remuxeados:
        ffmpeg_command_concat = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', lista_archivo_temporal,
            '-an',
            '-c', 'copy',
            'video_unido_sin_audio.mp4'
        ]

        try:
            subprocess.run(ffmpeg_command_concat, check=True, capture_output=True)
            print("Los videos se han unido exitosamente (usando archivo de lista y archivos remuxeados).")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar FFmpeg para concatenar (archivo de lista): {e}")
            print(f"Salida de error de FFmpeg:\n{e.stderr.decode()}")
        except Exception as e:
            print(f"Ocurrió un error durante la concatenación (archivo de lista): {e}")
        finally:
            # Limpiar los archivos temporales y el archivo de lista
            for archivo_temporal in archivos_remuxeados:
                try:
                    os.remove(archivo_temporal)
                    print(f"Archivo temporal eliminado: {archivo_temporal}")
                except OSError as e:
                    print(f"Error al eliminar el archivo temporal {archivo_temporal}: {e}")
            try:
                os.remove(lista_archivo_temporal)
                print(f"Archivo de lista eliminado: {lista_archivo_temporal}")
            except OSError as e:
                print(f"Error al eliminar el archivo de lista {lista_archivo_temporal}: {e}")
    else:
        print("No se pudieron re-muxear los archivos o hubo un error al crear la lista, no se intentó la concatenación.")
