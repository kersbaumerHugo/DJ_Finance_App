import pytest
import pandas as pd
from tables.transformers import processar_evolucao_diaria

class TestProcessarEvolucaoDiaria:
    """Testes para processamento de evolução diária"""
    
    def test_processar_evolucao_success(self):
        """Testa processamento com dados válidos"""
        # Arrange
        dados = [
            {
                'data': '2024-01-01',
                'saldo_acumulado': 1000.00,
                'receitas_dia': 1000.00,
                'despesas_dia': 0.00,
                'saldo_dia': 1000.00
            },
            {
                'data': '2024-01-02',
                'saldo_acumulado': 800.00,
                'receitas_dia': 0.00,
                'despesas_dia': 200.00,
                'saldo_dia': -200.00
            }
        ]
        
        # Act
        df = processar_evolucao_diaria(dados)
        
        # Assert
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'data' in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['data'])
        assert df['saldo_acumulado'].iloc[0] == 1000.00
    
    def test_processar_evolucao_empty(self):
        """Testa comportamento com lista vazia"""
        # Act
        df = processar_evolucao_diaria([])
        
        # Assert
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    def test_processar_evolucao_sorted(self):
        """Testa se dados são ordenados por data"""
        # Arrange - Dados fora de ordem
        dados = [
            {'data': '2024-01-03', 'saldo_acumulado': 1500.00},
            {'data': '2024-01-01', 'saldo_acumulado': 1000.00},
            {'data': '2024-01-02', 'saldo_acumulado': 1200.00}
        ]
        
        # Act
        df = processar_evolucao_diaria(dados)
        
        # Assert
        assert df['data'].iloc[0] < df['data'].iloc[1]
        assert df['data'].iloc[1] < df['data'].iloc[2]
