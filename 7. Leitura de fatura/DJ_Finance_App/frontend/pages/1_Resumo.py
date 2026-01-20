import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from services.api import get_resumo

data = get_resumo()


st.title("📊 Finanças Geral")


col1, col2, col3 = st.columns(3)
col1.metric("💰 Dinheiro na conta", f"R$ {data['faturamento']:,}")
col2.metric("👥 Previsão de fim de mês", data['usuarios'])
col3.metric("📅 Mês", data['mes'])

df = pd.DataFrame({
    "Categoria": ["A", "B", "C"],
    "Valor": [30, 50, 20]
})

fig = px.bar(df, x="Categoria", y="Valor", title="Distribuição")
st.plotly_chart(fig, use_container_width=True)
