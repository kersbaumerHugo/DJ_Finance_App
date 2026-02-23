"""
Dashboard Financeiro - APENAS ORQUESTRAÇÃO
Toda lógica está nos componentes e transformers
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from services.api import get_analytics_financeiro, APIException
from components.metrics import resumo_financeiro_cards
from components.graphs import (
    gauge_saude_financeira,
    grafico_evolucao_saldo,
    grafico_receitas_despesas_dia,
    grafico_pizza_categoria
)
from components.layouts import interpretacao_saude
from tables.transformers import processar_evolucao_diaria
import plotly.express as px
from components.tables import tabela_detalhamento_financeiro  # ✅ NOVO

st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Dashboard Financeiro")

# ========== FILTROS ==========
col_filtro1, col_filtro2 = st.columns(2)
with col_filtro1:
    mes_selecionado = st.selectbox(
        "Mês",
        options=list(range(1, 13)),
        index=datetime.now().month - 1,
        format_func=lambda x: datetime(2000, x, 1).strftime('%B')
    )

with col_filtro2:
    ano_selecionado = st.selectbox(
        "Ano",
        options=list(range(datetime.now().year - 2, datetime.now().year + 1)),
        index=2
    )

# ========== CARREGAR DADOS ==========
try:
    with st.spinner('📊 Carregando análise financeira...'):
        analytics = get_analytics_financeiro(mes=mes_selecionado, ano=ano_selecionado)
    
    resumo = analytics['resumo']
    saude = analytics['saude_financeira']
    evolucao = analytics['evolucao_diaria']
    gastos_cat = analytics['gastos_por_categoria']
    receitas_cat = analytics['receitas_por_categoria']
    detalhamento = analytics['detalhamento']
    # Nome do mês para exibição
    mes_nome = datetime(2000, mes_selecionado, 1).strftime('%B').upper()[:3]
    
    # ========== SEÇÃO 1: RESUMO ==========
    st.markdown("### 📊 Resumo do Período")
    resumo_financeiro_cards(resumo, saude)
    
    # ========== SEÇÃO 1.5: TABELA DETALHADA (NOVA!) ==========
    st.markdown("---")
    st.markdown("### 📋 Detalhamento de Entradas e Saídas")
    if detalhamento['entradas']:
        st.markdown("#### 💵 Entradas")
        df_entradas = pd.DataFrame(detalhamento['entradas'])
        st.dataframe(df_entradas, use_container_width=True, hide_index=True)
        st.metric("Total Entradas", f"R$ {detalhamento['total_entradas']:,.2f}")
    if detalhamento['saidas']:
        st.markdown("#### 💸 Saídas")
        df_saidas = pd.DataFrame(detalhamento['saidas'])
        st.dataframe(df_saidas, use_container_width=True, hide_index=True)
        st.metric("Total Saídas", f"R$ {detalhamento['total_saidas']:,.2f}")
    #tabela_detalhamento_financeiro(detalhamento, mes_nome)
    
    # ========== SEÇÃO 2: SAÚDE FINANCEIRA ==========
    st.markdown("---")
    st.markdown("### 🏥 Indicador de Saúde Financeira")
    
    col_ind1, col_ind2 = st.columns([2, 1])
    
    with col_ind1:
        fig_gauge = gauge_saude_financeira(saude)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col_ind2:
        interpretacao_saude(saude, resumo['quantidade_transacoes'])
    
    # ========== SEÇÃO 3: EVOLUÇÃO ==========
    st.markdown("---")
    st.markdown("### 📈 Evolução do Saldo (Dia a Dia)")
    
    if evolucao:
        df_evolucao = processar_evolucao_diaria(evolucao)
        
        fig_evolucao = grafico_evolucao_saldo(df_evolucao)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        
        fig_bars = grafico_receitas_despesas_dia(df_evolucao)
        st.plotly_chart(fig_bars, use_container_width=True)
    else:
        st.info("📭 Nenhuma transação encontrada neste período")
    
    # ========== SEÇÃO 4: CATEGORIAS ==========
    st.markdown("---")
    st.markdown("### 📊 Análise por Categoria")
    
    col_cat1, col_cat2 = st.columns(2)
    
    with col_cat1:
        st.markdown("#### 💸 Despesas por Categoria")
        if gastos_cat:
            df_gastos = pd.DataFrame(gastos_cat)
            fig_gastos = grafico_pizza_categoria(
                df_gastos,
                'Distribuição de Despesas',
                px.colors.sequential.Reds_r
            )
            st.plotly_chart(fig_gastos, use_container_width=True)
            
            st.dataframe(
                df_gastos[['categoria', 'total', 'count', 'percentual']].rename(columns={
                    'categoria': 'Categoria',
                    'total': 'Total (R$)',
                    'count': 'Quantidade',
                    'percentual': '%'
                }),
                hide_index=True
            )
        else:
            st.info("Nenhuma despesa registrada")
    
    with col_cat2:
        st.markdown("#### 💵 Receitas por Categoria")
        if receitas_cat:
            df_receitas = pd.DataFrame(receitas_cat)
            fig_receitas = grafico_pizza_categoria(
                df_receitas,
                'Distribuição de Receitas',
                px.colors.sequential.Greens_r
            )
            st.plotly_chart(fig_receitas, use_container_width=True)
            
            st.dataframe(
                df_receitas[['categoria', 'total', 'count', 'percentual']].rename(columns={
                    'categoria': 'Categoria',
                    'total': 'Total (R$)',
                    'count': 'Quantidade',
                    'percentual': '%'
                }),
                hide_index=True
            )
        else:
            st.info("Nenhuma receita registrada")


    
    
    

except APIException as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    st.info("💡 Verifique se o backend está rodando")
    if st.button("🔄 Tentar novamente"):
        st.rerun()
except Exception as e:
    st.error(f"❌ Erro inesperado: {str(e)}")
    if st.checkbox("Mostrar detalhes técnicos"):
        st.exception(e)


