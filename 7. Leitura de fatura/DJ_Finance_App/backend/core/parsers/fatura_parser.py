"""
Serviço de processamento de faturas
"""
from typing import List, Dict, Any
import os
from core.parsers.nubank_parser import NubankParser
from core.models import Lancamento
from decimal import Decimal


class FaturaProcessor:
    """Processa e importa faturas"""
    
    # Mapeamento de bancos para parsers
    PARSERS = {
        'nubank': NubankParser,
        # Adicionar outros conforme implementados
        # 'brb': BRBParser,
        # 'mercadopago': MercadoPagoParser,
        # 'cea': CEAParser,
    }
    
    @staticmethod
    def detect_banco(filename: str) -> str:
        """
        Detecta banco baseado no nome do arquivo
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            Nome do banco detectado
        """
        filename_lower = filename.lower()
        
        if 'nubank' in filename_lower:
            return 'nubank'
        elif 'brb' in filename_lower:
            return 'brb'
        elif 'mercadopago' in filename_lower or 'mp' in filename_lower:
            return 'mercadopago'
        elif 'cea' in filename_lower or 'c&a' in filename_lower:
            return 'cea'
        
        raise ValueError("Banco não identificado. Renomeie o arquivo incluindo o nome do banco.")
    
    @staticmethod
    def process_fatura(file_path: str, banco: str = None) -> Dict[str, Any]:
        """
        Processa arquivo de fatura
        
        Args:
            file_path: Caminho do arquivo
            banco: Nome do banco (opcional, será detectado automaticamente)
            
        Returns:
            dict: {
                'banco': str,
                'total_transacoes': int,
                'valor_total': float,
                'transacoes': List[Dict]
            }
        """
        # Detectar banco se não fornecido
        if not banco:
            banco = FaturaProcessor.detect_banco(os.path.basename(file_path))
        
        # Obter parser apropriado
        parser_class = FaturaProcessor.PARSERS.get(banco.lower())
        if not parser_class:
            raise ValueError(f"Parser para banco '{banco}' não implementado")
        
        # Processar arquivo
        parser = parser_class(file_path)
        transacoes = parser.process_file()
        
        # Calcular estatísticas
        valor_total = sum(t['valor'] for t in transacoes)
        
        return {
            'banco': banco,
            'total_transacoes': len(transacoes),
            'valor_total': valor_total,
            'transacoes': transacoes
        }
    
    @staticmethod
    def import_transacoes(transacoes: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Importa transações para o banco de dados
        """
        importadas = 0
        duplicadas = 0
        erros = 0
        
        for transacao in transacoes:
            try:
                # ✅ Converter data para formato correto
                data_str = str(transacao['data'])
                if ' ' in data_str:  # Remover hora se existir
                    data_str = data_str.split(' ')[0]
                
                # Verificar duplicatas
                existe = Lancamento.objects.filter(
                    data=data_str,  # ✅ Usar data formatada
                    descricao=transacao['descricao'],
                    valor=Decimal(str(transacao['valor']))
                ).exists()
                
                if existe:
                    duplicadas += 1
                    continue
                
                # Criar lançamento
                Lancamento.objects.create(
                    descricao=transacao['descricao'],
                    data=data_str,  # ✅ Usar data formatada
                    categoria=transacao['categoria'],
                    tipo=transacao['tipo'],
                    metodo_pagamento=transacao['metodo_pagamento'],
                    valor=Decimal(str(transacao['valor']))
                )
                
                importadas += 1
                
            except Exception as e:
                print(f"Erro ao importar transação: {e}")
                erros += 1
        
        return {
            'importadas': importadas,
            'duplicadas': duplicadas,
            'erros': erros
        }
