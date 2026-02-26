import pytest
from freezegun import freeze_time
from django.core.management import call_command
from core.models import Recorrencia, Lancamento
from decimal import Decimal

@pytest.mark.django_db
class TestManagementCommands:
    
    def test_criar_recorrencias_padrao(self):
        """Testa criação de recorrências padrão"""
        call_command('criar_recorrencias_padrao')
        
        assert Recorrencia.objects.filter(descricao='Salário Hugo').exists()
        assert Recorrencia.objects.filter(descricao='Salário Geo').exists()
    
    @freeze_time("2026-02-01")
    def test_gerar_lancamentos_recorrentes(self):
        """Testa geração de lançamentos recorrentes"""
        # Criar recorrência
        Recorrencia.objects.create(
            descricao='Salário Test',
            tipo='ENTRADA',
            categoria='Salário',
            valor_padrao=Decimal('5000.00'),
            dia_vencimento=5,
            usa_dia_util=True,
            metodo_pagamento='PIX'
        )
        
        # Gerar lançamentos
        call_command('gerar_lancamentos_recorrentes', '--mes=2', '--ano=2026')
        
        # Verificar criação
        assert Lancamento.objects.filter(
            descricao='Salário Test',
            status_pagamento='PREVISIONADO',
            is_recorrente=True
        ).exists()
    
    def test_nao_duplica_lancamentos_recorrentes(self):
        """Testa que não duplica lançamentos ao executar comando novamente"""
        recorrencia = Recorrencia.objects.create(
            descricao='Test',
            tipo='ENTRADA',
            categoria='Test',
            valor_padrao=Decimal('100.00'),
            dia_vencimento=10,
            usa_dia_util=False,
            metodo_pagamento='PIX'
        )
        
        # Executar duas vezes
        call_command('gerar_lancamentos_recorrentes', '--mes=2', '--ano=2026')
        call_command('gerar_lancamentos_recorrentes', '--mes=2', '--ano=2026')
        
        # Deve ter apenas 1
        assert Lancamento.objects.filter(recorrencia_origem_id=recorrencia.id).count() == 1
