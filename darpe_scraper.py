import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    url_base = "https://darpepro.com/tienda/"
    # Le ponemos cabeceras para que tu web se crea que es un navegador Chrome real, no un bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    }

    try:
        response = requests.get(url_base, headers=headers, timeout=20)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        
        # MODO DESTRUCTOR: Buscar todas las etiquetas 'a' (enlaces) que contengan una imagen
        enlaces_con_imagen = soup.find_all("a", href=True)
        candidatos = []
        
        for enlace in enlaces_con_imagen:
            img = enlace.find("img")
            # Si el enlace tiene una imagen dentro, es muy probable que sea un producto
            if img:
                url_destino = enlace["href"]
                # Filtramos para que no coja el logo de la web, sino cosas de la tienda
                if "producto" in url_destino or "tienda" in url_destino or "darpepro.com" in url_destino:
                    
                    # Intentamos sacar la imagen (incluso si está oculta por lazy-loading)
                    url_imagen = img.get("data-src") or img.get("src") or img.get("data-lazy-src") or ""
                    
                    # Intentamos sacar el nombre (del texto alternativo de la imagen o del título)
                    nombre = img.get("alt") or enlace.get_text(strip=True)
                    
                    # Si no hay nombre, buscamos el texto del contenedor
                    if not nombre or len(nombre) < 3:
                        padre = enlace.parent
                        if padre:
                            nombre = padre.get_text(strip=True)
                    
                    if not nombre:
                        nombre = "Producto DarpePro"

                    # Solo lo añadimos si la imagen es una URL válida
                    if url_imagen.startswith("http"):
                        candidatos.append({
                            "nombre": nombre[:70].strip(), # Cortamos el nombre si es un texto larguísimo
                            "url": url_destino,
                            "imagen_url": url_imagen
                        })

        if candidatos:
            # Elegimos uno al azar de todos los que ha pescado
            return random.choice(candidatos)
            
        # PLAN DE EMERGENCIA EXTREMO: Si no encuentra productos, coge la primera imagen que vea
        # Hacemos esto para que al menos veas que el Excel se rellena y Streamlit funciona
        imagenes_sueltas = soup.find_all("img", src=True)
        if imagenes_sueltas:
            for img in imagenes_sueltas:
                if img["src"].startswith("http"):
                    return {
                        "nombre": "Prueba de Conexión (Scraper Genérico)",
                        "url": url_base,
                        "imagen_url": img["src"]
                    }

    except Exception as e:
        print(f"Error en Scraper: {e}")
        
    return None
