import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

from services.model import get_model, predict
from state.session import init_session
from services.img_preprocessing import preprocess_image

from .components.bar_char import show_bar_chart
from .components.confidence import show_confidence
from .components.confidence_trend import show_confidence_trend

animal_names = [
    "African Elephant", "Amur Leopard", "Arctic Fox", "Cheetahs", "Chimpanzee", 
    "Jaguars", "Lion", "Orangutan", "Panda", "Panthers", "Rhino"
]





def show_Prediction():
    # Cache Model AI
    model = get_model()

    # Session States
    init_session(animal_names)

    # ---------------- HEADER ----------------
    st.title("Endangered Animals Evaluation")
    # ---------------- LAYOUT ----------------
    col1, col2 = st.columns([2, 3])
    # -------- LEFT PANEL (AI Model) --------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("AI Image Clasification Model")
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
        st.markdown("""
        Analyze an image of the 11 threatened species and identify 
        which class it belongs to with 78% accuracy.
        """)

        # Configura la imagen a subir
        uploaded_file = st.file_uploader("Upload an image of an animal", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            # Ventana de la imagen
            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Image", width=400)
            
            # Boton para evaluar la imagen 
            if st.button("Evaluate"):
                try:
                    # Preprocesar imagen para el modelo
                    img_array = preprocess_image(image)
                    # Prediccion
                    preds = predict(model,img_array)

                    # Guardar Session state
                    st.session_state.predictions = preds
                    # ---------------- MODEL PREDICTION HISTORY CACHE ----------------
                    if "history_full" not in st.session_state:
                        st.session_state.history_full = []

                    st.session_state.history_full.append(preds)

                    label   = np.argmax(preds)
                    animal  = animal_names[label]

                    st.success(f"Predicted: {animal}")
                
                except Exception as e:
                    st.error(f"Error: {e}")


        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------------


    # -------- RIGHT PANEL --------
    with col2:

        top1, top2 = st.columns([3, 1])

        # ---- Total Sales ----
        with top1:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown('<div class="title">Total Sale</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric">90,744</div>', unsafe_allow_html=True)

            show_bar_chart(animal_names, st.session_state.predictions)

            st.markdown('</div>', unsafe_allow_html=True)

        # ---- Confidence Rate ----
        with top2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            show_confidence(st.session_state.predictions)

            st.markdown('</div>', unsafe_allow_html=True)

        # ---- Prediction Confidence Trend ----
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        show_confidence_trend(st.session_state.history_full,
                                animal_names)
        
        st.markdown('</div>', unsafe_allow_html=True)