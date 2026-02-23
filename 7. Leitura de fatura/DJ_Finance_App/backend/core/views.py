from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LancamentoSerializer
from .services import AnalyticsService
from .models import Lancamento
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from core.parsers.fatura_parser import FaturaProcessor
import os

def converter_para_json(obj):
    """Converte objetos não serializáveis para JSON"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj
@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_fatura(request):
    """
    Endpoint para upload e processamento de faturas
    """
    try:
        # Validar arquivo
        if 'file' not in request.FILES:
            return Response({
                'error': 'Nenhum arquivo enviado'
            }, status=400)
        
        file = request.FILES['file']
        banco = request.data.get('banco', None)
        
        print(f"📄 Arquivo recebido: {file.name} ({file.size} bytes)")
        print(f"🏦 Banco: {banco}")
        
        # Salvar arquivo temporariamente
        file_path = default_storage.save(f'temp/{file.name}', file)
        full_path = default_storage.path(file_path)
        
        print(f"💾 Salvo em: {full_path}")
        
        try:
            # Processar fatura
            resultado = FaturaProcessor.process_fatura(full_path, banco)
            
            print(f"✅ Processado: {resultado['total_transacoes']} transações")
            
            # ✅ CONVERTER valores não serializáveis
            transacoes_serializaveis = []
            for t in resultado['transacoes']:
                # ✅ Garantir que a data está no formato YYYY-MM-DD (sem hora)
                data_str = str(t['data'])
                if ' ' in data_str:  # Se tem hora, remover
                    data_str = data_str.split(' ')[0]
                
                transacoes_serializaveis.append({
                    'data': data_str,  # Apenas YYYY-MM-DD
                    'descricao': str(t['descricao']),
                    'categoria': str(t['categoria']),
                    'valor': float(t['valor']),
                    'tipo': str(t.get('tipo', 'SAIDA')),
                    'metodo_pagamento': str(t.get('metodo_pagamento', 'CREDITO_NUBANK'))
                })
            resposta = {
                'success': True,
                'banco': str(resultado['banco']),
                'total_transacoes': int(resultado['total_transacoes']),
                'valor_total': float(resultado['valor_total']),
                'transacoes': transacoes_serializaveis
            }
            
            print(f"📤 Enviando resposta com {len(transacoes_serializaveis)} transações")
            
            return Response(resposta, status=200)
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"🗑️ Arquivo temporário removido")
    
    except ValueError as e:
        print(f"⚠️ ValueError: {str(e)}")
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Erro ao processar fatura: {str(e)}'}, status=500)


@csrf_exempt  # ✅ ADICIONAR esta linha também
@api_view(['POST'])
def importar_fatura(request):
    """
    Endpoint para importar transações processadas
    """
    try:
        transacoes = request.data.get('transacoes', [])
        
        if not transacoes:
            return Response({'error': 'Nenhuma transação fornecida'}, status=400)
        
        # Importar
        resultado = FaturaProcessor.import_transacoes(transacoes)
        
        return Response({
            'success': True,
            **resultado
        })
        
    except Exception as e:
        print(f"❌ Erro na importação: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def analytics_financeiro(request):
    """
    Endpoint de analytics - Apenas orquestra o serviço
    """
    try:
        # Filtros
        mes = request.GET.get('mes', None)
        ano = request.GET.get('ano', None)
        
        # Queryset
        qs = Lancamento.objects.all()
        if mes and ano:
            qs = qs.filter(data__month=mes, data__year=ano)
        elif ano:
            qs = qs.filter(data__year=ano)
        
        # ✅ Delegar para camada de serviço
        service = AnalyticsService()
        
        resumo = service.calcular_resumo(qs)
        saude = service.calcular_saude_financeira(
            resumo['receitas_total'],
            resumo['despesas_total']
        )
        evolucao = service.calcular_evolucao_diaria(qs)
        gastos = service.analisar_por_categoria(
            qs, 'Despesa', resumo['despesas_total']
        )
        receitas = service.analisar_por_categoria(
            qs, 'Receita', resumo['receitas_total']
        )
        detalhamento = service.detalhar_entradas_saidas(qs)
        return Response({
            'resumo': resumo,
            'saude_financeira': saude,
            'evolucao_diaria': evolucao,
            'gastos_por_categoria': gastos,
            'receitas_por_categoria': receitas,
            'detalhamento': detalhamento
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

#LIST+CREATE
@api_view(["GET", "POST"])
def lancamentos(request):
    if request.method == "GET":
        qs = Lancamento.objects.all()
        return Response(LancamentoSerializer(qs, many=True).data)

    serializer = LancamentoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

#UPDATE+DELETE
@api_view(["PUT", "DELETE"])
def lancamento_detail(request, pk):
    lanc = Lancamento.objects.get(pk=pk)

    if request.method == "PUT":
        serializer = LancamentoSerializer(lanc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    lanc.delete()
    return Response(status=204)

@api_view(['GET'])
def meses(request):
   if request.method == "GET":
      qs = pd.DataFrame.from_records(Lancamento.objects.all().values())
      print(qs)
      data = {
      'index' : ["Month","Year"],
      0: ["Janeiro","2026"],
      1: ['Dezembro',"2025"],
      2: ["Novembro","2025"]
      }
      return Response(data)
   
   return Response(status=400)  

##
