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
    def import_transacoes(transacoes: List[Dict[str, Any]], banco: str = 'NUBANK') -> Dict[str, int]:
        """
        Importa transações com proteção
        """
        from core.models import Lancamento
        from decimal import Decimal
        
        importadas = 0
        duplicadas = 0
        erros = 0
        deletadas = 0
        
        tem_csv = any(t.get('origem') == 'CSV' for t in transacoes)
        
        if tem_csv:
            print(f"🗑️ Deletando CSVs antigos do banco {banco}...")
            deleted_count = Lancamento.objects.filter(
                origem='CSV',
                metodo_pagamento__icontains=banco
            ).delete()[0]
            deletadas = deleted_count
            print(f"✅ {deleted_count} transações CSV antigas removidas")
        
        for transacao in transacoes:
            try:
                data_str = str(transacao['data'])
                if ' ' in data_str:
                    data_str = data_str.split(' ')[0]
                
                origem = transacao.get('origem', 'MANUAL')
                
                # ✅ Verificar duplicatas APENAS para PDF/MANUAL
                if origem not in ['CSV']:
                    existe = Lancamento.objects.filter(
                        data=data_str,
                        descricao=transacao['descricao'],
                        valor=Decimal(str(transacao['valor'])),
                        origem__in=['PDF', 'MANUAL']  # Não comparar com CSV
                    ).exists()
                    
                    if existe:
                        duplicadas += 1
                        print(f"⚠️ Duplicata detectada: {transacao['descricao']} em {data_str}")
                        continue
                
                # Criar lançamento
                Lancamento.objects.create(
                    descricao=transacao['descricao'],
                    data=data_str,
                    categoria=transacao['categoria'],
                    tipo=transacao.get('tipo', 'SAIDA'),
                    metodo_pagamento=transacao.get('metodo_pagamento', 'CREDITO_NUBANK'),
                    valor=Decimal(str(transacao['valor'])),
                    mes_referencia=transacao.get('mes_referencia'),
                    ano_referencia=transacao.get('ano_referencia'),
                    origem=origem
                )
                
                importadas += 1
                
            except Exception as e:
                print(f"❌ Erro ao importar: {e}")
                erros += 1
        
        return {
            'importadas': importadas,
            'duplicadas': duplicadas,
            'erros': erros,
            'deletadas_csv': deletadas
        }
        

