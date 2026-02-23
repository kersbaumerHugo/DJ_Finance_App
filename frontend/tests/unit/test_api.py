import pytest
from unittest.mock import patch, Mock
import requests
from services.api import (
    get_lancamentos,
    create_lancamento,
    update_lancamento,
    delete_lancamento,
    get_all_meses,
    API_BASE_URL,
)


class TestGetLancamentos:
    """Testes para a função get_lancamentos"""

    @patch("services.api.requests.get")
    def test_get_lancamentos_success(self, mock_get, sample_lancamentos_list):
        """Testa busca de lançamentos com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = sample_lancamentos_list
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result = get_lancamentos()

        # Assert
        assert len(result) == 2
        assert result[0]["descricao"] == "Salário"
        assert result[1]["valor"] == 250.00
        mock_get.assert_called_once_with(f"{API_BASE_URL}/lancamentos/", timeout=30)

    @patch("services.api.requests.get")
    def test_get_lancamentos_empty_list(self, mock_get):
        """Testa quando não há lançamentos"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Act
        result = get_lancamentos()

        # Assert
        assert result == []
        assert len(result) == 0

    @patch("services.api.requests.get")
    def test_get_lancamentos_network_error(self, mock_get):
        """Testa comportamento quando há erro de rede"""
        # Arrange
        mock_get.side_effect = requests.ConnectionError("Network error")

        # Act & Assert
        with pytest.raises(requests.ConnectionError):
            get_lancamentos()


class TestCreateLancamento:
    """Testes para criação de lançamentos"""

    @patch("services.api.requests.post")
    def test_create_lancamento_success(self, mock_post, sample_lancamento_data):
        """Testa criação de lançamento com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = sample_lancamento_data
        mock_post.return_value = mock_response

        payload = {
            "descricao": "Novo item",
            "data": "2024-01-20",
            "categoria": "Teste",
            "status": "Despesa",
            "valor": 100.00,
        }

        # Act
        result = create_lancamento(payload)

        # Assert
        assert result.status_code == 201
        mock_post.assert_called_once_with(f"{API_BASE_URL}/lancamentos/", timeout=30, json=payload)

    @patch("services.api.requests.post")
    def test_create_lancamento_validation_error(self, mock_post):
        """Testa criação com dados inválidos"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Dados inválidos"}
        mock_post.return_value = mock_response

        payload = {"descricao": ""}  # Payload inválido

        # Act
        result = create_lancamento(payload)

        # Assert
        assert result.status_code == 400


class TestUpdateLancamento:
    """Testes para atualização de lançamentos"""

    @patch("services.api.requests.put")
    def test_update_lancamento_success(self, mock_put):
        """Testa atualização com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        lancamento_id = 1
        payload = {"descricao": "Descrição atualizada"}

        # Act
        result = update_lancamento(lancamento_id, payload)

        # Assert
        assert result.status_code == 200
        mock_put.assert_called_once_with(
            f"{API_BASE_URL}/lancamentos/{lancamento_id}/", timeout=30, json=payload
        )


class TestDeleteLancamento:
    """Testes para exclusão de lançamentos"""

    @patch("services.api.requests.delete")
    def test_delete_lancamento_success(self, mock_delete):
        """Testa exclusão com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        lancamento_id = 1

        # Act
        result = delete_lancamento(lancamento_id)

        # Assert
        assert result.status_code == 204
        mock_delete.assert_called_once_with(f"{API_BASE_URL}/lancamentos/{lancamento_id}/", timeout=30)


class TestGetAllMeses:
    """Testes para buscar todos os meses"""

    @patch("services.api.requests.get")
    def test_get_all_meses_success(self, mock_get):
        """Testa busca de meses com sucesso"""
        # Arrange
        expected_data = {
            "index": ["Month", "Year"],
            0: ["Janeiro", "2026"],
            1: ["Dezembro", "2025"],
        }
        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        # Act
        result = get_all_meses()

        # Assert
        assert result == expected_data
        assert result["index"] == ["Month", "Year"]
# ... código existente ...

class TestGetAnalyticsFinanceiro:
    """Testes para a função get_analytics_financeiro"""
    
    @patch('services.api.requests.get')
    def test_get_analytics_success(self, mock_get, sample_analytics_response):
        """Testa busca de analytics com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = sample_analytics_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Act
        from services.api import get_analytics_financeiro
        result = get_analytics_financeiro(mes=1, ano=2024)
        
        # Assert
        assert 'resumo' in result
        assert 'saude_financeira' in result
        assert 'detalhamento' in result
        assert result['resumo']['receitas_total'] == 10000.00
        
        # Verificar chamada com parâmetros
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert 'params' in call_args[1]
        assert call_args[1]['params']['mes'] == 1
        assert call_args[1]['params']['ano'] == 2024
    
    @patch('services.api.requests.get')
    def test_get_analytics_without_filters(self, mock_get, sample_analytics_response):
        """Testa busca sem filtros"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = sample_analytics_response
        mock_get.return_value = mock_response
        
        # Act
        from services.api import get_analytics_financeiro
        result = get_analytics_financeiro()
        
        # Assert
        assert result is not None
        mock_get.assert_called_once()
        mock_get.assert_called_once_with(f"{API_BASE_URL}/lancamentos/meses/", timeout=30)
