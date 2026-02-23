"""Componentes de métricas (cards)"""
import streamlit as st
from typing import Optional

def metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    icon: str = ""
):
    """
    Renderiza um card de métrica padronizado
    
    Args:
        label: Texto do label
        value: Valor principal
        delta: Variação (opcional)
        delta_color: Cor do delta ("normal", "inverse", "off")
        icon: Emoji do ícone
    """
    full_label = f"{icon} {label}" if icon else label
    st.metric(label=full_label, value=value, delta=delta, delta_color=delta_color)


def resumo_financeiro_cards(resumo: dict, saude: dict):
    """
    Renderiza os 4 cards principais do resumo financeiro
    
    Args:
        resumo: Dicionário com resumo financeiro
        saude: Dicionário com indicadores de saúde
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            "Receitas",
            f"R$ {resumo['receitas_total']:,.2f}",
            icon="💵"
        )
    
    with col2:
        metric_card(
            "Despesas",
            f"R$ {resumo['despesas_total']:,.2f}",
            delta=f"-{saude['percentual_gastos']:.1f}% das receitas",
            delta_color="inverse",
            icon="💸"
        )
    
    with col3:
        metric_card(
            "Saldo",
            f"R$ {resumo['saldo']:,.2f}",
            delta=f"{saude['taxa_poupanca']:.1f}% economizado",
            delta_color="normal" if resumo['saldo'] >= 0 else "inverse",
            icon="💰"
        )
    
    with col4:
        metric_card(
            "Saúde Financeira",
            saude['status'],
            delta=f"Score: {saude['score']}/100",
            icon="🏥"
        )
