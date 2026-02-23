import pytest
from unittest.mock import patch, Mock
from services.api import get_analytics_financeiro, APIException

class TestAnalyticsIntegrationFlow:
    """Testes de integração do fluxo de analytics"""
    
    @patch('services.api.requests.get')
    def test_full_analytics_flow(self, mock_get, sample_analytics_response):
        """Testa fluxo completo de analytics"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = sample_analytics_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Act
        analytics = get_analytics_financeiro(mes=1, ano=2024)
        
        # Assert - Estrutura completa
        assert all(key in analytics for key in [
            'resumo', 'saude_financeira', 'evolucao_diaria',
            'gastos_por_categoria', 'receitas_por_categoria', 'detalhamento'
        ])
        
        # Assert - Cálculos corretos
        assert analytics['resumo']['saldo'] == (
            analytics['resumo']['receitas_total'] - 
            analytics['resumo']['despesas_total']
        )
        
        # Assert - Detalhamento consistente
        assert analytics['detalhamento']['saldo_previsto'] == analytics['resumo']['saldo']
