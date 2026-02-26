import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from darpe_scraper import obtener_producto_aleatorio_total


def conectar_google_sheets():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)

    hoja = client.open("Automatización DarpePro").sheet1
    return hoja


def ejecutar_bot():

    hoja = conectar_google_sheets()

    producto = obtener_producto_aleatorio_total()

    if producto:
        datos = [
            producto['nombre'],
            producto['url'],
            producto['imagen_url'],
            "Pendiente",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        hoja.append_row(datos)
        print("Producto enviado:", producto['nombre'])
    else:
        print("No se pudo obtener producto.")


if __name__ == "__main__":
    ejecutar_bot()
