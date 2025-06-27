from googleapiclient.discovery import build
import bridges
import time

# --- Configura tus credenciales y ID de Motor de Búsqueda ---
API_KEY = bridges.google_api  # Reemplaza con tu Clave de API de Google Cloud
CX = "90556d12415d84063" # Reemplaza con el ID de tu Custom Search Engine

def buscar_imagenes_google(query, num_results=5):
    """
    Realiza una búsqueda de imágenes en Google usando la Custom Search API.

    Args:
        query (str): El término de búsqueda.
        num_results (int): El número máximo de resultados a devolver (máx. 10 por solicitud).

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa una imagen
              y contiene su URL, título, etc.
    """
    try:
        # Construye el servicio de la API de Custom Search
        # 'customsearch' es el nombre del servicio, 'v1' es la versión
        service = build("customsearch", "v1", developerKey=API_KEY)

        # Ejecuta la búsqueda.
        # 'q': el término de búsqueda
        # 'cx': el ID de tu Custom Search Engine
        # 'searchType': MUY IMPORTANTE, para especificar que buscas imágenes
        # 'num': número de resultados (máx. 10 por solicitud, aunque puedes paginar)
        res = service.cse().list(
            q=query,
            cx=CX,
            searchType='image',
            num=num_results
        ).execute()

        print("Esto es res:")
        print(res)
        time.sleep(18)

        # Extrae los resultados
        items = res.get('items', [])
        
        resultados_imagenes = []
        for item in items:
            resultados_imagenes.append({
                'title': item.get('title'),
                'link': item.get('link'),  # URL directa de la imagen
                'displayLink': item.get('displayLink'), # URL del sitio donde se encontró
                'thumbnailLink': item['image'].get('thumbnailLink') if 'image' in item else None # URL de la miniatura
            })
        
        return resultados_imagenes

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

# --- Ejemplo de uso ---
if __name__ == "__main__":
    termino_busqueda = "Mexico Day of the Dead"
    imagenes_encontradas = buscar_imagenes_google(termino_busqueda, num_results=3)

    if imagenes_encontradas:
        print(f"Imágenes encontradas para '{termino_busqueda}':")
        for i, imagen in enumerate(imagenes_encontradas):
            print(f"--- Imagen {i+1} ---")
            print(f"Título: {imagen.get('title')}")
            print(f"URL: {imagen.get('link')}")
            print(f"URL Miniatura: {imagen.get('thumbnailLink')}")
            print("-" * 20)
    else:
        print("No se encontraron imágenes o hubo un error.")