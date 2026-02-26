from datetime import datetime, timedelta
import holidays

# Feriados brasileiros
feriados_brasil = holidays.Brazil()

def eh_dia_util(data: datetime) -> bool:
    """
    Verifica se uma data é dia útil usando a biblioteca holidays
    """
    # Sábado = 5, Domingo = 6
    if data.weekday() >= 5:
        return False
    
    # Verificar feriados brasileiros
    if data in feriados_brasil:
        return False
    
    return True

def calcular_n_dia_util(mes: int, ano: int, n: int) -> datetime:
    """
    Calcula o N-ésimo dia útil do mês
    
    Args:
        mes: Mês (1-12)
        ano: Ano
        n: Número do dia útil (1=primeiro, 5=quinto)
    
    Returns:
        Data do N-ésimo dia útil
    """
    data = datetime(ano, mes, 1)
    dias_uteis_contados = 0
    
    # Limite de segurança (máximo 50 dias)
    max_dias = 50
    dias_percorridos = 0
    
    while dias_uteis_contados < n and dias_percorridos < max_dias:
        if eh_dia_util(data):
            dias_uteis_contados += 1
            if dias_uteis_contados == n:
                return data
        
        data += timedelta(days=1)
        dias_percorridos += 1
        
        # Se passou para o próximo mês, erro
        if data.month != mes:
            raise ValueError(f"Não há {n} dias úteis no mês {mes}/{ano}")
    
    if dias_percorridos >= max_dias:
        raise ValueError(f"Limite de dias excedido ao buscar {n}º dia útil")
    
    return data

def proximo_dia_util(data: datetime) -> datetime:
    """
    Retorna o próximo dia útil a partir de uma data
    """
    proxima = data + timedelta(days=1)
    tentativas = 0
    
    while not eh_dia_util(proxima) and tentativas < 30:
        proxima += timedelta(days=1)
        tentativas += 1
    
    return proxima
