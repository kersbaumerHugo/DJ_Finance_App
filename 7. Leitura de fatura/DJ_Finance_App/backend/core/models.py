from django.db import models


class Lancamento (models.Model):
   descricao = models.CharField(max_length = 255)
   data = models.DateField()
   categoria = models.CharField(max_length = 255)
   status = models.CharField(max_length = 20)
   valor = models.DecimalField(max_digits=10,decimal_places=2)

   
