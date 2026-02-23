import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pandas as pd
import streamlit as st
from services.api import *

tab1 = st.tabs(["Resumo", "Proventos"])

st.set_page_config(layout="wide")
col_list = []
subcol_list = []
for col in st.columns(
    4,
    border=True,
):
    col_list.append(col)

patrim_total = 100
luc_total = 100
provent_total = 100
variacao = 0.1470
rentabilidade = 0.2356


with col_list[0]:
    st.metric("Patrimônio total", patrim_total, format="R$%.2f")
with col_list[1]:
    st.metric("Lucro Total", luc_total, format="R$%.2f")
with col_list[2]:
    st.metric("Proventos recebidos", provent_total, format="R$%.2f")
with col_list[3]:
    subcol_list = []
    for col in st.columns(2):
        subcol_list.append(col)
    with subcol_list[0]:
        st.metric("Variação", variacao, format="percent")
    with subcol_list[1]:
        st.metric("Rentabilidade", rentabilidade, format="percent")
