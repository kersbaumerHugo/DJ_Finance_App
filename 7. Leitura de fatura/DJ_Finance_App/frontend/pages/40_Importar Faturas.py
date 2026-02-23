"""
Página para importação de faturas
"""
import streamlit as st
import pandas as pd
import requests
from services.api import API_BASE_URL, APIException

st.set_page_config(
    page_title="Importar Faturas",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Importar Faturas")

# ========== UPLOAD DE ARQUIVO ==========
st.markdown("### 📤 Upload de Fatura")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Selecione o arquivo da fatura (CSV ou PDF)",
        type=['csv', 'pdf'],
        help="Formatos aceitos: CSV do Nubank, BRB, Mercado Pago, C&A"
    )

with col2:
    banco = st.selectbox(
        "Banco (opcional)",
        options=['Detectar automaticamente', 'Nubank', 'BRB', 'Mercado Pago', 'C&A']
    )

if uploaded_file:
    st.info(f"📁 Arquivo: **{uploaded_file.name}** ({uploaded_file.size} bytes)")
    
    # ========== PROCESSAR ARQUIVO ==========
    if st.button("🔍 Processar Fatura", type="primary"):
        with st.spinner('Processando fatura...'):
            try:
                # Preparar dados
                files = {'file': uploaded_file}
                data = {'banco': banco if banco != 'Detectar automaticamente' else None}
                
                # Enviar para API
                response = requests.post(
                    f"{API_BASE_URL}/faturas/upload/",
                    files=files,
                    data=data
                )
                response.raise_for_status()
                resultado = response.json()
                
                # Armazenar no session_state
                st.session_state.fatura_processada = resultado
                st.success(f"✅ Fatura processada com sucesso!")
                
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro ao processar: {str(e)}")

# ========== PREVIEW DOS DADOS ==========
if 'fatura_processada' in st.session_state:
    resultado = st.session_state.fatura_processada
    
    st.markdown("---")
    st.markdown("### 📊 Preview dos Dados")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏦 Banco", resultado['banco'].upper())
    with col2:
        st.metric("📝 Transações", resultado['total_transacoes'])
    with col3:
        st.metric("💰 Valor Total", f"R$ {resultado['valor_total']:,.2f}")
    
    # Tabela de transações
    st.markdown("#### Transações Detectadas")
    df_transacoes = pd.DataFrame(resultado['transacoes'])
    df_transacoes['data'] = pd.to_datetime(df_transacoes['data']).dt.strftime('%d/%m/%Y')
    
    st.dataframe(
        df_transacoes[['data', 'descricao', 'categoria', 'valor']],
        use_container_width=True,
        hide_index=True
    )
    
    # ========== IMPORTAR PARA O SISTEMA ==========
    st.markdown("---")
    st.markdown("### ✅ Confirmar Importação")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("💾 Importar Transações", type="primary", use_container_width=True):
            with st.spinner('Importando transações...'):
                try:
                    # Enviar para importação
                    response = requests.post(
                        f"{API_BASE_URL}/faturas/importar/",
                        json={'transacoes': resultado['transacoes']}
                    )
                    response.raise_for_status()
                    resultado_import = response.json()
                    
                    # Exibir resultado
                    st.success(f"✅ {resultado_import['importadas']} transações importadas!")
                    
                    if resultado_import['duplicadas'] > 0:
                        st.warning(f"⚠️ {resultado_import['duplicadas']} duplicadas ignoradas")
                    
                    if resultado_import['erros'] > 0:
                        st.error(f"❌ {resultado_import['erros']} erros")
                    
                    # Limpar session_state
                    del st.session_state.fatura_processada
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erro ao importar: {str(e)}")
