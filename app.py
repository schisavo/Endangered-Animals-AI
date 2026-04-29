import streamlit as st

st.set_page_config(page_title="🌿 Endangered Animals Evaluation", layout="wide")

st.markdown(f"""
<style>

/* -------- Sidebar base -------- */
section[data-testid="stSidebar"] {{
    /*  background-color: transparent; sin fondo */
    border-right: 1px solid rgba(255,255,255,0.05);
    padding: 0px;
}}

/* -------- Items del menú -------- */
div[data-testid="stSidebarNav"] ul {{
    padding-top: 0px;
}}

/* Cada opción */
div[data-testid="stSidebarNav"] li {{
    margin: 0px 0px;
    border-radius: 12px;
    transition: all 0.3s ease;
}}

/* Botón interno */
div[data-testid="stSidebarNav"] a {{
    border-radius: 12px;
    padding: 1px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

/* -------- HOVER -------- */
div[data-testid="stSidebarNav"] a:hover {{
    background: linear-gradient(90deg, #215B63, #67C090);
    color: white !important;
    transform: translateX(5px);
    box-shadow: 0px 4px 15px rgba(103,192,144,0.3);
}}

/* -------- ITEM ACTIVO -------- */
div[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: linear-gradient(90deg, #67C090, #AAFFC7);
    color: #0b0f2a !important;
    font-weight: 600;
    box-shadow: 0px 4px 20px rgba(170,255,199,0.4);
}}

/* -------- ICONOS -------- */
div[data-testid="stSidebarNav"] svg {{
    width: 20px;
    height: 20px;
}}

/* -------- TEXTO -------- */
div[data-testid="stSidebarNav"] span {{
    font-size: 14px;
}}

/* -------- EFECTO SUAVE GENERAL -------- */
* {{
    transition: all 0.2s ease-in-out;
}}

</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/Main_Menu.py", title="Dashboard", icon=":material/home:"),
    st.Page("pages/Graphics_Species.py", title="Graphics Species", icon=":material/smart_toy:"),
    st.Page("pages/Graphics_World_Wildlife.py", title="Graphics World Wildlife", icon=":material/analytics:"), 
    st.Page("pages/Map_Graphics_Species.py", title="Map World Wildlife", icon=":material/map:") ])

st.sidebar.markdown("""
### 🌿 Endangered Animals Evaluation

![Version](https://img.shields.io/badge/version-1.0.0-67C090)
![License](https://img.shields.io/badge/license-Apache_2.0-AAFFC7)
![Status](https://img.shields.io/badge/status-active-215B63)

---

📁 **Project**  
Endangered Animals Evaluation  

👥 **Maintainers**  schisavo  

---
""")

st.sidebar.markdown("""
<div class="sidebar-divider"></div>
""", unsafe_allow_html=True)



pg.run()

