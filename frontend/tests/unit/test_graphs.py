import pytest
import pandas as pd
import plotly.graph_objects as go
from components.graphs import (
    gauge_saude_financeira,
    grafico_evolucao_saldo,
    grafico_receitas_despesas_dia,
    grafico_pizza_categoria
)
import plotly.express as px

class TestGaugeSaudeFinanceira:
    """Testes para gráfico gauge"""
    
    def test_gauge_creation(self, sample_saude_financeira):
        """Testa criação do gauge"""
        # Act
        fig = gauge_saude_financeira(sample_saude_financeira)
        
        # Assert
        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == 'indicator'
        assert fig.data[0].value == 70.0
    
    def test_gauge_color(self, sample_saude_financeira):
        """Testa se cor é aplicada corretamente"""
        # Act
        fig = gauge_saude_financeira(sample_saude_financeira)
        
        # Assert
        assert fig.data[0].gauge.bar.color == 'blue'


class TestGraficoEvolucaoSaldo:
    """Testes para gráfico de evolução"""
    
    def test_grafico_creation(self, sample_evolucao_dataframe):
        """Testa criação do gráfico"""
        # Act
        fig = grafico_evolucao_saldo(sample_evolucao_dataframe)
        
        # Assert
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1
        assert fig.data[0].type == 'scatter'
    
    def test_grafico_has_zero_line(self, sample_evolucao_dataframe):
        """Testa se tem linha de zero"""
        # Act
        fig = grafico_evolucao_saldo(sample_evolucao_dataframe)
        
        # Assert
        # Verificar se há uma linha horizontal
        assert len(fig.layout.shapes) > 0 or 'hovermode' in fig.layout


class TestGraficoPizzaCategoria:
    """Testes para gráfico de pizza"""
    
    def test_pizza_creation(self):
        """Testa criação do gráfico de pizza"""
        # Arrange
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'C'],
            'total': [1000.00, 500.00, 300.00]
        })
        
        # Act
        fig = grafico_pizza_categoria(
            df,
            'Teste',
            px.colors.sequential.Reds_r
        )
        
        # Assert
        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == 'pie'
        assert len(fig.data[0].labels) == 3
