import pytest
from datetime import datetime
from freezegun import freeze_time
from core.utils.data_utils import eh_dia_util, calcular_n_dia_util, proximo_dia_util

class TestDataUtils:
    
    def test_eh_dia_util_segunda(self):
        """Testa que segunda-feira é dia útil"""
        # 03/02/2026 é uma terça-feira
        data = datetime(2026, 2, 3)
        assert eh_dia_util(data) is True
    
    def test_eh_dia_util_sabado(self):
        """Testa que sábado NÃO é dia útil"""
        # 07/02/2026 é um sábado
        data = datetime(2026, 2, 7)
        assert eh_dia_util(data) is False
    
    def test_eh_dia_util_domingo(self):
        """Testa que domingo NÃO é dia útil"""
        # 08/02/2026 é um domingo
        data = datetime(2026, 2, 8)
        assert eh_dia_util(data) is False
    
    def test_eh_dia_util_feriado_ano_novo(self):
        """Testa que feriado NÃO é dia útil"""
        # 01/01/2026 é Ano Novo (quinta-feira mas feriado)
        data = datetime(2026, 1, 1)
        assert eh_dia_util(data) is False
    
    def test_calcular_primeiro_dia_util(self):
        """Testa cálculo do 1º dia útil de fevereiro/2026"""
        # 01/02/2026 é domingo, então 1º dia útil é 02/02 (segunda)
        resultado = calcular_n_dia_util(2, 2026, 1)
        assert resultado.day == 2
        assert resultado.month == 2
    
    def test_calcular_quinto_dia_util(self):
        """Testa cálculo do 5º dia útil (para salários)"""
        # Fevereiro 2026: 02, 03, 04, 05, 06 (5º dia útil)
        resultado = calcular_n_dia_util(2, 2026, 5)
        assert resultado.day == 6
        assert resultado.month == 2
    
    def test_proximo_dia_util_de_sexta(self):
        """Testa próximo dia útil após sexta"""
        # 06/02/2026 é sexta, próximo útil é 09/02 (segunda)
        sexta = datetime(2026, 2, 6)
        resultado = proximo_dia_util(sexta)
        assert resultado.day == 9
    
    def test_calcular_dia_util_mes_sem_dias_suficientes(self):
        """Testa erro quando não há dias úteis suficientes"""
        # Fevereiro tem ~20 dias úteis
        with pytest.raises(ValueError):
            calcular_n_dia_util(2, 2026, 30)
