"""Layouts reutilizáveis"""
import streamlit as st
from typing import Dict

def interpretacao_saude(saude: Dict, quantidade: int):
    """
    Renderiza painel de interpretação da saúde financeira
    
    Args:
        saude: Dicionário com indicadores de saúde
        quantidade: Quantidade de transações
    """
    st.markdown("#### 📋 Interpretação")
    st.markdown(f"""
    **Status:** :{saude['cor']}[{saude['status']}]
    
    **Taxa de Poupança:** {saude['taxa_poupanca']:.1f}%
    
    **Percentual de Gastos:** {saude['percentual_gastos']:.1f}%
    
    **Transações:** {quantidade} no período
    """)
    
    # Dicas contextuais
    if saude['status'] == "Crítica":
        st.error("⚠️ Suas despesas estão maiores que as receitas!")
        st.info("💡 Revise seus gastos e identifique onde pode economizar.")
    elif saude['status'] == "Atenção":
        st.warning("⚠️ Você está gastando quase tudo que ganha.")
        st.info("💡 Tente economizar pelo menos 10% das suas receitas.")
    elif saude['status'] == "Boa":
        st.success("✅ Você está economizando! Continue assim.")
    else:
        st.success("🎉 Excelente! Você está com ótima saúde financeira!")
