import streamlit as st
import pandas as pd

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/Species_clean.csv")

# ---------------- CLEAN ----------------
# eliminar filas sin coordenadas
df = df.dropna(subset=["lat", "lon"])

# ---------------- TITLE ----------------
st.title("🌍 Endangered Species Map")

# ---------------- FILTER ----------------
types = st.multiselect(
    "Filter by Type",
    options=df["Type"].unique(),
    default=df["Type"].unique()
)

df_filtered = df[df["Type"].isin(types)]

# ---------------- SIZE (Population) ----------------
def extract_population(value):
    try:
        value = str(value)
        num = "".join([c for c in value if c.isdigit()])
        return float(num) if num else 50
    except:
        return 50

df_filtered["size"] = df_filtered["Estimated Population"].apply(extract_population)

# ---------------- COLOR ----------------
color_map = {
    "Mammal": [255, 99, 132],
    "Bird": [54, 162, 235],
    "Reptile": [75, 192, 192],
    "Fish": [255, 206, 86],
    "Insect": [153, 102, 255],
    "Plant": [46, 204, 113],
    "Plant (Tree)": [0, 200, 120],
    "Amphibian": [0, 255, 180],
    "Fungi": [200, 200, 200]
}

df_filtered["color"] = df_filtered["Type"].apply(
    lambda x: color_map.get(x, [180,180,180])
)

# ---------------- MAP ----------------
st.map(
    df_filtered,
    latitude="lat",
    longitude="lon",
    size="size",
    color="color"
)

# ---------------- TABLE (BONUS) ----------------
with st.expander("📊 View Data"):
    st.dataframe(df_filtered[[
        "Common Name",
        "Type",
        "Estimated Population",
        "Threats"
    ]])