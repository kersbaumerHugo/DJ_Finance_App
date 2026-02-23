"""
Módulo de comunicação com a API Django
Todas as funções fazem requisições HTTP para o backend
"""

import requests
from typing import Dict, List, Any, Optional
from config.settings import API_BASE_URL, REQUEST_TIMEOUT


class APIException(Exception):
    """Exceção customizada para erros de API"""

    pass


def _handle_request_error(error: Exception, operation: str) -> None:
    """
    Centraliza o tratamento de erros de requisições

    Args:
        error: Exceção capturada
        operation: Nome da operação (para mensagem de erro)

    Raises:
        APIException: Com mensagem apropriada ao tipo de erro
    """
    if isinstance(error, requests.Timeout):
        raise APIException(f"Timeout ao {operation} (>{REQUEST_TIMEOUT}s)")
    elif isinstance(error, requests.ConnectionError):
        raise APIException(
            f"Erro de conexão ao {operation}. Verifique se a API está rodando em {API_BASE_URL}"
        )
    elif isinstance(error, requests.HTTPError):
        status_code = error.response.status_code
        try:
            error_detail = error.response.json()
        except:
            error_detail = error.response.text
        raise APIException(f"Erro HTTP {status_code} ao {operation}: {error_detail}")
    else:
        raise APIException(f"Erro inesperado ao {operation}: {str(error)}")


# ========== RESUMO ==========


def get_resumo() -> dict[str, Any]:
    """
    Busca o resumo financeiro do mês atual

    Returns:
        dict: Dados do resumo (faturamento, usuarios, mes)

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/resumo/"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        _handle_request_error(e, "buscar resumo")


# ========== LANÇAMENTOS - CRUD ==========


def get_lancamentos() -> list[dict[str, Any]]:
    """
    Busca todos os lançamentos

    Returns:
        list: Lista de lançamentos

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/lancamentos/"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        _handle_request_error(e, "buscar lançamentos")


def create_lancamento(data: dict[str, Any]) -> requests.Response:
    """
    Cria um novo lançamento

    Args:
        data: Dados do lançamento (descricao, data, categoria, status, valor)

    Returns:
        Response: Resposta da requisição

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/lancamentos/"
        response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        _handle_request_error(e, "criar lançamento")


def update_lancamento(lancamento_id: int, data: dict[str, Any]) -> requests.Response:
    """
    Atualiza um lançamento existente

    Args:
        lancamento_id: ID do lançamento a ser atualizado
        data: Dados atualizados

    Returns:
        Response: Resposta da requisição

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/lancamentos/{lancamento_id}/"
        response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        _handle_request_error(e, f"atualizar lançamento {lancamento_id}")


def delete_lancamento(lancamento_id: int) -> requests.Response:
    """
    Deleta um lançamento

    Args:
        lancamento_id: ID do lançamento a ser deletado

    Returns:
        Response: Resposta da requisição

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/lancamentos/{lancamento_id}/"
        response = requests.delete(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        _handle_request_error(e, f"deletar lançamento {lancamento_id}")


# ========== MESES ==========


def get_all_meses() -> dict[str, Any]:
    """
    Busca todos os meses com lançamentos

    Returns:
        dict: Estrutura com meses disponíveis

    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/lancamentos/meses/"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        _handle_request_error(e, "buscar meses")
        
# ========== ANALYTICS ==========

def get_analytics_financeiro(mes: Optional[int] = None, ano: Optional[int] = None) -> dict[str, Any]:
    """
    Busca análise financeira completa
    
    Args:
        mes: Mês para filtro (opcional)
        ano: Ano para filtro (opcional)
    
    Returns:
        dict: Análise completa com resumo, evolução e categorias
        
    Raises:
        APIException: Se houver erro na comunicação
    """
    try:
        url = f"{API_BASE_URL}/analytics/"
        params = {}
        if mes:
            params['mes'] = mes
        if ano:
            params['ano'] = ano
            
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        _handle_request_error(e, "buscar analytics financeiro")
