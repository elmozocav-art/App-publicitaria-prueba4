import os
import json
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="DarpePro Bot Control", page_icon="🚀")
st.title("🚀 Panel de Control DarpePro")

def inicializar_google_sheets():
    # 1. Intentar extraer de Secrets de Streamlit o de Variables de Entorno
    secret_data = st.secrets.get('GOOGLE_CREDENTIALS') or os.environ.get('GOOGLE_CREDENTIALS')
    
    if not secret_data:
        st.error("❌ No se encontró el Secret GOOGLE_CREDENTIALS")
        return None

    info = json.loads(secret_data)
    creds = Credentials.from_service_account_info(info)
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = gspread.authorize(creds.with_scopes(scope))
    
    return client.open("Hoja de DarpePro").sheet1

def subir_producto_manual(nombre, url):
    try:
        hoja = inicializar_google_sheets()
        if hoja:
            # Añadir la fila con estado "Pendiente"
            # Tu bot de Make leerá esta fila automáticamente
            nueva_fila = [nombre, url, "", "Pendiente"]
            hoja.append_row(nueva_fila)
            return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False

# --- INTERFAZ VISUAL (Streamlit) ---
st.subheader("Publicación Manual de Productos")
st.write("Completa los datos para añadir un producto a la cola de publicación de Instagram.")

with st.form("formulario_producto"):
    nombre_input = st.text_input("Nombre del Producto", placeholder="Ej: Trolley Corbin")
    url_input = st.text_input("URL del Producto", placeholder="https://darpepro.com/...")
    
    boton_enviar = st.form_submit_button("Añadir a la lista")

    if boton_enviar:
        if nombre_input and url_input:
            with st.spinner("Subiendo a Google Sheets..."):
                exito = subir_producto_manual(nombre_input, url_input)
                if exito:
                    st.success(f"✅ ¡Producto '{nombre_input}' añadido! El bot lo publicará en breve.")
        else:
            st.warning("⚠️ Por favor, rellena ambos campos.")

# --- SECCIÓN DE ESTADO (Opcional) ---
if st.checkbox("Verificar conexión con Google Sheets"):
    hoja = inicializar_google_sheets()
    if hoja:
        st.write("✅ Conexión establecida con: *Hoja de DarpePro*")
