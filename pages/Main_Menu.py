import numpy as np
import streamlit as st
from PIL import Image

from state.session import init_session
from services.model import get_model, predict
from services.img_preprocessing import preprocess_image

from ui.components.bar_char import show_bar_chart
from ui.components.confidence import show_confidence
from ui.components.confidence_trend import show_confidence_trend


animal_names = [
    "African Elephant", "Amur Leopard", "Arctic Fox", "Cheetahs", "Chimpanzee", 
    "Jaguars", "Lion", "Orangutan", "Panda", "Panthers", "Rhino"
]

# ---------------- INIT ----------------
model = get_model()
init_session(animal_names)

# ---------------- HEADER ----------------
st.title("🌿 Endangered is :green[Animals] Evaluation")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2, 3])

# -------- LEFT PANEL --------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("AI Image Clasification Model", divider="green")
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)

    st.markdown("""
    Analyze an image of the 11 threatened species and identify 
    which class it belongs to with 78% accuracy.
        🐘 🐆 🐒 🦁 🦧 🐼  🦏  
    """)

    uploaded_file = st.file_uploader(
        "Upload an image of an animal",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)

        if st.button("Evaluate"):
            try:
                img_array = preprocess_image(image)
                preds = predict(model, img_array)

                st.session_state.predictions = preds

                if "history_full" not in st.session_state:
                    st.session_state.history_full = []

                st.session_state.history_full.append(preds)

                label = np.argmax(preds)
                animal = animal_names[label]

                st.success(f"Predicted: {animal}")

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- RIGHT PANEL --------
with col2:

    top1, top2 = st.columns([3, 1])

    # ---- Bar Chart ----
    with top1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Probabilities", divider="green")
        st.subheader("Class Probability", divider="green")

        show_bar_chart(animal_names, st.session_state.predictions)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Confidence ----
    with top2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        show_confidence(st.session_state.predictions)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Trend ----
    st.markdown('<div class="card">', unsafe_allow_html=True)

    show_confidence_trend(
        st.session_state.history_full,
        animal_names
    )

    st.markdown('</div>', unsafe_allow_html=True)