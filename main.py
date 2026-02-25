import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="DarpePro One-Click", page_icon="⚡")

def inicializar_google_sheets():
    try:
        # 1. Obtener secretos de Streamlit
        secret_data = st.secrets.get('GOOGLE_CREDENTIALS')
        if not secret_data:
            st.error("❌ No se encontraron las credenciales en Secrets.")
            return None

        # 2. Cargar JSON y limpiar la clave para evitar 'Invalid JWT Signature'
        info = json.loads(secret_data)
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace("\\n", "\n")
        
        # 3. Autenticación
        creds = Credentials.from_service_account_info(info)
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        client = gspread.authorize(creds.with_scopes(scope))
        
        # 4. Abrir la hoja
        return client.open("Hoja de DarpePro").sheet1
    
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def ejecutar_bot_manual():
    hoja = inicializar_google_sheets()
    if hoja:
        try:
            nombre_producto = "Set Malcon" 
            url_producto = "https://darpepro.com/set-malcon/"
            
            # Añadir fila con estado Pendiente para Make.com
            nueva_fila = [nombre_producto, url_producto, "", "Pendiente"]
            hoja.append_row(nueva_fila)
            return nombre_producto
        except Exception as e:
            st.error(f"❌ Error al escribir en la hoja: {e}")
    return None

# --- INTERFAZ VISUAL ---
st.title("⚡ Publicador Automático DarpePro")
st.write("Haz clic en el botón para enviar el producto a Instagram.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Conectando..."):
        producto = ejecutar_bot_manual()
        if producto:
            st.success(f"✅ ¡Éxito! '{producto}' enviado correctamente.")
            st.balloons()

# --- PANEL DE CONTROL (Corregido para evitar SyntaxError) ---
with st.expander("⚙️ Configuración y Estado"):
    st.write("Verifica la conexión con Google Sheets abajo:")
    if st.button("Probar Conexión"):
        test = inicializar_google_sheets()
        if test:
            st.success("✅ Conexión establecida correctamente.")
