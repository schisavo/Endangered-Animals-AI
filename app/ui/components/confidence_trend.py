import streamlit as st
import pandas as pd

def show_confidence_trend(history_full, animal_names):
    st.markdown("### Animal Probability Trends")
    df = pd.DataFrame(history_full, columns=animal_names)
    st.line_chart(df)