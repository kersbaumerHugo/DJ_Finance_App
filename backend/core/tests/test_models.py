import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from core.models import Lancamento, Recorrencia

@pytest.mark.django_db
class TestLancamentoModel:
    
    def test_criar_lancamento_basico(self):
        """Testa criação de lançamento básico"""
        lancamento = Lancamento.objects.create(
            descricao='Test',
            data=timezone.now(),
            categoria='Teste',
            tipo='SAIDA',
            metodo_pagamento='PIX',
            valor=Decimal('100.00')
        )
        
        assert lancamento.id is not None
        assert lancamento.status_pagamento == 'PAGO'  # default
        assert lancamento.is_recorrente is False
        assert str(lancamento) == 'Test'
    
    def test_lancamento_previsionado(self):
        """Testa criação de lançamento previsionado"""
        lancamento = Lancamento.objects.create(
            descricao='Salário Hugo',
            data=timezone.now(),
            categoria='Salário',
            tipo='ENTRADA',
            metodo_pagamento='PIX',
            valor=Decimal('7800.00'),
            status_pagamento='PREVISIONADO',
            is_recorrente=True
        )
        
        assert lancamento.status_pagamento == 'PREVISIONADO'
        assert lancamento.is_recorrente is True
    
    def test_choices_status_pagamento(self):
        """Testa que status_pagamento aceita apenas valores válidos"""
        lancamento = Lancamento(
            descricao='Test',
            data=timezone.now(),
            categoria='Test',
            tipo='SAIDA',
            valor=Decimal('50.00'),
            status_pagamento='INVALIDO'
        )
        
        # Deve validar no save
        with pytest.raises(Exception):  # ValidationError
            lancamento.full_clean()


@pytest.mark.django_db
class TestRecorrenciaModel:
    
    def test_criar_recorrencia_salario(self):
        """Testa criação de recorrência de salário"""
        recorrencia = Recorrencia.objects.create(
            descricao='Salário Hugo',
            tipo='ENTRADA',
            categoria='Salário',
            valor_padrao=Decimal('7800.00'),
            dia_vencimento=5,
            usa_dia_util=True,
            metodo_pagamento='PIX',
            palavras_chave_matching='salario,hugo'
        )
        
        assert recorrencia.id is not None
        assert recorrencia.ativo is True  # default
        assert recorrencia.usa_dia_util is True
        assert str(recorrencia) == 'Salário Hugo - R$ 7800.00 (Dia 5)'
    
    def test_recorrencia_assinatura(self):
        """Testa criação de recorrência de assinatura"""
        recorrencia = Recorrencia.objects.create(
            descricao='YouTube Premium',
            tipo='SAIDA',
            categoria='Assinatura',
            valor_padrao=Decimal('35.99'),
            dia_vencimento=9,
            usa_dia_util=False,
            metodo_pagamento='CREDITO_NUBANK',
            palavras_chave_matching='youtube,premium'
        )
        
        assert recorrencia.usa_dia_util is False
        assert recorrencia.tipo == 'SAIDA'
