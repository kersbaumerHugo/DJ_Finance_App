import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from services.api import criar_lancamento

st.subheader("➕ Novo lançamento")

with st.form("novo_lancamento"):
    data = st.date_input("Data")
    descricao = st.text_input("Descrição")
    categoria = st.text_input("Categoria")
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    valor = st.number_input("Valor", step=0.01)

    submitted = st.form_submit_button("Salvar")

if submitted:
    payload = {
        "data": data.isoformat(),
        "descricao": descricao,
        "categoria": categoria,
        "tipo": tipo,
        "valor": valor
    }

    resp = criar_lancamento(payload)

    if resp.status_code == 201:
        st.success("Lançamento salvo com sucesso!")
    else:
        st.error("Erro ao salvar")
        st.json(resp.json())
