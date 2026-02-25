import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    """
    Entra en la web de DarpePro, busca productos reales 
    y devuelve un diccionario con la información.
    """
    url_base = "https://darpepro.com/tienda/" # Ajusta esta URL a tu sección de catálogo
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url_base, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Buscamos los contenedores de productos (ajusta el selector según tu web)
        # Comúnmente en WooCommerce es 'li.product' o 'div.product'
        productos = soup.select("li.product") 

        if not productos:
            # Intento alternativo de selector si el primero falla
            productos = soup.find_all("div", class_="product-grid-item")

        if productos:
            # Elegimos uno al azar para asegurar variedad
            p = random.choice(productos)
            
            # Extraer Nombre
            nombre = p.select_one(".woocommerce-loop-product__title").text.strip()
            
            # Extraer Enlace
            enlace = p.select_one("a")["href"]
            
            # Extraer Imagen (buscando el atributo src o data-src para evitar imágenes vacías)
            img_tag = p.select_one("img")
            imagen = img_tag.get("data-src") or img_tag.get("src")

            # VALIDACIÓN CRÍTICA: 
            # Si el nombre es genérico o muy corto, devolvemos None para que el main.py reintente
            if "Destacado" in nombre or len(nombre) < 3:
                return None

            return {
                "nombre": nombre,
                "url": enlace,
                "imagen_url": imagen
            }
            
    except Exception as e:
        print(f"Error en el scraper: {e}")
        return None

    return None