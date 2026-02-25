import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="DarpePro One-Click", page_icon="⚡")

def inicializar_google_sheets():
    try:
        # PANTILLA DIRECTA: Pegamos tus datos aquí para evitar errores de Secrets
        info = {
          "type": "service_account",
          "project_id": "automatizacion-darpepro",
          "private_key_id": "7dec218613311a522ef8a09e4602ca15e804a4f7",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDm4VNtSULgqEJJWTFleXuqbpcPlQlEFKCcuhmMZK7kOpBeLVG0j9ZxxM1VA+DDnBJ2TZjCvdnmd2/RQIwWETlVvqthrlhhXPrw6O6xz+2kmpC/Po3qcXTV2Vyz4B45tRxrnBg0pWqJOfsuLUytSn5UCJdTtNcUxsv4yMwP6TRsJMvdIJT5l51uq7zFat7faEupeZow8JSqD2b16N3MgoXYOecdnCDyPtBOjSqOOTTlcWhF5yd1dCShbg6KPeEmQ412cGTTnb8Q0iFlS2oLtLhx8ohJUXrGhpQVNxALSfauOACZC5PbBvp7y3AdBEqk7pWhc/a42BRhX48A+i5dDlMVAgMBAAECggEACYylqA4xAfHJAWz6/2N4RfhaWdP5lM31nAXmgJ65d8nO/CuLsZgxb8s1YvV3b8pzc7PfRE7DRdEILZ4p18/RO0auTVVUunzfXuTY2pSVvl/WP31q3pjgEuhGo/n6cLtDov/LJdehrG4FgZzGCx+Fp3F424bN+UIFCxPjEiq8dwHf0AVBm/vryLziUe1RhWhmU5PCqJQT7T5qCmYQiVtr2D6lDU2nWch7R3oKLhYA/yaWdp6whgmEQ5YPSmGiGEA+qLrvOX8pIIZk3k5MJDNuKzTHSEG71iVcW5wfaDceS/QbcemkUxvrFN1WGYe25X29thzi2pbRdFR758UVQQtSEQKBgQD+sdCW1oe+fGwjbmYbrJfvPPU2PB+Fj09lcadPHpsCzoW7N11yv/Lcmxl65Fkw31EFFtK7Aqrc9XE7l99Xs2pF1OezrTRkStGpn2/iuu3uFoLjE3s2lwg9rPfkJ5m06OY2ZPUTizv/M9fVM2SGiHwsCd2JP4faC9Eb2CV/XDjHcwKBgQDoEEOf1HfHVirpKTePsM5/Tnn6x3pgc45VjlHm4SigSI5Ft+bZ0Zqt0Ww56hP7emRb5GzGqoDIgxhhkzXx6X+Zo+bi2T9tMBLYyvkkGsva+1S2/lXRGppu/w5oDF/u4Cpu2FBXEG5ZBOvlUFTNUMU3/hhJwvIo6VUBzjMHU2KJVwKBgDHqT2MAcGIYqGjZPhG2ZaBxZe1XIyZdy8Wp3IxZBzApoXPridjvXX12uCupjQFTAuHocyxLfYkIYUS4owDhHLbK3w4Lp/Tv5N9Fa/wXfoHmz4gJTWCJgQf1Wi/QwwL9kgCfEJjf9MYzNt2F0PG81fkbhdtcJBfLsROv7MllHYuZAoGAfsmUCNjucCw12Zm5T3pL9+YKYudlhxjbZQcS3E+cAKZjhNfK+qq4Fctbk/C95iGif0o32/r/zY1CXt0tFfR60Jhp5vrG2oLvaR7MK9uwEP5L9IbUoCAmzAnx9wr7xukWheUNT+QcReqYb3sKOfqtJcBfyL0HzS5eUVQ1MQVvypUCgYEAmMNB+xZp8Vrwj4ZkHuyQV5NdVLRaGIRfmIyDm8YG9t4A1CR6Ezs4ZB+2kPSkoZFuZcU9iRKXn2F9jIknuW49zqt2VLtGBPj3UGwB+Tc4Q+k/Ytcz6bZXn8BIvBG15fNXpMFN6lekdvgZHV2wWvHJbIJFZOVb0MhDqKNtJ2e2J+E=\n-----END PRIVATE KEY-----\n",
          "client_email": "bot-darpepro@automatizacion-darpepro.iam.gserviceaccount.com",
          "client_id": "104849416098488477184",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-darpepro%40automatizacion-darpepro.iam.gserviceaccount.com",
          "universe_domain": "googleapis.com"
        }

        # Limpiamos la clave por si acaso
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        
        # Autenticación directa
        creds = Credentials.from_service_account_info(info)
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        client = gspread.authorize(creds.with_scopes(scope))
        
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
            nueva_fila = [nombre_producto, url_producto, "", "Pendiente"]
            hoja.append_row(nueva_fila)
            return nombre_producto
        except Exception as e:
            st.error(f"❌ Error al escribir: {e}")
    return None

# --- INTERFAZ ---
st.title("⚡ Publicador DarpePro")
st.write("Pulsa el botón y olvida los errores de configuración.")

if st.button('🚀 ¡PUBLICAR SIGUIENTE PRODUCTO AHORA!', use_container_width=True):
    with st.spinner("Conectando directamente..."):
        producto = ejecutar_bot_manual()
        if producto:
            st.success(f"✅ ¡Hecho! '{producto}' enviado.")
            st.balloons()
