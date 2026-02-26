import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials
# Importamos tu scraper real
from darpe_scraper import obtener_producto_aleatorio_total

st.set_page_config(page_title="DarpePro Publicador", page_icon="⚡")
st.title("⚡ Publicador DarpePro")

def conectar_google_sheets():
    ruta_json = "credenciales.json"
    
    # 1. Intentar cargar desde el archivo físico (Streamlit)
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r') as f:
                datos = json.load(f)
        except Exception as e:
            st.error(f"Error al leer el JSON: {e}")
            return None
    # 2. Intentar cargar desde Secretos de GitHub (Para el bot automático)
    elif os.getenv("GOOGLE_CREDENTIALS"):
        datos = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    else:
        st.error("❌ No se encontraron credenciales (ni archivo ni Secret).")
        return None

    try:
        # ARREGLO CRÍTICO: Forzar que los \n sean saltos de línea reales
        # Esto soluciona el 'Invalid JWT Signature' definitivamente
        if "private_key" in datos:
            datos["private_key"] = datos["private_key"].replace("\\n", "\n")
        
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(datos, scopes=scope)
        client = gspread.authorize(creds)
        
        return client.open("Hoja de DarpePro").sheet1
    except Exception as e:
        st.error(f"❌ Error de firma o conexión: {str(e)}")
        return None

# --- INTERFAZ ---
st.write("Haz clic para que el bot busque un producto real y lo mande a publicar.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Buscando producto en la tienda y conectando con Google..."):
        # Llamamos a tu scraper para obtener un producto real
        producto = obtener_producto_aleatorio_total()
        
        if producto:
            hoja = conectar_google_sheets()
            if hoja:
                try:
                    # Usamos los datos reales obtenidos del scraper
                    nueva_fila = [producto['nombre'], producto['url'], producto['imagen_url'], "Pendiente"]
                    hoja.append_row(nueva_fila)
                    st.success(f"✅ ¡Éxito! '{producto['nombre']}' enviado a la hoja.")
                    st.image(producto['imagen_url'], width=200)
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error al escribir en la hoja: {e}")
        else:
            st.error("❌ No se pudo extraer ningún producto de la web. Revisa el scraper.")
