import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="DarpePro One-Click", page_icon="⚡")

def inicializar_google_sheets():
    try:
        # 1. Intentar obtener secretos
        secret_data = st.secrets.get('GOOGLE_CREDENTIALS')
        if not secret_data:
            st.error("❌ No se encontraron las credenciales en 'Advanced settings > Secrets'.")
            return None

        # 2. Cargar y limpiar la clave
        info = json.loads(secret_data)
        if "private_key" in info:
            # Reemplazo doble para asegurar que la firma sea válida
            info["private_key"] = info["private_key"].replace("\\n", "\n")
        
        # 3. Autenticación
        creds = Credentials.from_service_account_info(info)
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        client = gspread.authorize(creds.with_scopes(scope))
        
        # 4. Abrir hoja
        return client.open("Hoja de DarpePro").sheet1
    
    except Exception as e:
        st.error(f"❌ Error crítico de conexión: {e}")
        return None

def ejecutar_bot_manual():
    hoja = inicializar_google_sheets()
    if hoja:
        try:
            # Datos del producto a publicar
            nombre_producto = "Set Malcon" 
            url_producto = "https://darpepro.com/set-malcon/"
            
            # Añadir fila para que Make.com la procese
            nueva_fila = [nombre_producto, url_producto, "", "Pendiente"]
            hoja.append_row(nueva_fila)
            return nombre_producto
        except Exception as e:
            st.error(f"❌ Error al escribir en la hoja: {e}")
    return None

# --- INTERFAZ VISUAL ---
st.title("⚡ Publicador Automático DarpePro")
st.write("Haz clic en el botón para enviar el producto a Instagram.")

# Botón principal
if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Conectando con Google Sheets y Make.com..."):
        producto = ejecutar_bot_manual()
        if producto:
            st.success(f"✅ ¡Éxito! '{producto}' añadido a la cola.")
            st.balloons()

# --- PANEL DE CONTROL ---
with st.expander("
