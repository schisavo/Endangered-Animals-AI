import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# Mostrar dataset de World Wild Life
st.title("World Wildlife Dataset Visualization")

try:
    dataset_path = "./data/World Wildlife Species.csv"
    df = pd.read_csv(dataset_path)

    df['Scientifc Name']= df['Scientifc Name'].fillna("Unknown")
    df['Conservation Status'] = df['Conservation Status'].fillna("Unclassified")

    st.write("### Dataset Exploration")
    
    if st.checkbox("Show the first rows"):
        num_rows = st.slider("Number of rows to display:", min_value=10, max_value=97, value=10)
        st.dataframe(df.head(num_rows))
    
    if st.checkbox("Show descriptive statistics"):
        st.write("### Dataset Statistics")
        st.write(df.describe())
    
    if st.checkbox("Filter by Conservation Status"):
        species_list = df['Conservation Status'].unique()
        selected_species = st.selectbox("Select a Conservation Status:", species_list)
        filtered_df = df[df['Conservation Status'] == selected_species]
        st.write(f"### Data for {selected_species}")
        st.dataframe(filtered_df)

    if st.checkbox("Show Pie Chart of Conservation Status"):
        st.write("### Distribution of Conservation Status")
        status_counts = df['Conservation Status'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

except FileNotFoundError:
    st.error("The file `World Wildlife.csv` was not found. Please ensure it is in the correct directory.")
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")