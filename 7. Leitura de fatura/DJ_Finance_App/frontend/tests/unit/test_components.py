import pytest
from unittest.mock import patch, MagicMock

class TestMetricCard:
    """Testes para componente metric_card"""
    
    @patch('streamlit.metric')
    def test_metric_card_basic(self, mock_metric):
        """Testa renderização básica do card"""
        # Arrange
        from components.metrics import metric_card
        
        # Act
        metric_card("Teste", "R$ 1.000,00")
        
        # Assert
        mock_metric.assert_called_once()
        call_args = mock_metric.call_args[1]
        assert call_args['label'] == "Teste"
        assert call_args['value'] == "R$ 1.000,00"
    
    @patch('streamlit.metric')
    def test_metric_card_with_icon(self, mock_metric):
        """Testa card com ícone"""
        # Arrange
        from components.metrics import metric_card
        
        # Act
        metric_card("Teste", "100", icon="💰")
        
        # Assert
        call_args = mock_metric.call_args[1]
        assert "💰" in call_args['label']


class TestResumoFinanceiroCards:
    """Testes para componente resumo_financeiro_cards"""
    
    @patch('streamlit.columns')
    @patch('components.metrics.metric_card')
    def test_resumo_cards(self, mock_metric_card, mock_columns):
        """Testa renderização dos cards de resumo"""
        # Arrange
        from components.metrics import resumo_financeiro_cards
        
        mock_columns.return_value = [MagicMock() for _ in range(4)]
        
        resumo = {
            'receitas_total': 10000.00,
            'despesas_total': 6000.00,
            'saldo': 4000.00
        }
        saude = {
            'taxa_poupanca': 40.0,
            'percentual_gastos': 60.0,
            'status': 'Excelente',
            'score': 90
        }
        
        # Act
        resumo_financeiro_cards(resumo, saude)
        
        # Assert
        assert mock_metric_card.call_count == 4
