from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def verificar_lancamentos_recorrentes_startup(sender, **kwargs):
    """
    Verifica e gera lançamentos recorrentes automaticamente no startup
    """
    try:
        from core.models import Recorrencia, Lancamento
        from core.utils.data_utils import calcular_n_dia_util
        from decimal import Decimal
        
        hoje = timezone.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        # Verificar se já verificou hoje
        cache_key = f'recorrencias_verificadas_{hoje.date()}'
        from django.core.cache import cache
        
        if cache.get(cache_key):
            logger.info("✅ Lançamentos recorrentes já verificados hoje")
            return
        
        logger.info(f"🔄 Verificando lançamentos recorrentes para {mes_atual}/{ano_atual}...")
        
        recorrencias = Recorrencia.objects.filter(ativo=True)
        criados = 0
        
        for recorrencia in recorrencias:
            try:
                # Calcular data do lançamento
                if recorrencia.usa_dia_util:
                    data_lancamento = calcular_n_dia_util(mes_atual, ano_atual, recorrencia.dia_vencimento)
                else:
                    # Dia fixo (limitar a 28 para evitar erros em fevereiro)
                    dia = min(recorrencia.dia_vencimento, 28)
                    data_lancamento = datetime(ano_atual, mes_atual, dia)
                
                # Verificar se já existe
                ja_existe = Lancamento.objects.filter(
                    recorrencia_origem_id=recorrencia.id,
                    data__month=mes_atual,
                    data__year=ano_atual
                ).exists()
                
                if ja_existe:
                    continue
                
                # Criar apenas se a data já passou ou é hoje
                if data_lancamento.date() <= hoje.date():
                    Lancamento.objects.create(
                        descricao=recorrencia.descricao,
                        data=data_lancamento,
                        categoria=recorrencia.categoria,
                        tipo=recorrencia.tipo,
                        metodo_pagamento=recorrencia.metodo_pagamento,
                        valor=recorrencia.valor_padrao,
                        status_pagamento='PREVISIONADO',
                        is_recorrente=True,
                        recorrencia_origem_id=recorrencia.id,
                        origem='RECORRENCIA'
                    )
                    
                    criados += 1
                    logger.info(f"✅ Criado: {recorrencia.descricao} para {data_lancamento.strftime('%d/%m/%Y')}")
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar {recorrencia.descricao}: {str(e)}")
        
        # Também verificar o próximo mês se estivermos nos últimos 3 dias
        if hoje.day >= 28:
            proximo_mes = mes_atual + 1 if mes_atual < 12 else 1
            proximo_ano = ano_atual if mes_atual < 12 else ano_atual + 1
            
            logger.info(f"🔄 Pré-gerando lançamentos para {proximo_mes}/{proximo_ano}...")
            
            for recorrencia in recorrencias:
                try:
                    if recorrencia.usa_dia_util:
                        data_lancamento = calcular_n_dia_util(proximo_mes, proximo_ano, recorrencia.dia_vencimento)
                    else:
                        dia = min(recorrencia.dia_vencimento, 28)
                        data_lancamento = datetime(proximo_ano, proximo_mes, dia)
                    
                    ja_existe = Lancamento.objects.filter(
                        recorrencia_origem_id=recorrencia.id,
                        data__month=proximo_mes,
                        data__year=proximo_ano
                    ).exists()
                    
                    if not ja_existe:
                        Lancamento.objects.create(
                            descricao=recorrencia.descricao,
                            data=data_lancamento,
                            categoria=recorrencia.categoria,
                            tipo=recorrencia.tipo,
                            metodo_pagamento=recorrencia.metodo_pagamento,
                            valor=recorrencia.valor_padrao,
                            status_pagamento='PREVISIONADO',
                            is_recorrente=True,
                            recorrencia_origem_id=recorrencia.id,
                            origem='RECORRENCIA'
                        )
                        
                        criados += 1
                        logger.info(f"✅ Pré-criado: {recorrencia.descricao} para {data_lancamento.strftime('%d/%m/%Y')}")
                
                except Exception as e:
                    logger.error(f"❌ Erro ao pré-gerar {recorrencia.descricao}: {str(e)}")
        
        if criados > 0:
            logger.info(f"✅ {criados} lançamento(s) recorrente(s) criado(s)")
        
        # Marcar como verificado hoje (cache de 24h)
        cache.set(cache_key, True, 86400)
        
    except Exception as e:
        logger.error(f"❌ Erro na verificação automática: {str(e)}")
