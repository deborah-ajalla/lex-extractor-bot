import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import google.generativeai as genai
import os
from dotenv import load_dotenv
#-----------------------------------------------------
#PARA EJECUTAR: EN CONSOLA --> streamlit run app_v4.py
#-----------------------------------------------------

# Carga las variables ocultas del archivo .env
load_dotenv()
#----------------------------------------------
# --> NOMBRE DE PESTAÑA
st.set_page_config(page_title='APP ANALIZA SENTENCIAS JUDICIALES', initial_sidebar_state="collapsed") # PARA ICONO:  img=imagen.png -> ,page_icon= "img" 
#----------------------------------------------
# --> IMAGEN BANNER
img = Image.open ("banner.jpg")

# Primero redimensiono  imagen con PIL
img_redimensionada = img.resize((700, 350))

# Muestro la imagen
st.image(img_redimensionada)

#st.image(img, width=700, heigth= 400)
#----------------------------------------------
# --> TITULO PPAL
st.markdown("<h1 style='text-align: center;font-size: 36px;'>⚖️ Analizador de Sentencias Judiciales ⚖️</h1>", unsafe_allow_html=True)
#st.title("⚖️ Analizador de Sentencias Judiciales ⚖️")

#st.write("Sube tu fallo en formato PDF para analizar automáticamente los autos, la resolución, la doctrina y más.")
st.markdown("<p style='text-align: center; font-size: 20px;'>Subí tu fallo en formato PDF para analizar automáticamente <br> los autos, la resolución, la doctrina y más.</p>", unsafe_allow_html=True)
#----------------------------------------------
# --> BARRA LATERAL
st.sidebar.header ("Opciones")
#----------------------------------------------
# Lee la ruta de Tesseract desde el .env
ruta_tesseract = os.getenv("TESSERACT_PATH")
if ruta_tesseract:
    pytesseract.pytesseract.tesseract_cmd = ruta_tesseract
#----------------------------------------------
# --> 1. SECCIÓN DE LECTURA DEL PDF 
archivo_pdf = st.file_uploader("Cargar documento PDF", type="pdf")
texto_extraido = ""

if archivo_pdf is not None:
    st.info("Procesando documento ... ⌛")
    documento = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
    barra_progreso = st.progress(0)
    total_paginas = len(documento)

    for i, pagina in enumerate(documento):
        pix = pagina.get_pixmap(dpi=300)
        imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        texto_pagina = pytesseract.image_to_string(imagen, lang='spa')
        texto_extraido += texto_pagina + "\n"
        barra_progreso.progress((i + 1) / total_paginas)

    st.success("¡Documento leído exitosamente!")

    with st.expander("Ver texto extraído"):
        st.write(texto_extraido)

# 2. SECCIÓN DE IA
st.divider()
st.subheader("🧠 Análisis Jurídico")

if st.button("Generar Análisis Jurídico", type="primary"): #--> ➡️⚙️cambiar color ❌
    # Lee la API Key directamente del entorno de forma segura
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key: #--> ⚙️verificar funcionamiento ❌
        st.error("⚠️ No se encontró la API Key en el archivo .env")
    elif not texto_extraido:
        st.warning("⚠️ Primero debes procesar un documento PDF arriba.")
    else:
        try:
            genai.configure(api_key=api_key)
            modelo = genai.GenerativeModel('gemini-2.5-flash') #--> ⚙️verificar modelo ❌
            
            instruccion = f"""
            Eres un abogado experto y analista de jurisprudencia. Tu tarea es leer el siguiente texto extraído de una sentencia judicial y estructurar su análisis. Debes ser objetivo, preciso y utilizar terminología jurídica correcta. Devuelve la información estructurada con los siguientes títulos exactos: 
            - Autos
            - Motivo del Juicio
            - Temas Principales
            - Artículos Controvertidos
            - Resolución
            - Doctrina

            Si un dato no está presente en el texto, indica 'No especificado en el documento'. 

            Documento a analizar:
            {texto_extraido}
            """
            
            with st.spinner("Analizando la sentencia, extrayendo doctrina y resolución..."):
                respuesta = modelo.generate_content(instruccion) #--> ⚙️verificar funcionamiento ❌
                
            st.success("¡Análisis completado!")
            st.markdown(respuesta.text)
            
        except Exception as e:
            st.error(f"Hubo un error al conectar con la IA: {e}")