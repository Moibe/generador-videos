import os

def lista_archivos(directorio):
    nombres_archivos = []  # Inicializamos una lista vacía para guardar los nombres

    try:
        # Verificar si la carpeta existe
        if os.path.exists(directorio) and os.path.isdir(directorio):
            # Listar todos los elementos dentro de la carpeta
            elementos = os.listdir(directorio)

            print(f"Archivos encontrados en la carpeta '{directorio}':")
            for elemento in elementos:
                ruta_completa = os.path.join(directorio, elemento)
                # Verificar si el elemento es un archivo
                if os.path.isfile(ruta_completa):
                    nombres_archivos.append(elemento)  # Añadir el nombre del archivo a la lista
                    print(elemento)  # Opcional: imprimir el nombre mientras se guarda

            print("\nLista de nombres de archivos guardada en la variable 'nombres_archivos'.")
            # Ahora la variable 'nombres_archivos' contiene todos los nombres de los archivos
            # que puedes usar en el resto de tu código.
            # Ejemplo de cómo podrías acceder a los nombres:
            # for nombre in nombres_archivos:
            #     print(f"Procesando archivo: {nombre}")

            return nombres_archivos

        else:
            print(f"La carpeta '{directorio}' no existe o no es un directorio.")
            nombres_archivos = []  # Asegurarse de que la lista esté vacía en caso de error
            return nombres_archivos

    except Exception as e:
        print(f"Ocurrió un error al acceder a la carpeta: {e}")
        nombres_archivos = []  # Asegurarse de que la lista esté vacía en caso de error
        return nombres_archivos