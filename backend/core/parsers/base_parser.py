"""
Parser base abstrato para processamento de faturas
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd


class BaseParser(ABC):
    """Classe base para todos os parsers de fatura"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.banco = self.__class__.__name__.replace('Parser', '')
    
    @abstractmethod
    def extract_data(self) -> pd.DataFrame:
        """
        Extrai dados do arquivo e retorna DataFrame padronizado
        
        Returns:
            DataFrame com colunas: [data, descricao, categoria, valor, metodo_pagamento]
        """
        pass
    
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza DataFrame para o formato padrão do sistema
        
        Args:
            df: DataFrame bruto extraído
            
        Returns:
            DataFrame normalizado
        """
        # Garantir colunas obrigatórias
        required_columns = ['data', 'descricao', 'valor']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna obrigatória '{col}' não encontrada")
        
        # Converter data para datetime
        df['data'] = pd.to_datetime(df['data'])
        
        # Garantir valor como float
        df['valor'] = df['valor'].astype(float)
        
        # Preencher campos opcionais
        if 'categoria' not in df.columns:
            df['categoria'] = 'Não categorizado'
        
        if 'metodo_pagamento' not in df.columns:
            df['metodo_pagamento'] = f'CREDITO_{self.banco.upper()}'
        
        # Adicionar tipo (SAIDA para faturas)
        df['tipo'] = 'SAIDA'
        
        return df
    
    def categorizar_automatico(self, descricao: str) -> str:
        """
        Categoriza transação baseado em palavras-chave
        
        Args:
            descricao: Descrição da transação
            
        Returns:
            Categoria sugerida
        """
        descricao_lower = descricao.lower()
        
        categorias_keywords = {
            'Alimentação': ['mercado', 'supermercado', 'padaria', 'restaurante', 'lanche', 'ifood', 'uber eats'],
            'Transporte': ['uber', '99', 'gasolina', 'posto', 'combustivel', 'estacionamento'],
            'Saúde': ['farmacia', 'droga', 'hospital', 'clinica', 'medico', 'laboratorio'],
            'Moradia': ['aluguel', 'condominio', 'energia', 'agua', 'internet', 'telefone'],
            'Lazer': ['cinema', 'streaming', 'netflix', 'spotify', 'jogo', 'playstation'],
            'Educação': ['livro', 'curso', 'escola', 'faculdade', 'udemy'],
        }
        
        for categoria, keywords in categorias_keywords.items():
            for keyword in keywords:
                if keyword in descricao_lower:
                    return categoria
        
        return 'Outros'
    
    def process_file(self) -> List[Dict[str, Any]]:
        """
        Pipeline completo de processamento
        
        Returns:
            Lista de dicionários prontos para importação
        """
        # Extrair dados
        df = self.extract_data()
        
        # Normalizar
        df = self.normalize_data(df)
        
        # Categorizar automaticamente se não estiver categorizado
        df['categoria'] = df.apply(
            lambda row: self.categorizar_automatico(row['descricao']) 
            if row['categoria'] == 'Não categorizado' 
            else row['categoria'],
            axis=1
        )
        
        # Converter para lista de dicts
        return df.to_dict('records')
