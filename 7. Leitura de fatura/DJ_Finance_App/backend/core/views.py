from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from 

@api_view(['GET'])
def resumo(request):
   data = {
      'faturamento' : 128450,
      'usuarios': 342,
      'mes': 'Janeiro'
      }
   return Response(data)   
@api_view(["POST"])
def criar_lancamento(request):
    serializer = LancamentoSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["PUT"])
def atualizar_lancamento(request, pk):
    lancamento = Lancamento.objects.get(pk=pk)
    serializer = LancamentoSerializer(lancamento, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
