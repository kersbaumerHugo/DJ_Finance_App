from django.db import models


class Lancamento (models.Model):
   descricao = models.CharField(max_length = 255)
   data = models.DateField()
   categoria = models.CharField(max_length = 255)
   status = models.CharField(max_length = 20)
   valor = models.DecimalField(max_digits=10,decimal_places=2)

   
class Faturas (models.Model):
   banco = models.CharField(max_length = 50)
   valor_inicial = models.DecimalField(max_digits=10,decimal_places=2)
   valor_atual = models.DecimalField(max_digits=10,decimal_places=2)
   pago = models.DecimalField(max_digits=10,decimal_places=2)
   diff = models.DecimalField(max_digits=10,decimal_places=2)
   
class Investimentos (models.Model):
   banco = models.CharField(max_length = 50)
   ativo = models.CharField(max_length = 8)
   quantidade = models.IntegerField()
   valor_compra = models.DecimalField(max_digits=10,decimal_places=2)
   #Fazer request de algum lugar para pegar o restante dos valores
   

#Tabelas para criar
   #Investimentos
   #Bancos
