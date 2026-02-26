import streamlit as st
from scraper_bot import ejecutar_bot

st.set_page_config(page_title="DarpePro Bot", page_icon="📦")

st.title("📦 DarpePro Bot Manual")

if st.button("Ejecutar ahora"):
    ejecutar_bot()
    st.success("Producto enviado a Google Sheets")
