import streamlit as st
import pandas as pd

def show_bar_chart(animal_names, predictions):
    data = pd.DataFrame({
        "Animal": animal_names,
        "Probability": predictions
    })

    st.bar_chart(data.set_index("Animal"), color="#215B63")