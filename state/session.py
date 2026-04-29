import streamlit as st
import numpy as np

def init_session(animal_names):
    if "predictions" not in st.session_state:
        st.session_state.predictions = np.zeros(len(animal_names))
    
    if "history_full" not in st.session_state:
        st.session_state.history_full = []

