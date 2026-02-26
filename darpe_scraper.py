import requests
from bs4 import BeautifulSoup
import random


def obtener_producto_aleatorio_total():

    url_base = "https://darpepro.com/tienda/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url_base, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        enlaces = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/producto/" in href or "/product/" in href:
                enlaces.append(href)

        enlaces = list(set(enlaces))

        if not enlaces:
            return None

        url_producto = random.choice(enlaces)

        response_producto = requests.get(url_producto, headers=headers, timeout=10)
        soup_producto = BeautifulSoup(response_producto.content, "html.parser")

        titulo = soup_producto.find("h1")
        nombre = titulo.get_text(strip=True) if titulo else None

        img = soup_producto.find("img")
        imagen = img["src"] if img and img.get("src") else None

        if not nombre or len(nombre) < 3:
            return None

        return {
            "nombre": nombre,
            "url": url_producto,
            "imagen_url": imagen
        }

    except Exception as e:
        print("Error scraper:", e)
        return None
