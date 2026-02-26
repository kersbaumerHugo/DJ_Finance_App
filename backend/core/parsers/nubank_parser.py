"""
Parser completo para faturas Nubank (PDF e CSV)
"""
import re
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from .base_parser import BaseParser

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class NubankParser(BaseParser):
    """
    Parser para faturas Nubank
    
    Suporta:
    - PDF de fatura (extração com pdfplumber)
    - CSV exportado do app Nubank
    """
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.is_pdf = file_path.lower().endswith('.pdf')
    
    def extract_data(self) -> pd.DataFrame:
        """
        Extrai dados do arquivo Nubank (PDF ou CSV)
        """
        if self.is_pdf:
            return self._extract_from_pdf()
        else:
            return self._extract_from_csv()
    
    def _extract_from_csv(self) -> pd.DataFrame:
        """
        Extrai dados do CSV do Nubank
        Formato: date,title,amount
        """
        try:
            # Ler CSV
            df = pd.read_csv(self.file_path, encoding='utf-8')
            
            print(f"📊 Colunas: {df.columns.tolist()}")
            print(f"📊 Total linhas: {len(df)}")
            
            # Renomear colunas
            df = df.rename(columns={
                'date': 'data',
                'title': 'descricao',
                'amount': 'valor'
            })
            
            # Processar data
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%Y-%m-%d')
            
            # Processar valor (já vem como número, apenas garantir absoluto)
            df['valor'] = df['valor'].abs()
            
            # Filtrar "Pagamento recebido"
            df = df[~df['descricao'].str.contains('Pagamento recebido', case=False, na=False)]
            
            # Extrair mês/ano de referência
            primeira_data = pd.to_datetime(df['data'].iloc[0])
            mes_referencia = primeira_data.month
            ano_referencia = primeira_data.year
            
            # Adicionar metadados
            df['mes_referencia'] = mes_referencia
            df['ano_referencia'] = ano_referencia
            df['origem'] = 'CSV'
            
            # Categorizar
            df['categoria'] = df['descricao'].apply(self.categorizar_automatico)
            
            print(f"✅ {len(df)} transações extraídas do CSV")
            
            return df[['data', 'descricao', 'categoria', 'valor', 'mes_referencia', 'ano_referencia', 'origem']]
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise ValueError(f"Erro ao processar CSV: {str(e)}")
        
    
    def _extract_from_pdf(self) -> pd.DataFrame:
        """
        Extrai dados do PDF da fatura Nubank
        """
        if not PDF_AVAILABLE:
            raise ValueError("pdfplumber não instalado")
        
        try:
            transacoes = []
            
            with pdfplumber.open(self.file_path) as pdf:
                texto_completo = ""
                for page in pdf.pages:
                    texto_completo += page.extract_text() + "\n"
                
                # Extrair info da fatura
                ref_fatura = re.search(r'FATURA\s+\d{2}\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)\s+(20\d{2})', texto_completo, re.I)
                periodo = re.search(r'Período vigente:\s*(\d{1,2})\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)\s+a\s+(\d{1,2})\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)', texto_completo, re.I)
                
                meses = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
                
                ano_fatura = int(ref_fatura.group(2)) if ref_fatura else 2024
                mes_fatura = meses[ref_fatura.group(1).upper()] if ref_fatura else 1
                
                if periodo:
                    mes_inicio = meses[periodo.group(2).upper()]
                    mes_fim = meses[periodo.group(4).upper()]
                    ano_inicio = ano_fatura if mes_inicio <= mes_fatura else ano_fatura - 1
                    ano_fim = ano_fatura if mes_fim <= mes_fatura else ano_fatura - 1
                else:
                    ano_inicio = ano_fim = ano_fatura
                    mes_inicio = mes_fim = mes_fatura
                
                print(f"📅 Ref: {mes_fatura:02d}/{ano_fatura} | Período: {mes_inicio:02d}/{ano_inicio} a {mes_fim:02d}/{ano_fim}")
                
                # ✅ REGEX ULTRA SIMPLES - Captura qualquer coisa entre DATA e R$
                # Formato: "DD MÊS" + quebra/espaços + texto + "R$" + valor
                pattern = r'(\d{1,2})\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)\s+(.+?)\s+R\$\s+([\d.,\-]+)'
                
                for match in re.finditer(pattern, texto_completo, re.IGNORECASE | re.DOTALL):
                    dia = int(match.group(1))
                    mes_str = match.group(2).upper()
                    desc_bruta = match.group(3)
                    valor_str = match.group(4)
                    
                    mes = meses[mes_str]
                    
                    # Determinar ano
                    ano_transacao = ano_inicio if mes >= mes_inicio else ano_fim
                    
                    # Limpar descrição: remove quebras, data repetida, espaços extras
                    desc = re.sub(r'\n+', ' ', desc_bruta)  # Remove quebras
                    desc = re.sub(r'^\d{1,2}\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)\s+', '', desc, flags=re.I)  # Remove data repetida
                    desc = ' '.join(desc.split())  # Normaliza espaços
                    desc = desc.strip()
                    
                    # Limpar valor
                    valor_str = valor_str.replace('.', '').replace(',', '.')
                    if valor_str.startswith('-'):
                        valor_str = valor_str[1:]  # Remove sinal negativo (pagamentos)
                    
                    # Validar
                    if self._is_valid_transaction(desc, valor_str):
                        try:
                            data = datetime(ano_transacao, mes, dia).strftime('%Y-%m-%d')
                            valor = float(valor_str)
                            
                            transacoes.append({
                                'data': data,
                                'descricao': desc,
                                'valor': valor,
                                'mes_referencia': mes_fatura,
                                'ano_referencia': ano_fatura,
                                'origem': 'PDF'
                            })
                        except:
                            continue
            
            print(f"✅ {len(transacoes)} transações capturadas")
            
            if not transacoes:
                raise ValueError("Nenhuma transação encontrada")
            
            df = pd.DataFrame(transacoes)
            #df = df.drop_duplicates(subset=['data', 'descricao', 'valor'])
            df['categoria'] = df['descricao'].apply(self.categorizar_automatico)
            
            return df[['data', 'descricao', 'categoria', 'valor', 'mes_referencia', 'ano_referencia', 'origem']]
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise ValueError(f"Erro: {str(e)}")

    def _is_valid_transaction(self, descricao: str, valor_str: str) -> bool:
        """
        Valida se uma linha é realmente uma transação válida
        """
        desc_clean = descricao.strip().lower()
        
        # ✅ FILTRAR "Pagamento em DD MÊS"
        if re.match(r'^pagamento em \d{1,2} (jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)', desc_clean):
            return False
        
        # Lista de strings inválidas
        invalidos = [
            'transações de',
            'total de compras',
            'fatura anterior',
            'pagamento recebido',
            'outros lançamentos',
            'total a pagar',
            'pagamento mínimo',
            'saldo restante',
            'limite total',
            'saldo em aberto',
            'fechamento',
            'emissão',
            'de 16',
            'hugo kersbaumer',
            'nubank',
        ]
        
        # Filtro "a DD MÊS"
        if re.match(r'^a\s+\d{1,2}\s+(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)$', desc_clean):
            return False
        
        for invalido in invalidos:
            if invalido in desc_clean:
                return False
        
        # Descrição muito curta
        if len(desc_clean) < 3:
            return False
        
        # Valor inválido
        try:
            valor = float(valor_str)
            if valor <= 0 or valor > 1000000:
                return False
        except:
            return False
        
        return True
