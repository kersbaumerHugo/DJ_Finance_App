"""Componentes de gráficos padronizados"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any

def gauge_saude_financeira(saude: Dict[str, Any]) -> go.Figure:
    """
    Cria gráfico gauge de saúde financeira
    
    Args:
        saude: Dicionário com indicadores de saúde
        
    Returns:
        Figura do Plotly
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=saude['score'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score de Saúde", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': saude['cor']},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ffcccc'},
                {'range': [30, 50], 'color': '#ffe6cc'},
                {'range': [50, 70], 'color': '#cce6ff'},
                {'range': [70, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def grafico_evolucao_saldo(df_evolucao: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de linha com evolução do saldo
    
    Args:
        df_evolucao: DataFrame com evolução diária
        
    Returns:
        Figura do Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_evolucao['data'],
        y=df_evolucao['saldo_acumulado'],
        mode='lines+markers',
        name='Saldo Acumulado',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title="Evolução do Saldo Acumulado",
        xaxis_title="Data",
        yaxis_title="Saldo (R$)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def grafico_receitas_despesas_dia(df_evolucao: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras comparando receitas e despesas por dia
    
    Args:
        df_evolucao: DataFrame com evolução diária
        
    Returns:
        Figura do Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_evolucao['data'],
        y=df_evolucao['receitas_dia'],
        name='Receitas',
        marker_color='#2ecc71'
    ))
    
    fig.add_trace(go.Bar(
        x=df_evolucao['data'],
        y=df_evolucao['despesas_dia'],
        name='Despesas',
        marker_color='#e74c3c'
    ))
    
    fig.update_layout(
        title="Receitas vs Despesas por Dia",
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        barmode='group',
        height=400
    )
    
    return fig


def grafico_pizza_categoria(
    df: pd.DataFrame,
    titulo: str,
    color_sequence
) -> go.Figure:
    """
    Cria gráfico de pizza para análise por categoria
    
    Args:
        df: DataFrame com dados por categoria
        titulo: Título do gráfico
        color_sequence: Sequência de cores do Plotly
        
    Returns:
        Figura do Plotly
    """
    fig = px.pie(
        df,
        values='total',
        names='categoria',
        title=titulo,
        color_discrete_sequence=color_sequence
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig
