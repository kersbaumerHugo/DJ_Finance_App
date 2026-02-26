"""
Dashboard Financeiro com Tabs: Base e Avançada
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

mes_nome = datetime(2000, mes_selecionado, 1).strftime('%B').upper()[:3]

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
    
    # ========== TABS ==========
    tab_base, tab_avancada = st.tabs(["📊 Visão Base", "📈 Visão Avançada"])
    
    # ========== TAB BASE (ESTILO EXCEL) ==========
    with tab_base:
        st.markdown("### 📊 Resumo do Período")
        resumo_financeiro_cards(resumo, saude)
        
        st.markdown("---")
        
        # Buscar lançamentos diretamente da API para ter controle total
        from services.api import get_lancamentos
        
        try:
            # Filtrar lançamentos do mês
            todos_lancamentos = get_lancamentos()
            
            # Filtrar por mês/ano
            import pandas as pd
            df_todos = pd.DataFrame(todos_lancamentos)
            
            if not df_todos.empty:
                df_todos['data'] = pd.to_datetime(df_todos['data'])
                df_filtrado = df_todos[
                    (df_todos['data'].dt.month == mes_selecionado) &
                    (df_todos['data'].dt.year == ano_selecionado)
                ]
                
                # Separar entradas e saídas
                entradas = df_filtrado[df_filtrado['tipo'] == 'ENTRADA']
                saidas = df_filtrado[df_filtrado['tipo'] == 'SAIDA']
                
                # Agrupar entradas por categoria
                entradas_por_categoria = {}
                for _, row in entradas.iterrows():
                    cat = row.get('categoria', 'Outros')
                    if cat not in entradas_por_categoria:
                        entradas_por_categoria[cat] = []
                    entradas_por_categoria[cat].append({
                        'subcategoria': row['descricao'][:30],
                        'valor': float(row['valor'])
                    })
                
                # Agrupar saídas por banco
                saidas_por_banco = {}
                for _, row in saidas.iterrows():
                    banco = row.get('metodo_pagamento', 'OUTROS')
                    banco_nome = banco.replace('CREDITO_', '').replace('_', ' ')
                    if banco_nome not in saidas_por_banco:
                        saidas_por_banco[banco_nome] = 0
                    saidas_por_banco[banco_nome] += float(row['valor'])
        
                # CSS Estilo Excel
                st.markdown("""
                <style>
                .tabela-excel {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 20px 0;
                }
                .mes-col {
                    background-color: #4a4a4a;
                    color: white;
                    font-size: 40px;
                    font-weight: bold;
                    text-align: center;
                    vertical-align: middle;
                    padding: 30px 15px;
                    border: 2px solid #333;
                }
                .secao-entrada {
                    background-color: #f8d7da;
                    color: #721c24;
                    font-weight: bold;
                    text-align: center;
                    padding: 12px;
                    border: 2px solid #721c24;
                }
                .secao-saida {
                    background-color: #d1ecf1;
                    color: #0c5460;
                    font-weight: bold;
                    text-align: center;
                    padding: 12px;
                    border: 2px solid #0c5460;
                }
                .categoria-entrada {
                    background-color: #f8d7da;
                    color: #721c24;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    border: 1px solid #999;
                }
                .categoria-saida {
                    background-color: #d1ecf1;
                    color: #0c5460;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    border: 1px solid #999;
                }
                .sub-cell {
                    background-color: white;
                    padding: 8px;
                    text-align: center;
                    border: 1px solid #999;
                }
                .val-cell {
                    background-color: white;
                    padding: 8px;
                    text-align: right;
                    font-weight: bold;
                    border: 1px solid #999;
                }
                .box-montante {
                    background-color: #d1ecf1;
                    border: 3px solid #0c5460;
                    color: #0c5460;
                    padding: 20px;
                    text-align: center;
                    margin: 10px 0;
                }
                .box-previsionado {
                    background-color: #f8d7da;
                    border: 3px solid #721c24;
                    color: #721c24;
                    padding: 20px;
                    text-align: center;
                    margin: 10px 0;
                }
                .box-titulo {
                    font-size: 14px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .box-valor {
                    font-size: 28px;
                    font-weight: bold;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Layout: Tabela + Boxes
                col_tabela, col_boxes = st.columns([3, 1])
                
                with col_tabela:
                    if entradas_por_categoria or saidas_por_banco:
                        st.markdown("#### 📊 Visão por Banco/Categoria")
                        # Construir tabela HTML
                        html = '<table class="tabela-excel"><tr>'
                        html += f'<td rowspan="50" class="mes-col">{mes_nome}</td>'
                        
                        # ENTRADAS
                        total_linhas_entrada = sum(len(items) for items in entradas_por_categoria.values())
                        html += f'<td rowspan="{total_linhas_entrada}" class="secao-entrada">ENTRADA</td>'
                        
                        primeira = True
                        for cat, items in entradas_por_categoria.items():
                            if not primeira:
                                html += '<tr>'
                            html += f'<td rowspan="{len(items)}" class="categoria-entrada">{cat.upper()}</td>'
                            if items:
                                html += f'<td class="sub-cell">{items[0]["subcategoria"]}</td>'
                                html += f'<td class="val-cell">R$ {items[0]["valor"]:,.2f}</td></tr>'
                            for item in items[1:]:
                                html += f'<tr><td class="sub-cell">{item["subcategoria"]}</td>'
                                html += f'<td class="val-cell">R$ {item["valor"]:,.2f}</td></tr>'
                            primeira = False
                        
                        # SAÍDAS
                        html += f'<tr><td rowspan="{len(saidas_por_banco) + 1}" class="secao-saida">SAÍDA</td>'
                        html += f'<td rowspan="{len(saidas_por_banco)}" class="categoria-saida">FATURAS</td>'
                        
                        primeira = True
                        for banco, valor in saidas_por_banco.items():
                            if not primeira:
                                html += '<tr>'
                            html += f'<td class="sub-cell">{banco}</td>'
                            html += f'<td class="val-cell">R$ {valor:,.2f}</td></tr>'
                            primeira = False
                        
                        html += '</table>'
                        st.markdown(html, unsafe_allow_html=True)
                    else:
                        st.info("📭 Nenhum dado para exibir neste período")
                
                with col_boxes:
                    st.markdown(f'''
                    <div class="box-montante">
                        <div class="box-titulo">MONTANTE</div>
                        <div class="box-valor">R$ {resumo["receitas_total"]:,.2f}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="box-previsionado">
                        <div class="box-titulo">MONTANTE PREVISIONADO</div>
                        <div class="box-valor">R$ {resumo["saldo"]:,.2f}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.info("📭 Nenhum lançamento encontrado")
        except Exception as e:
            st.error(f"Erro ao carregar dados da tab base: {str(e)}")
            st.exception(e)
    
    # ========== TAB AVANÇADA (GRÁFICOS) ==========
    with tab_avancada:
        st.markdown("### 🏥 Indicador de Saúde Financeira")
        col_ind1, col_ind2 = st.columns([2, 1])
        
        with col_ind1:
            fig_gauge = gauge_saude_financeira(saude)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col_ind2:
            interpretacao_saude(saude, resumo['quantidade_transacoes'])
        
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
