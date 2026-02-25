import streamlit as st
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from darpe_scraper import obtener_producto_aleatorio_total

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
# El archivo 'credenciales.json' debe estar en la misma carpeta
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Escribe aquí el nombre EXACTO de tu hoja de Google
NOMBRE_HOJA = "Automatización DarpePro"

try:
    hoja = client.open(NOMBRE_HOJA).sheet1
except Exception as e:
    st.error(f"❌ No se pudo abrir la hoja. Revisa el nombre o si compartiste el email del bot: {e}")
    st.stop()

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="DarpePro Feed Bot", page_icon="📦")
st.title("📦 Alimentador de Productos DarpePro")
st.write("Este bot busca productos reales y los envía a Google Sheets para que Make los publique.")

# Estado del bot
if "ejecutando" not in st.session_state:
    st.session_state.ejecutando = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Iniciar Ciclo (20h)"):
        st.session_state.ejecutando = True
with col2:
    if st.button("🛑 Detener Bot"):
        st.session_state.ejecutando = False

# --- BUCLE PRINCIPAL ---
if st.session_state.ejecutando:
    while st.session_state.ejecutando:
        with st.status("🔍 Buscando producto en la web...", expanded=True) as status:
            # Extraer info real del producto
            producto = obtener_producto_aleatorio_total()
            
            # Validación: Evitamos nombres genéricos como "Producto Destacado"
            if producto and "Destacado" not in producto['nombre']:
                # Datos para enviar: [Nombre, URL Producto, URL Imagen, Status]
                datos_fila = [
                    producto['nombre'], 
                    producto['url'], 
                    producto['imagen_url'], 
                    "Pendiente"
                ]
                
                # Insertar en la primera fila vacía
                hoja.append_row(datos_fila)
                
                st.success(f"✅ Producto enviado: **{producto['nombre']}**")
                status.update(label="✅ Datos guardados en la Hoja", state="complete")
            else:
                st.warning("⚠️ Se detectó un nombre genérico o vacío. Reintentando en breve...")
            
            # Cálculo de la próxima ejecución
            proxima_hora = datetime.now().replace(hour=(datetime.now().hour + 20) % 24).strftime("%H:%M:%S")
            st.info(f"⏳ Esperando 20 horas. Próximo envío aproximado: {proxima_hora}")
            
        # Pausa de 20 horas (72.000 segundos)
        time.sleep(72000)
        st.rerun()