import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    url_base = "https://darpepro.com/tienda/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url_base, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Error de red: Código {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Selectores más flexibles (li.product es el estándar de WooCommerce)
        productos = soup.select("li.product") or soup.select(".product") or soup.select(".type-product")

        if not productos:
            print("No se encontraron productos con los selectores actuales.")
            return None

        # Intentar hasta 5 veces si un producto sale vacío
        for _ in range(5):
            p = random.choice(productos)
            
            # Buscamos el nombre en varios posibles tags (h2, h3 o la clase de WC)
            tag_nombre = p.select_one(".woocommerce-loop-product__title") or p.select_one("h2") or p.select_one("h3")
            nombre = tag_nombre.text.strip() if tag_nombre else "Producto sin nombre"
            
            # Enlace
            tag_a = p.select_one("a")
            enlace = tag_a["href"] if tag_a and tag_a.has_attr("href") else None
            
            # Imagen (buscando todas las fuentes posibles)
            img_tag = p.select_one("img")
            imagen = ""
            if img_tag:
                imagen = img_tag.get("data-src") or img_tag.get("src") or img_tag.get("srcset", "").split(" ")[0]

            # Si tenemos lo básico, lo devolvemos
            if enlace and len(nombre) > 2:
                return {
                    "nombre": nombre,
                    "url": enlace,
                    "imagen_url": imagen
                }
            
    except Exception as e:
        print(f"Error en el scraper: {e}")
    
    return None
