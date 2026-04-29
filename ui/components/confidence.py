import streamlit as st
import numpy as np

def show_confidence(predictions):
    max_prob = float(np.max(predictions))

    st.markdown("Confidence")
            
    st.progress(max_prob)
    st.metric("Top Score", f"{max_prob*100:.2f}%")