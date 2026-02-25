import os
import json
import gspread
import requests
from google.oauth2.service_account import Credentials

def inicializar_google_sheets():
    # 1. Extraer la llave de los Secrets de GitHub
    secret_data = os.environ.get('GOOGLE_CREDENTIALS')
    if not secret_data:
        raise ValueError("No se encontró el Secret GOOGLE_CREDENTIALS")

    # 2. Configurar permisos
    info = json.loads(secret_data)
    creds = Credentials.from_service_account_info(info)
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = gspread.authorize(creds.with_scopes(scope))
    
    # 3. Abrir la hoja por su nombre exacto
    return client.open("Hoja de DarpePro").sheet1

def buscar_y_subir_productos():
    try:
        hoja = inicializar_google_sheets()
        
        # --- AQUÍ VA TU LÓGICA DE BÚSQUEDA ---
        # Como ejemplo, subiremos el producto que fallaba antes
        nombre_producto = "Set Malcon"
        url_producto = "https://darpepro.com/set-malcon/"
        # -------------------------------------

        # Añadir la fila con estado "Pendiente"
        # Columnas: A:Nombre, B:URL_Producto, C:URL_Imagen, D:Status
        nueva_fila = [nombre_producto, url_producto, "", "Pendiente"]
        hoja.append_row(nueva_fila)
        
        print(f"✅ Producto '{nombre_producto}' subido con éxito a Google Sheets.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    buscar_y_subir_productos()
