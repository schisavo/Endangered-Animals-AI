import os
from keras.models import load_model
import streamlit as st

MODELS_DIR = "./models"

@st.cache_resource
def get_model():
    files = [
        f for f in os.listdir(MODELS_DIR)
        if f.endswith(".keras") or f.endswith(".h5")
    ]

    if not files:
        raise FileNotFoundError("No hay modelos en la carpeta models/")

    latest_model = max(
        files,
        key=lambda f: os.path.getctime(os.path.join(MODELS_DIR, f))
    )

    model_path = os.path.join(MODELS_DIR, latest_model)
    print(f"📦 Cargando modelo: {model_path}")

    return load_model(model_path)


def predict(model, img_array):
    return model.predict(img_array)[0]