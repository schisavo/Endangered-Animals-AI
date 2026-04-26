import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import random

# Mostar dataset de Species
def show_Species_Dataset():
    st.title("Endangered Species Dataset Visualization")

    try:
        dataset_path = "./data/Species.csv"
        df = pd.read_csv(dataset_path)
        df['Common Name'] = df['Common Name'].replace('-', 'Unknown Name')

        st.write("### Dataset Exploration")
        
        if st.checkbox("Show the first rows"):
            num_rows = st.slider("Number of rows to display:", min_value=10, max_value=90, value=10)
            st.dataframe(df.head(num_rows))
        
        if st.checkbox("Show descriptive statistics"):
            st.write("### Dataset Statistics")
            st.write(df.describe())
        
        if st.checkbox("Filter by species"):
            species_list = df['Species Name'].unique()
            selected_species = st.selectbox("Select a species:", species_list)
            filtered_df = df[df['Species Name'] == selected_species]
            st.write(f"### Data for {selected_species}")
            st.dataframe(filtered_df)
            
        if st.checkbox("Show Graph of Type"):
            animals = set()
            animals_type_dic = { }

            # Sacamos los tipos de animales unicos de el DataSet
            for tipo in df["Type"]:
                animals.add(tipo)    
            # Sacamos los datos y lo agregamos a un diccionario con la cantidad de animales
            # que hay en el DataSet del mismo tipo
            for i in animals:
                count = 0
                for tipo_animal in df.Type == i:
                    if tipo_animal == True:
                        count += 1 
                animals_type_dic[i] = count
            
            #Lista de colores
            RandomColor = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in animals_type_dic.keys()]
            fig, ax = plt.subplots()
            ax.set_title("Graph of animals and number of endangered species")
            ax.barh(animals_type_dic.keys(),animals_type_dic.values(),color=RandomColor)
            ax.set_xticks(range(0,21))
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("The file `Species.csv` was not found. Please ensure it is in the correct directory.")
    except Exception as e:
        st.error(f"An error occurred while loading the dataset: {e}")