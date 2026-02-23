import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict
from services.api import (
    get_analytics_financeiro, 
    create_lancamento,
    update_lancamento,
    delete_lancamento,
    APIException
)
from components.tables import (
    tabela_editavel_entradas,
    tabela_editavel_saidas,
    processar_alteracoes
)
"""
Página para editar entradas e saídas mês a mês
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from services.api import (
    get_analytics_financeiro, 
    create_lancamento,
    update_lancamento,
    delete_lancamento,
    APIException
)
from components.tables import (
    tabela_editavel_entradas,
    tabela_editavel_saidas,
    processar_alteracoes
)

st.set_page_config(
    page_title="Editar Lançamentos",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Editar Lançamentos Mensais")

# ========== SELETOR DE MÊS/ANO ==========
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

mes_nome = datetime(2000, mes_selecionado, 1).strftime('%B %Y')

# ========== CARREGAR DADOS ==========
try:
    with st.spinner('📊 Carregando lançamentos...'):
        analytics = get_analytics_financeiro(mes=mes_selecionado, ano=ano_selecionado)
    
    detalhamento = analytics['detalhamento']
    entradas = detalhamento['entradas']
    saidas = detalhamento['saidas']
    
    # ✅ CORREÇÃO: Criar DataFrames originais com conversão de data
    df_entradas_original = pd.DataFrame(entradas)
    if not df_entradas_original.empty:
        df_entradas_original['data'] = pd.to_datetime(df_entradas_original['data'])
    
    df_saidas_original = pd.DataFrame(saidas)
    if not df_saidas_original.empty:
        df_saidas_original['data'] = pd.to_datetime(df_saidas_original['data'])
    
    # Salvar estado original no session_state
    if 'entradas_original' not in st.session_state:
        st.session_state.entradas_original = pd.DataFrame(entradas)
    
    if 'saidas_original' not in st.session_state:
        st.session_state.saidas_original = pd.DataFrame(saidas)
    
    # ========== TABELA DE ENTRADAS ==========
    st.markdown("---")
    entradas_editadas = tabela_editavel_entradas(entradas, mes_nome)
    
    # ========== TABELA DE SAÍDAS ==========
    st.markdown("---")
    saidas_editadas = tabela_editavel_saidas(saidas, mes_nome)
    
    # ========== RESUMO ==========
    st.markdown("---")
    col_resumo1, col_resumo2, col_resumo3 = st.columns(3)
    
    total_entradas = entradas_editadas['custo'].sum() if not entradas_editadas.empty else 0
    total_saidas = saidas_editadas['custo'].sum() if not saidas_editadas.empty else 0
    saldo = total_entradas - total_saidas
    
    with col_resumo1:
        st.metric("💵 Total Entradas", f"R$ {total_entradas:,.2f}")
    
    with col_resumo2:
        st.metric("💸 Total Saídas", f"R$ {total_saidas:,.2f}")
    
    with col_resumo3:
        delta_color = "normal" if saldo >= 0 else "inverse"
        st.metric("💰 Saldo", f"R$ {saldo:,.2f}", delta_color=delta_color)
    
    # ========== BOTÃO SALVAR ==========
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    
    with col_btn1:
        if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
            try:
                with st.spinner('Salvando alterações...'):
                    # Processar entradas
                    mudancas_entradas = processar_alteracoes(
                        st.session_state.entradas_original,
                        entradas_editadas
                    )
                    
                    # Processar saídas
                    mudancas_saidas = processar_alteracoes(
                        st.session_state.saidas_original,
                        saidas_editadas
                    )
                    
                    # No botão salvar, ao criar novos lançamentos:
                    # Aplicar mudanças nas entradas
                    for novo in mudancas_entradas['novos']:
                        payload = {
                            'descricao': novo['especificacao'],
                            'data': novo['data'],
                            'categoria': novo['categoria'],
                            'tipo': 'ENTRADA',  # ✅ CORRIGIR
                            'metodo_pagamento': novo.get('metodo_pagamento', 'TRANSFERENCIA'),
                            'valor': float(novo['custo'])
                        }
                        create_lancamento(payload)
                    
                    for atualizado in mudancas_entradas['atualizados']:
                        payload = {
                            'descricao': atualizado['especificacao'],
                            'data': atualizado['data'],
                            'categoria': atualizado['categoria'],
                            'valor': float(atualizado['custo'])
                        }
                        update_lancamento(int(atualizado['id']), payload)
                    
                    for deletado_id in mudancas_entradas['deletados']:
                        delete_lancamento(int(deletado_id))
                    
                    # Aplicar mudanças nas saídas
                    for novo in mudancas_saidas['novos']:
                        payload = {
                            'descricao': novo['especificacao'],
                            'data': novo['data'],
                            'categoria': novo['categoria'],
                            'tipo': 'SAIDA',  # ✅ CORRIGIR
                            'metodo_pagamento': novo.get('metodo_pagamento', 'PREVISIONADO'),
                            'valor': float(novo['custo'])
                        }
                        create_lancamento(payload)
                    
                    for atualizado in mudancas_saidas['atualizados']:
                        payload = {
                            'descricao': atualizado['especificacao'],
                            'data': atualizado['data'],
                            'categoria': atualizado['categoria'],
                            'valor': float(atualizado['custo'])
                        }
                        update_lancamento(int(atualizado['id']), payload)
                    
                    for deletado_id in mudancas_saidas['deletados']:
                        delete_lancamento(int(deletado_id))
                    
                    # Contar alterações
                    total_mudancas = (
                        len(mudancas_entradas['novos']) +
                        len(mudancas_entradas['atualizados']) +
                        len(mudancas_entradas['deletados']) +
                        len(mudancas_saidas['novos']) +
                        len(mudancas_saidas['atualizados']) +
                        len(mudancas_saidas['deletados'])
                    )
                    
                    if total_mudancas > 0:
                        st.success(f"✅ {total_mudancas} alteração(ões) salva(s) com sucesso!")
                        # Limpar cache
                        st.session_state.clear()
                        st.rerun()
                    else:
                        st.info("ℹ️ Nenhuma alteração detectada")
                        
            except APIException as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")
    
    with col_btn2:
        if st.button("🔄 Recarregar", use_container_width=True):
            st.session_state.clear()
            st.rerun()

except APIException as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    st.info("💡 Verifique se o backend está rodando")
    if st.button("🔄 Tentar novamente"):
        st.rerun()

except Exception as e:
    st.error(f"❌ Erro inesperado: {str(e)}")
    if st.checkbox("Mostrar detalhes técnicos"):
        st.exception(e)
