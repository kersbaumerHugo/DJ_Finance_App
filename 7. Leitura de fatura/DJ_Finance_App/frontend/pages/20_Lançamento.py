import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Lançamentos",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Lançamentos")
st.write("Escolha um tipo de lançamento para realizar:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Novo Lançamento"):
        st.switch_page("pages\\21_Novo Lançamento.py")
with col2:
    if st.button("📝 Editar Lançamentos"):
        st.switch_page("pages\\22_Editar Lançamentos.py")
