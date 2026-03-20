import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carga las variables ocultas del archivo .env
load_dotenv()

st.title("⚖️ Analizador de Sentencias Judiciales")
st.write("Sube tu fallo en formato PDF para analizar automáticamente los autos, la resolución, la doctrina y más.")