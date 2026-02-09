from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LancamentoSerializer
from .models import Lancamento
import pandas as pd


##Faturas---------------#

@api_view(['GET'])
def resumo(request):
   data = {
      'faturamento' : 128450,
      'usuarios': 342,
      'mes': 'Janeiro'
      }
   return Response(data)   

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
