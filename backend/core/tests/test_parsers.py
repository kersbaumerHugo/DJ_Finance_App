import pytest
import pandas as pd
from decimal import Decimal
from core.parsers.nubank_parser import NubankParser

class TestNubankParser:
    
    @pytest.fixture
    def parser_csv(self, tmp_path):
        """Cria um CSV de teste"""
        csv_content = """date,title,amount
2026-02-10,Uber Uber *Trip Help.U,15.50
2026-02-10,McDonald's,35.90
2026-02-11,Pagamento recebido,-1000.00
2026-02-12,Amazon,99.90"""
        
        csv_file = tmp_path / "teste.csv"
        csv_file.write_text(csv_content)
        
        return NubankParser(str(csv_file), 'NUBANK')
    
    def test_parse_csv_basico(self, parser_csv):
        """Testa parsing básico de CSV"""
        df = parser_csv._extract_from_csv()
        
        assert len(df) == 3  # Exclui "Pagamento recebido"
        assert 'data' in df.columns
        assert 'descricao' in df.columns
        assert 'valor' in df.columns
        assert 'categoria' in df.columns
        assert df['origem'].iloc[0] == 'CSV'
    
    def test_parse_csv_filtra_pagamento(self, parser_csv):
        """Testa que filtra 'Pagamento recebido'"""
        df = parser_csv._extract_from_csv()
        
        assert 'Pagamento recebido' not in df['descricao'].values
    
    def test_categorizar_transporte(self, parser_csv):
        """Testa categorização de transporte"""
        categoria = parser_csv.categorizar_automatico('Uber *Trip')
        assert categoria == 'Transporte'
    
    def test_categorizar_alimentacao(self, parser_csv):
        """Testa categorização de alimentação"""
        categoria = parser_csv.categorizar_automatico('McDonald\'s')
        assert categoria == 'Alimentação'
    
    def test_categorizar_compras_online(self, parser_csv):
        """Testa categorização de compras online"""
        categoria = parser_csv.categorizar_automatico('Amazon')
        assert categoria == 'Compras Online'
    
    def test_valores_absolutos(self, parser_csv):
        """Testa que valores são sempre positivos"""
        df = parser_csv._extract_from_csv()
        
        assert (df['valor'] > 0).all()
