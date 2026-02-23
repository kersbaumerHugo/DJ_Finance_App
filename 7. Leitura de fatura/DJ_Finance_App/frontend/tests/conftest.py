import pytest
import pandas as pd
from datetime import date, datetime

# ========== FIXTURES EXISTENTES ==========

@pytest.fixture
def sample_lancamento_data():
    """Dados de exemplo de um lançamento"""
    return {
        "id": 1,
        "descricao": "Compra no mercado",
        "data": "2024-01-15",
        "categoria": "Alimentação",
        "status": "Despesa",
        "valor": 150.50,
    }

@pytest.fixture
def sample_lancamentos_list():
    """Lista de lançamentos"""
    return [
        {
            "id": 1,
            "descricao": "Salário",
            "data": "2024-01-05",
            "categoria": "Renda",
            "status": "Receita",
            "valor": 5000.00,
        },
        {
            "id": 2,
            "descricao": "Conta de luz",
            "data": "2024-01-10",
            "categoria": "Utilidades",
            "status": "Despesa",
            "valor": 250.00,
        },
    ]

@pytest.fixture
def sample_dataframe():
    """DataFrame de exemplo para testes de tabelas"""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "descricao": ["Item 1", "Item 2", "Item 3"],
        "valor": [100.50, 200.75, 50.25],
        "categoria": ["A", "B", "A"],
    })

@pytest.fixture
def sample_resumo_response():
    """Resposta esperada do endpoint /resumo"""
    return {"faturamento": 128450, "usuarios": 342, "mes": "Janeiro"}

# ========== NOVAS FIXTURES ==========

@pytest.fixture
def sample_analytics_response():
    """Resposta completa do endpoint /analytics/"""
    return {
        "resumo": {
            "receitas_total": 10000.00,
            "despesas_total": 6500.00,
            "saldo": 3500.00,
            "quantidade_transacoes": 25
        },
        "saude_financeira": {
            "score": 70.0,
            "status": "Boa",
            "cor": "blue",
            "taxa_poupanca": 35.0,
            "percentual_gastos": 65.0
        },
        "evolucao_diaria": [
            {
                "data": "2024-01-01",
                "saldo_acumulado": 1000.00,
                "receitas_dia": 1000.00,
                "despesas_dia": 0.00,
                "saldo_dia": 1000.00
            },
            {
                "data": "2024-01-02",
                "saldo_acumulado": 800.00,
                "receitas_dia": 0.00,
                "despesas_dia": 200.00,
                "saldo_dia": -200.00
            }
        ],
        "gastos_por_categoria": [
            {
                "categoria": "Alimentação",
                "total": 2500.00,
                "count": 10,
                "percentual": 38.46
            },
            {
                "categoria": "Transporte",
                "total": 1500.00,
                "count": 5,
                "percentual": 23.08
            }
        ],
        "receitas_por_categoria": [
            {
                "categoria": "Salário",
                "total": 8000.00,
                "count": 2,
                "percentual": 80.0
            },
            {
                "categoria": "Freelance",
                "total": 2000.00,
                "count": 3,
                "percentual": 20.0
            }
        ],
        "detalhamento": {
            "entradas": {
                "Salário": [
                    {"subcategoria": "Salário Principal", "valor": 5000.00},
                    {"subcategoria": "Salário Extra", "valor": 3000.00}
                ],
                "Freelance": [
                    {"subcategoria": "Projeto A", "valor": 2000.00}
                ]
            },
            "saidas": {
                "Alimentação": [
                    {"subcategoria": "Supermercado", "valor": 1500.00},
                    {"subcategoria": "Restaurantes", "valor": 1000.00}
                ],
                "Transporte": [
                    {"subcategoria": "Gasolina", "valor": 800.00},
                    {"subcategoria": "Uber", "valor": 700.00}
                ]
            },
            "total_entradas": 10000.00,
            "total_saidas": 6500.00,
            "saldo_previsto": 3500.00
        }
    }

@pytest.fixture
def sample_evolucao_dataframe():
    """DataFrame de evolução processado"""
    return pd.DataFrame({
        'data': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'saldo_acumulado': [1000.00, 800.00, 1200.00],
        'receitas_dia': [1000.00, 0.00, 500.00],
        'despesas_dia': [0.00, 200.00, 100.00],
        'saldo_dia': [1000.00, -200.00, 400.00]
    })

@pytest.fixture
def sample_saude_financeira():
    """Dados de saúde financeira"""
    return {
        "score": 70.0,
        "status": "Boa",
        "cor": "blue",
        "taxa_poupanca": 35.0,
        "percentual_gastos": 65.0
    }
