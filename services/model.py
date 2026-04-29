from keras.models import load_model
import streamlit as st

@st.cache_resource
def get_model():
    return load_model("./models/modelo_cnn_entrenado.h5")

def predict(model, img_array):
    return model.predict(img_array)[0]