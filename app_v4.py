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

st.title("⚖️ Analizador de Sentencias Judiciales ⚖️")
st.write("Sube tu fallo en formato PDF para analizar automáticamente los autos, la resolución, la doctrina y más.")

# Lee la ruta de Tesseract desde el .env
ruta_tesseract = os.getenv("TESSERACT_PATH")
if ruta_tesseract:
    pytesseract.pytesseract.tesseract_cmd = ruta_tesseract

# 1. SECCIÓN DE LECTURA DEL PDF 
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