"""Transformações de DataFrames"""
import pandas as pd
from typing import List, Dict
def processar_evolucao_diaria(dados: List[Dict]) -> pd.DataFrame:
    """
    Converte dados de evolução para DataFrame
    
    Args:
        dados: Lista de dicionários com evolução diária
        
    Returns:
        DataFrame processado
    """
    if not dados:
        return pd.DataFrame()
    
    df = pd.DataFrame(dados)
    df['data'] = pd.to_datetime(df['data'])
    return df.sort_values('data')
