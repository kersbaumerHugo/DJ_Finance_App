import streamlit as st
#import requests
#import pandas as pd
#import plotly.express as px

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="🏠",
    layout="wide"
)

# ========== VERIFICAÇÃO AUTOMÁTICA DE RECORRÊNCIAS ==========
def verificar_recorrencias_auto():
    """
    Verifica e gera lançamentos recorrentes automaticamente
    Executa apenas uma vez por dia
    """
    hoje = datetime.now().date()
    
    # Verificar se já executou hoje
    if 'ultima_verificacao_recorrencias' in st.session_state:
        if st.session_state.ultima_verificacao_recorrencias == hoje:
            return
    
    try:
        # Chamar endpoint de verificação (vamos criar)
        from services.api import verificar_recorrencias
        resultado = verificar_recorrencias()
        
        if resultado.get('criados', 0) > 0:
            st.toast(f"✅ {resultado['criados']} lançamento(s) recorrente(s) criado(s)!", icon="✅")
        
        # Marcar como verificado hoje
        st.session_state.ultima_verificacao_recorrencias = hoje
        
    except Exception as e:
        pass  # Falha silenciosa para não atrapalhar UX

# Executar verificação
verificar_recorrencias_auto()

st.title("🏠 Dashboard Financeiro")
st.write("Escolha uma área para acessar:")

col1, col2, col3  = st.columns(3)

with col1:
    if st.button("📊 Resumo"):
        st.switch_page("pages\\1_Resumo.py")
with col2:
    if st.button("📝 Lançamento"):
        st.switch_page("pages\\20_Lançamento.py")
        
with col3:
    if st.button("💰 Investimentos"):
        st.switch_page("pages\\3_Investimentos.py")
        


