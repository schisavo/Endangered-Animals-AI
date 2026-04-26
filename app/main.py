import streamlit as st
import numpy as np
import pandas as pd
from ui.prediction import show_Prediction
from ui.species_view import show_Species_Dataset
from ui.wildlife_view import show_World_Wildlife_Dataset

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ERP Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
    <style>
        body {
            background-color: #0b0f2a;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .card {
            background: linear-gradient(145deg, #111633, #0b0f2a);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
        }
        .title {
            font-size: 20px;
            font-weight: 600;
        }
        .metric {
            font-size: 28px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
# Menu vertical de la izquierda 
st.sidebar.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)

# Menu vertical opciones
with st.sidebar:
    st.title("⚡ ERP")
    st.markdown("---")
    st.markdown("## Navigation")
    
    #Opciones para cambiar el contenido
    page = st.radio("", ["Main Menu", "Graphics Species","Graphics World Wildlife"]
                    ,label_visibility="collapsed")
    st.markdown("---")

    # Botones adicionales (opcionales, no navegación principal)
    st.button("Analytics")
    st.button("Search")
    st.button("Calendar")
    st.button("Settings")

# ---------------- ROUTING ----------------
if page == "Main Menu":
    show_Prediction()
elif page == "Graphics Species":
    show_Species_Dataset()
elif page == "Graphics World Wildlife":
    show_World_Wildlife_Dataset()

