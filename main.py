import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="DarpePro Publicador", page_icon="⚡")
st.title("⚡ Publicador DarpePro")

def conectar_google_sheets():
    try:
        # Cargamos el archivo que acabas de subir a GitHub
        ruta_json = "credenciales.json"
        
        if not os.path.exists(ruta_json):
            st.error("❌ No se encuentra el archivo credenciales.json en el repositorio.")
            return None

        # Autenticación usando el archivo físico para evitar errores de firma
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(ruta_json, scopes=scope)
        client = gspread.authorize(creds)
        
        # Intentamos abrir la hoja
        return client.open("Hoja de DarpePro").sheet1
    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")
        return None

# Botón de acción
st.write("Haz clic para enviar el producto a la cola de publicación.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Conectando con Google Sheets..."):
        hoja = conectar_google_sheets()
        if hoja:
            try:
                # Datos de prueba
                nueva_fila = ["Set Malcon", "https://darpepro.com/set-malcon/", "", "Pendiente"]
                hoja.append_row(nueva_fila)
                st.success("✅ ¡Éxito! Producto añadido a la hoja.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error al escribir en la hoja: {e}")
