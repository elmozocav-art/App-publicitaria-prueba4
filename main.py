def inicializar_google_sheets():
    secret_data = st.secrets.get('GOOGLE_CREDENTIALS')
    if not secret_data:
        st.error("❌ No se encontraron las credenciales en los Secrets.")
        return None

    info = json.loads(secret_data)
    
    # ESTA LÍNEA ES LA CLAVE: Corrige los saltos de línea de la clave privada
    info["private_key"] = info["private_key"].replace("\\n", "\n")
    
    creds = Credentials.from_service_account_info(info)
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = gspread.authorize(creds.with_scopes(scope))
    return client.open("Hoja de DarpePro").sheet1
