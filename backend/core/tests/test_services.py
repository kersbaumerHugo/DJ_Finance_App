import pytest
from django.test import TestCase
from core.models import Lancamento
from core.services import AnalyticsService
from datetime import date
from decimal import Decimal

from core.parsers.fatura_parser import FaturaProcessor
from core.models import Lancamento
class TestAnalyticsService(TestCase):
    """Testes para o serviço de analytics"""
    
    def setUp(self):
        """Criar dados de teste"""
        # Receitas
        Lancamento.objects.create(
            descricao="Salário",
            data=date(2024, 1, 5),
            categoria="Renda",
            status="Receita",
            valor=Decimal("5000.00")
        )
        Lancamento.objects.create(
            descricao="Freelance",
            data=date(2024, 1, 15),
            categoria="Renda",
            status="Receita",
            valor=Decimal("2000.00")
        )
        
        # Despesas
        Lancamento.objects.create(
            descricao="Supermercado",
            data=date(2024, 1, 10),
            categoria="Alimentação",
            status="Despesa",
            valor=Decimal("800.00")
        )
        Lancamento.objects.create(
            descricao="Gasolina",
            data=date(2024, 1, 20),
            categoria="Transporte",
            status="Despesa",
            valor=Decimal("300.00")
        )
    
    def test_calcular_resumo(self):
        """Testa cálculo do resumo financeiro"""
        # Arrange
        qs = Lancamento.objects.all()
        service = AnalyticsService()
        
        # Act
        resumo = service.calcular_resumo(qs)
        
        # Assert
        assert resumo['receitas_total'] == 7000.00
        assert resumo['despesas_total'] == 1100.00
        assert resumo['saldo'] == 5900.00
        assert resumo['quantidade_transacoes'] == 4
    
    def test_calcular_saude_financeira_excelente(self):
        """Testa classificação de saúde financeira como Excelente"""
        # Arrange
        service = AnalyticsService()
        receitas = 10000.00
        despesas = 7000.00  # 30% de poupança
        
        # Act
        saude = service.calcular_saude_financeira(receitas, despesas)
        
        # Assert
        assert saude['status'] == "Excelente"
        assert saude['cor'] == "green"
        assert saude['score'] == 90
        assert saude['taxa_poupanca'] == 30.0
    
    def test_calcular_saude_financeira_critica(self):
        """Testa classificação de saúde financeira como Crítica"""
        # Arrange
        service = AnalyticsService()
        receitas = 5000.00
        despesas = 6000.00  # Gastando mais que ganha
        
        # Act
        saude = service.calcular_saude_financeira(receitas, despesas)
        
        # Assert
        assert saude['status'] == "Crítica"
        assert saude['cor'] == "red"
        assert saude['score'] == 30
        assert saude['taxa_poupanca'] == -20.0
    
    def test_calcular_evolucao_diaria(self):
        """Testa cálculo de evolução diária"""
        # Arrange
        qs = Lancamento.objects.all()
        service = AnalyticsService()
        
        # Act
        evolucao = service.calcular_evolucao_diaria(qs)
        
        # Assert
        assert len(evolucao) > 0
        assert 'data' in evolucao[0]
        assert 'saldo_acumulado' in evolucao[0]
        assert 'receitas_dia' in evolucao[0]
        assert 'despesas_dia' in evolucao[0]
        
        # Verificar que saldo acumula corretamente
        primeiro_dia = evolucao[0]
        ultimo_dia = evolucao[-1]
        assert isinstance(primeiro_dia['saldo_acumulado'], float)
        assert isinstance(ultimo_dia['saldo_acumulado'], float)
    
    def test_analisar_por_categoria(self):
        """Testa análise por categoria"""
        # Arrange
        qs = Lancamento.objects.all()
        service = AnalyticsService()
        
        total_despesas = float(
        qs.filter(status='Despesa').aggregate(total=sum('valor'))['total'] or 0)
    
        # Act
        gastos = service.analisar_por_categoria(qs, 'Despesa', total_despesas)
        
        # Assert
        assert len(gastos) == 2
        assert gastos[0]['categoria'] in ['Alimentação', 'Transporte']
        assert 'total' in gastos[0]
        assert 'count' in gastos[0]
        assert 'percentual' in gastos[0]
        
        # Verificar que percentuais somam ~100%
        total_percentual = sum(cat['percentual'] for cat in gastos)
        assert 99.0 <= total_percentual <= 101.0  # Margem para arredondamento
    
    def test_detalhar_entradas_saidas(self):
        """Testa detalhamento de entradas e saídas"""
        # Arrange
        qs = Lancamento.objects.all()
        service = AnalyticsService()
        
        # Act
        detalhamento = service.detalhar_entradas_saidas(qs)
        
        # Assert
        assert 'entradas' in detalhamento
        assert 'saidas' in detalhamento
        assert 'total_entradas' in detalhamento
        assert 'total_saidas' in detalhamento
        assert 'saldo_previsto' in detalhamento
        
        # Verificar estrutura de entradas
        assert 'Renda' in detalhamento['entradas']
        assert len(detalhamento['entradas']['Renda']) == 2
        assert detalhamento['entradas']['Renda'][0]['subcategoria'] in ['Salário', 'Freelance']
        
        # Verificar totais
        assert detalhamento['total_entradas'] == 7000.00
        assert detalhamento['total_saidas'] == 1100.00
        assert detalhamento['saldo_previsto'] == 5900.00
