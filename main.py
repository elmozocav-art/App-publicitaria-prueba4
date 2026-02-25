import os
import json
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="DarpePro One-Click", page_icon="⚡")
st.title("⚡ Publicador Automático DarpePro")

def inicializar_google_sheets():
    # Carga de credenciales desde Secrets de Streamlit
    secret_data = st.secrets.get('GOOGLE_CREDENTIALS')
    if not secret_data:
        st.error("❌ No se encontraron las credenciales en Secrets.")
        return None

    info = json.loads(secret_data)
    creds = Credentials.from_service_account_info(info)
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = gspread.authorize(creds.with_scopes(scope))
    return client.open("Hoja de DarpePro").sheet1

def ejecutar_bot_automatico():
    try:
        hoja = inicializar_google_sheets()
        if hoja:
            # --- AQUÍ VA TU LÓGICA DE BÚSQUEDA AUTOMÁTICA ---
            # El bot busca el producto (puedes usar tu scraper o datos fijos)
            nombre_producto = "Set Malcon" 
            url_producto = "https://darpepro.com/set-malcon/"
            
            nueva_fila = [nombre_producto, url_producto, "", "Pendiente"]
            hoja.append_row(nueva_fila)
            return nombre_producto
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# --- INTERFAZ DE UN SOLO BOTÓN ---
st.write("Haz clic abajo para que el bot busque el siguiente producto y lo publique en Instagram.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("El bot está trabajando..."):
        producto = ejecutar_bot_automatico()
        if producto:
            st.success(f"✅ ¡Éxito! El producto '{producto}' ha sido enviado a Make.com.")
            st.balloons()
