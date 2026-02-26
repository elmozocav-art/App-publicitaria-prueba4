import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials
# IMPORTANTE: Asegúrate de que el archivo en GitHub se llame darpe_scraper.py
from darpe_scraper import obtener_producto_aleatorio_total

st.set_page_config(page_title="DarpePro Publicador", page_icon="⚡")
st.title("⚡ Publicador DarpePro")

def conectar_hoja():
    try:
        # Prioridad a Secrets de Streamlit (la caja de texto que pegamos)
        if "GOOGLE_CREDENTIALS" in st.secrets:
            datos = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        elif os.path.exists("credenciales.json"):
            with open("credenciales.json", 'r') as f:
                datos = json.load(f)
        else:
            st.error("❌ No se encuentran credenciales.")
            return None

        # Reparación de la llave privada (JWT Signature fix)
        if "private_key" in datos:
            datos["private_key"] = datos["private_key"].replace("\\n", "\n")
        
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(datos, scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Hoja de DarpePro").sheet1
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

# --- BOTÓN PRINCIPAL ---
# Ahora 'st' ya está definido arriba y no dará error
if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Buscando producto real en darpepro.com..."):
        producto = obtener_producto_aleatorio_total()
        
        if producto:
            st.info(f"📦 Producto detectado: {producto['nombre']}")
            hoja = conectar_hoja()
            if hoja:
                try:
                    nueva_fila = [producto['nombre'], producto['url'], producto['imagen_url'], "Pendiente"]
                    hoja.append_row(nueva_fila)
                    st.success(f"✅ ¡Añadido a la hoja con éxito!")
                    st.image(producto['imagen_url'], width=200)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al escribir en Google Sheets: {e}")
        else:
            st.error("❌ El Scraper no devolvió datos. Revisa que el archivo se llame darpe_scraper.py")
