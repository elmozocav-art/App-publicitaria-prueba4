import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="DarpePro Publicador", page_icon="⚡")
st.title("⚡ Publicador DarpePro")

def conectar_google_sheets():
    ruta_json = "credenciales.json"
    
    if not os.path.exists(ruta_json):
        st.error("❌ No se encuentra el archivo credenciales.json en el repositorio.")
        return None

    try:
        # 1. Leer el archivo JSON
        with open(ruta_json, 'r') as f:
            datos = json.load(f)
        
        # 2. LIMPIEZA FORZADA DE LA LLAVE (Para evitar el error de Firma JWT)
        # Reemplazamos los saltos de línea literales por reales
        if "private_key" in datos:
            datos["private_key"] = datos["private_key"].replace("\\n", "\n")
        
        # 3. Autenticación
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(datos, scopes=scope)
        client = gspread.authorize(creds)
        
        # 4. Abrir la hoja
        return client.open("Hoja de DarpePro").sheet1
    except Exception as e:
        st.error(f"❌ Error crítico de Google: {str(e)}")
        return None

# --- INTERFAZ ---
st.write("Pulsa el botón para enviar un producto a la hoja de cálculo.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Validando firma y conectando..."):
        hoja = conectar_google_sheets()
        if hoja:
            try:
                # Datos de prueba para verificar conexión
                nueva_fila = ["Set Malcon", "https://darpepro.com/set-malcon/", "", "Pendiente"]
                hoja.append_row(nueva_fila)
                st.success("✅ ¡CONECTADO! El producto se guardó en la hoja.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error al escribir: {e}")
