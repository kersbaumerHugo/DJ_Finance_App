import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Dashboard Financeiro")
st.write("Escolha uma área para acessar:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Resumo"):
        st.switch_page("pages\\1_Resumo.py")

with col2:
    if st.button("💰 Investimentos"):
        st.switch_page("2_Finanças.py")


