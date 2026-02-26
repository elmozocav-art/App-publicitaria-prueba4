# --- BOTÓN PRINCIPAL ---
if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Buscando producto real en darpepro.com..."):
        # Esto llama al archivo que acabas de renombrar
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
            # Ahora sabremos si el fallo es que no encuentra productos
            st.error("❌ El Scraper no pudo leer la tienda. Revisa que el archivo se llame darpe_scraper.py")
