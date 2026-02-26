"""
Testes para o sistema de processamento de faturas
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.parsers.nubank_parser import NubankParser
from core.parsers.fatura_parser import FaturaProcessor
from core.models import Lancamento
import os
import tempfile
from decimal import Decimal


class NubankParserTest(TestCase):
    """Testes para o NubankParser"""
    
    def setUp(self):
        """Preparar ambiente de teste"""
        self.test_csv_content = """date,category,title,amount
2024-01-15,food,Mercado ABC,150.50
2024-01-20,transport,Uber,25.00
2024-01-25,food,Restaurante XYZ,80.00
"""
        # Criar arquivo temporário para teste
        self.temp_csv = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.csv', 
            delete=False
        )
        self.temp_csv.write(self.test_csv_content)
        self.temp_csv.close()
    
    def tearDown(self):
        """Limpar arquivos temporários"""
        if os.path.exists(self.temp_csv.name):
            os.remove(self.temp_csv.name)
    
    def test_extract_csv_success(self):
        """Testa extração bem-sucedida de CSV"""
        parser = NubankParser(self.temp_csv.name)
        df = parser.extract_data()
        
        # Verificar estrutura
        self.assertEqual(len(df), 3)
        self.assertIn('data', df.columns)
        self.assertIn('descricao', df.columns)
        self.assertIn('categoria', df.columns)
        self.assertIn('valor', df.columns)
    
    def test_categorization(self):
        """Testa categorização automática"""
        parser = NubankParser(self.temp_csv.name)
        transacoes = parser.process_file()
        
        # Verificar categorias
        categorias = [t['categoria'] for t in transacoes]
        self.assertIn('Alimentação', categorias)
        self.assertIn('Transporte', categorias)
    
    def test_valores_positivos(self):
        """Testa se valores são sempre positivos"""
        parser = NubankParser(self.temp_csv.name)
        transacoes = parser.process_file()
        
        for transacao in transacoes:
            self.assertGreater(transacao['valor'], 0)
    
    def test_total_valor(self):
        """Testa soma total dos valores"""
        parser = NubankParser(self.temp_csv.name)
        transacoes = parser.process_file()
        
        total = sum(t['valor'] for t in transacoes)
        self.assertAlmostEqual(total, 255.50, places=2)


class FaturaProcessorTest(TestCase):
    """Testes para o FaturaProcessor"""
    
    def setUp(self):
        """Preparar ambiente de teste"""
        self.test_csv_content = """date,category,title,amount
2024-01-15,food,Mercado ABC,150.50
2024-01-20,transport,Uber,25.00
"""
        self.temp_csv = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='_nubank.csv',
            delete=False
        )
        self.temp_csv.write(self.test_csv_content)
        self.temp_csv.close()
    
    def tearDown(self):
        """Limpar arquivos temporários"""
        if os.path.exists(self.temp_csv.name):
            os.remove(self.temp_csv.name)
    
    def test_detect_banco(self):
        """Testa detecção automática do banco"""
        banco = FaturaProcessor.detect_banco('fatura_nubank.csv')
        self.assertEqual(banco, 'nubank')
        
        banco = FaturaProcessor.detect_banco('extrato_brb.pdf')
        self.assertEqual(banco, 'brb')
    
    def test_process_fatura(self):
        """Testa processamento completo da fatura"""
        resultado = FaturaProcessor.process_fatura(self.temp_csv.name)
        
        self.assertEqual(resultado['banco'], 'nubank')
        self.assertEqual(resultado['total_transacoes'], 2)
        self.assertAlmostEqual(resultado['valor_total'], 175.50, places=2)
        self.assertIsInstance(resultado['transacoes'], list)
    
    def test_import_transacoes(self):
        """Testa importação de transações para o banco"""
        # Processar fatura
        resultado = FaturaProcessor.process_fatura(self.temp_csv.name)
        
        # Importar
        stats = FaturaProcessor.import_transacoes(resultado['transacoes'])
        
        self.assertEqual(stats['importadas'], 2)
        self.assertEqual(stats['duplicadas'], 0)
        self.assertEqual(stats['erros'], 0)
        
        # Verificar no banco
        self.assertEqual(Lancamento.objects.count(), 2)
    
    def test_detectar_duplicatas(self):
        """Testa detecção de transações duplicadas"""
        # Processar e importar primeira vez
        resultado = FaturaProcessor.process_fatura(self.temp_csv.name)
        stats1 = FaturaProcessor.import_transacoes(resultado['transacoes'])
        
        # Tentar importar novamente
        stats2 = FaturaProcessor.import_transacoes(resultado['transacoes'])
        
        self.assertEqual(stats1['importadas'], 2)
        self.assertEqual(stats2['importadas'], 0)
        self.assertEqual(stats2['duplicadas'], 2)


class FaturaIntegrationTest(TestCase):
    """Testes de integração completos"""
    
    def test_fluxo_completo_csv(self):
        """Testa fluxo completo: upload → processamento → importação"""
        # Criar CSV de teste
        csv_content = """date,category,title,amount
2024-01-10,food,Padaria,15.00
2024-01-15,transport,Uber,30.00
2024-01-20,health,Farmácia,50.00
"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='_nubank.csv',
            delete=False
        )
        temp_file.write(csv_content)
        temp_file.close()
        
        try:
            # 1. Processar fatura
            resultado = FaturaProcessor.process_fatura(temp_file.name)
            
            self.assertEqual(resultado['total_transacoes'], 3)
            self.assertEqual(len(resultado['transacoes']), 3)
            
            # 2. Importar
            stats = FaturaProcessor.import_transacoes(resultado['transacoes'])
            
            self.assertEqual(stats['importadas'], 3)
            
            # 3. Verificar no banco
            lancamentos = Lancamento.objects.all()
            self.assertEqual(lancamentos.count(), 3)
            
            # Verificar campos
            for lanc in lancamentos:
                self.assertIsNotNone(lanc.descricao)
                self.assertIsNotNone(lanc.data)
                self.assertIsNotNone(lanc.categoria)
                self.assertEqual(lanc.tipo, 'SAIDA')
                self.assertEqual(lanc.metodo_pagamento, 'CREDITO_NUBANK')
                self.assertGreater(lanc.valor, Decimal('0'))
            
            # Verificar categorias
            categorias = set(lanc.categoria for lanc in lancamentos)
            self.assertIn('Alimentação', categorias)
            self.assertIn('Transporte', categorias)
            self.assertIn('Saúde', categorias)
        
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
