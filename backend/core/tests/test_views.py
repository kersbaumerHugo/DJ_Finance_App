import pytest
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Lancamento
from datetime import date
from decimal import Decimal
import json

class TestAnalyticsView(TestCase):
    """Testes para a view de analytics"""
    
    def setUp(self):
        """Configurar cliente e dados de teste"""
        self.client = Client()
        
        # Criar lançamentos de teste
        Lancamento.objects.create(
            descricao="Salário",
            data=date(2024, 1, 5),
            categoria="Renda",
            status="Receita",
            valor=Decimal("5000.00")
        )
        Lancamento.objects.create(
            descricao="Mercado",
            data=date(2024, 1, 10),
            categoria="Alimentação",
            status="Despesa",
            valor=Decimal("500.00")
        )
    
    def test_analytics_endpoint_success(self):
        """Testa se endpoint retorna dados corretamente"""
        # Act
        response = self.client.get('/api/analytics/')
        
        # Assert
        # ✅ CORREÇÃO: Adicionar debug se falhar
        if response.status_code != 200:
            print(f"Status: {response.status_code}")
            print(f"Content: {response.content}")
        assert response.status_code == 200
        data = response.json()
        
        assert 'resumo' in data
        assert 'saude_financeira' in data
        assert 'evolucao_diaria' in data
        assert 'gastos_por_categoria' in data
        assert 'receitas_por_categoria' in data
        assert 'detalhamento' in data
    
    def test_analytics_with_filters(self):
        """Testa filtros de mês e ano"""
        # Act
        response = self.client.get('/api/analytics/', {
            'mes': 1,
            'ano': 2024
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['resumo']['quantidade_transacoes'] >= 0
    
    def test_analytics_empty_data(self):
        """Testa comportamento com dados vazios"""
        # Arrange - Limpar dados
        Lancamento.objects.all().delete()
        
        # Act
        response = self.client.get('/api/analytics/')
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['resumo']['receitas_total'] == 0.0
        assert data['resumo']['despesas_total'] == 0.0
        assert data['evolucao_diaria'] == []
