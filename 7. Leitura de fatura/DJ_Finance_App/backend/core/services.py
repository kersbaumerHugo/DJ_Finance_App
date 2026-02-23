"""
Camada de serviço - Lógica de negócio separada das views
"""
from django.db.models import Sum, Count
from .models import Lancamento
import pandas as pd
from typing import Dict, Any, List


class AnalyticsService:
    """Serviço de análise financeira"""
    
    @staticmethod
    def calcular_resumo(queryset) -> Dict[str, float]:
        """Calcula resumo básico de receitas e despesas"""
        # ✅ CORRIGIR: status → tipo
        receitas = queryset.filter(tipo='ENTRADA').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        despesas = queryset.filter(tipo='SAIDA').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        receitas_float = float(receitas) if receitas else 0.0
        despesas_float = float(despesas) if despesas else 0.0
        
        return {
            'receitas_total': float(receitas),
            'despesas_total': float(despesas),
            'saldo': float(receitas - despesas),
            'quantidade_transacoes': queryset.count()
        }
    
    
    @staticmethod
    def calcular_saude_financeira(receitas: float, despesas: float) -> Dict[str, Any]:
        """Calcula indicadores de saúde financeira"""
        saldo = receitas - despesas
        
        if receitas > 0:
            taxa_poupanca = (saldo / receitas) * 100
            percentual_gastos = (despesas / receitas) * 100
        else:
            taxa_poupanca = 0
            percentual_gastos = 0
        
        # Classificação
        if taxa_poupanca >= 20:
            status, cor, score = "Excelente", "green", 90
        elif taxa_poupanca >= 10:
            status, cor, score = "Boa", "blue", 70
        elif taxa_poupanca >= 0:
            status, cor, score = "Atenção", "orange", 50
        else:
            status, cor, score = "Crítica", "red", 30
        
        return {
            'score': round(score, 1),
            'status': status,
            'cor': cor,
            'taxa_poupanca': round(taxa_poupanca, 2),
            'percentual_gastos': round(percentual_gastos, 2)
        }
    
    @staticmethod
    def calcular_evolucao_diaria(queryset) -> List[Dict[str, Any]]:
        """Calcula evolução diária do saldo"""
        df = pd.DataFrame.from_records(
            queryset.values('data', 'valor', 'tipo')
        )
        
        if df.empty:
            return []
        
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values('data')
        
        evolucao = []
        date_range = pd.date_range(df['data'].min(), df['data'].max())
        saldo_acumulado = 0
        
        for date in date_range:
            transacoes_dia = df[df['data'] == date]
            receitas_dia = transacoes_dia[
                transacoes_dia['tipo'] == 'ENTRADA'
            ]['valor'].sum()
            despesas_dia = transacoes_dia[
                transacoes_dia['tipo'] == 'SAIDA'
            ]['valor'].sum()
            
            saldo_acumulado += (receitas_dia - despesas_dia)
            
            evolucao.append({
                'data': date.strftime('%Y-%m-%d'),
                'saldo_acumulado': float(saldo_acumulado),
                'receitas_dia': float(receitas_dia),
                'despesas_dia': float(despesas_dia),
                'saldo_dia': float(receitas_dia - despesas_dia)
            })
        
        return evolucao
    
    @staticmethod
    def analisar_por_categoria(queryset, tipo_lancamento: str, total: float) -> List[Dict]:
        """Analisa gastos ou receitas por categoria"""
        # ✅ CORRIGIR: Mapear tipo antigo para novo
        tipo_filtro = 'SAIDA' if tipo_lancamento == 'Despesa' else 'ENTRADA'
        
        categorias = []
        
        for cat in queryset.filter(tipo=tipo_filtro).values('categoria').annotate(
            total=Sum('valor'),
            count=Count('id')
        ).order_by('-total'):
            cat_total = float(cat['total']) if cat['total'] else 0.0
            percentual = (cat_total / total * 100) if total > 0 else 0
            
            categorias.append({
                'categoria': cat['categoria'],
                'total': cat_total,
                'count': cat['count'],
                'percentual': round(percentual, 2)
            })
        
        return categorias
    
    @staticmethod
    def detalhar_entradas_saidas(queryset) -> Dict[str, Any]:
        """
        Detalha entradas e saídas com TODOS os campos necessários
        """
        # ✅ CORRIGIR: status → tipo
        # Entradas (Receitas)
        receitas = []
        for lanc in queryset.filter(tipo='ENTRADA').values(
            'id', 'descricao', 'data', 'categoria', 'tipo', 'metodo_pagamento', 'valor'
        ).order_by('data'):
            receitas.append({
                'id': lanc['id'],
                'especificacao': lanc['descricao'],
                'data': lanc['data'].strftime('%Y-%m-%d'),
                'categoria': lanc['categoria'],
                'metodo_pagamento': lanc['metodo_pagamento'],
                'custo': float(lanc['valor']) if lanc['valor'] else 0.0
            })
        
        # Saídas (Despesas)
        despesas = []
        for lanc in queryset.filter(tipo='SAIDA').values(
            'id', 'descricao', 'data', 'categoria', 'tipo', 'metodo_pagamento', 'valor'
        ).order_by('data'):
            despesas.append({
                'id': lanc['id'],
                'especificacao': lanc['descricao'],
                'data': lanc['data'].strftime('%Y-%m-%d'),
                'categoria': lanc['categoria'],
                'metodo_pagamento': lanc['metodo_pagamento'],
                'custo': float(lanc['valor']) if lanc['valor'] else 0.0
            })
        
        # Totais
        total_entradas = sum(r['custo'] for r in receitas)
        total_saidas = sum(d['custo'] for d in despesas)
        
        return {
            'entradas': receitas,
            'saidas': despesas,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'saldo_previsto': total_entradas - total_saidas
        }
