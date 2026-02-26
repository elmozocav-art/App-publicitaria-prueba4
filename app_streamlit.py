import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials
from darpe_scraper import obtener_producto_aleatorio_total

def conectar_google():
    # 1. Si estamos en Streamlit Cloud (usando Secrets)
    if "GOOGLE_CREDENTIALS" in st.secrets:
        datos = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        # IMPORTANTE: Esto arregla el error de la llave que mencionabas
        datos["private_key"] = datos["private_key"].replace("\\n", "\n")
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(datos, scopes=scope)
        return gspread.authorize(creds)
    
    # 2. Si estamos en Eclipse (usando el archivo local)
    elif os.path.exists("credenciales.json"):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file("credenciales.json", scopes=scope)
        return gspread.authorize(creds)
    
    return None

# --- USO DEL BOTÓN ---
st.title("⚡ Publicador DarpePro")

if st.button('🚀 PUBLICAR AHORA'):
    cliente = conectar_google()
    if cliente:
        hoja = cliente.open("Automatización DarpePro").sheet1
        producto = obtener_producto_aleatorio_total() # Asegúrate que el archivo se llame darpe_scraper.py
        
        if producto:
            hoja.append_row([producto['nombre'], producto['url'], producto['imagen_url'], "Pendiente"])
            st.success(f"✅ ¡Publicado: {producto['nombre']}!")
        else:
            st.error("❌ El Scraper no encontró productos. Revisa el nombre del archivo en GitHub.")

