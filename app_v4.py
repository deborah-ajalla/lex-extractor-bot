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