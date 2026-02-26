import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials
# Importamos tu scraper (asegúrate que el archivo se llame darpe_scraper.py)
from darpe_scraper import obtener_producto_aleatorio_total

st.set_page_config(page_title="DarpePro Publicador", page_icon="⚡")
st.title("⚡ Publicador DarpePro")

def conectar_hoja():
    try:
        # 1. Intentar leer desde Secrets (Streamlit Cloud)
        if "GOOGLE_CREDENTIALS" in st.secrets:
            datos = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        # 2. Intentar leer desde archivo local (GitHub / Local)
        elif os.path.exists("credenciales.json"):
            with open("credenciales.json", 'r') as f:
                datos = json.load(f)
        else:
            st.error("❌ No se encuentran las credenciales en ningún sitio.")
            return None

        # REPARACIÓN DE LLAVE: Esto elimina el error 'Invalid JWT Signature'
        if "private_key" in datos:
            # Reemplaza la representación de texto '\\n' por saltos de línea reales
            datos["private_key"] = datos["private_key"].replace("\\n", "\n")
        
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(datos, scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Hoja de DarpePro").sheet1
        
    except Exception as e:
        st.error(f"❌ Error de autenticación: {e}")
        return None

# --- BOTÓN PRINCIPAL ---
if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Buscando producto real y conectando..."):
        # Usamos tu scraper real
        producto = obtener_producto_aleatorio_total()
        
        if producto:
            hoja = conectar_hoja()
            if hoja:
                try:
                    nueva_fila = [producto['nombre'], producto['url'], producto['imagen_url'], "Pendiente"]
                    hoja.append_row(nueva_fila)
                    st.success(f"✅ ¡Publicado! '{producto['nombre']}' añadido a la hoja.")
                    st.image(producto['imagen_url'], width=200)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al escribir: {e}")
        else:
            st.error("No se pudo obtener información del producto.")
