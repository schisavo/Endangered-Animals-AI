import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from keras.models import load_model

animal_names = [
    "African Elephant", "Amur Leopard", "Arctic Fox", "Cheetahs", "Chimpanzee", 
    "Jaguars", "Lion", "Orangutan", "Panda", "Panthers", "Rhino"
]

# ---------------- MODEL CACHE ----------------
@st.cache_resource
def load_ai_model():
    return load_model("./models/modelo_cnn_entrenado.h5")

model = load_ai_model()

# ---------------- SESSION STATE ----------------
if "predictions" not in st.session_state:
    st.session_state.predictions = np.zeros(len(animal_names))

if "history_full" not in st.session_state:
    st.session_state.history_full = []
if "history" not in st.session_state:
    st.session_state.history = []

def show_prediction_img():
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
            # st.image(image, caption="Uploaded Image", use_column_width=True)
            st.image(image, caption="Uploaded Image", width=400)
            
            # Boton para evaluar la imagen 
            if st.button("Evaluate"):
                try:
                    # Preprocesamiento
                    img       = image.resize((128,128))
                    img_array = np.array(img) /255.0

                    if img_array.shape[-1] != 3:
                        img_array = np.stack((img_array,)*3, axis=1)

                    img_array = np.expand_dims(img_array, axis=0)
                    # Prediccion
                    preds     = model.predict(img_array)[0]

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

            data = pd.DataFrame({
                "Animal": animal_names,
                "Probability": st.session_state.predictions
            })

            st.bar_chart(data.set_index("Animal"))

            st.markdown('</div>', unsafe_allow_html=True)

        # ---- Confidence Rate ----
        with top2:
            max_prob = float(np.max(st.session_state.predictions))

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown("Confidence")
            
            st.progress(max_prob)
            st.metric("Top Score", f"{max_prob*100:.2f}%")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---- Prediction Confidence Trend ----
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### Animal Probability Trends")
        df = pd.DataFrame(st.session_state.history_full, columns=animal_names)
        st.line_chart(df)

        st.markdown('</div>', unsafe_allow_html=True)