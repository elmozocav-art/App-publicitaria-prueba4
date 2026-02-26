import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    url_base = "https://darpepro.com/tienda/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url_base, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Error: La web respondió con código {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Buscamos los productos (WooCommerce usa li.product)
        productos = soup.select("li.product") or soup.select(".product")

        if not productos:
            print("No se encontraron productos en la página.")
            return None

        # Elegimos uno al azar
        p = random.choice(productos)
        
        # Extraemos los datos con selectores seguros
        tag_nombre = p.select_one(".woocommerce-loop-product__title") or p.find("h2")
        nombre = tag_nombre.get_text(strip=True) if tag_nombre else "Producto DarpePro"
        
        tag_a = p.find("a")
        enlace = tag_a["href"] if tag_a else "https://darpepro.com/tienda/"
        
        tag_img = p.find("img")
        imagen = ""
        if tag_img:
            imagen = tag_img.get("data-src") or tag_img.get("src") or ""

        return {
            "nombre": nombre,
            "url": enlace,
            "imagen_url": imagen
        }
            
    except Exception as e:
        print(f"Error en el scraper: {e}")
        return None
