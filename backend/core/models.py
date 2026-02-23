from django.db import models


class Lancamento(models.Model):
    """
    Modelo unificado para lançamentos financeiros (entradas e saídas)
    """
    
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]
    
    METODO_PAGAMENTO_CHOICES = [
        ('PIX', 'PIX'),
        ('CREDITO_NUBANK', 'Cartão Crédito Nubank'),
        ('CREDITO_BRB', 'Cartão Crédito BRB'),
        ('CREDITO_C&A', 'Cartão Crédito C&A'),
        ('CREDITO_MERCADO_PAGO', 'Cartão Crédito Mercado Pago'),
        ('PREVISIONADO', 'Previsionado'),
    ]
    
    descricao = models.CharField(
        max_length=255,
        verbose_name='Descrição'
    )
    
    data = models.DateField(
        verbose_name='Data'
    )
    
    categoria = models.CharField(
        max_length=100,
        verbose_name='Categoria'
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo',
        help_text='Entrada (receita) ou Saída (despesa)'
    )
    
    metodo_pagamento = models.CharField(
        max_length=50,
        choices=METODO_PAGAMENTO_CHOICES,
        verbose_name='Método de Pagamento',
        help_text='Como foi pago ou recebido'
    )
    
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    mes_referencia = models.IntegerField(
        null=True,
        blank=True,
        help_text="Mês de referência da fatura"
    )
    ano_referencia = models.IntegerField(
        null=True,
        blank=True,
        help_text="Ano de referência da fatura"
    )
    origem = models.CharField(
        max_length=10,
        default='MANUAL',
        choices=[
        ('MANUAL', 'Manual'),
        ('PDF', 'PDF'),
        ('CSV', 'CSV'),
    ])
    
    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        ordering = ['-data', '-created_at']
        indexes = [
            models.Index(fields=['tipo', 'data']),
            models.Index(fields=['categoria', 'tipo']),
        ]
    
    def __str__(self):
        tipo_symbol = "💵" if self.tipo == 'ENTRADA' else "💸"
        return f"{tipo_symbol} {self.descricao} - R$ {self.valor}"

   
class Faturas (models.Model):
   banco = models.CharField(max_length = 50)
   valor_inicial = models.DecimalField(max_digits=10,decimal_places=2)
   valor_atual = models.DecimalField(max_digits=10,decimal_places=2)
   pago = models.DecimalField(max_digits=10,decimal_places=2)
   diff = models.DecimalField(max_digits=10,decimal_places=2)
   vencimento = models.DateField()
   limite_total = models.DecimalField(max_digits=10,decimal_places=2)
   
class Investimentos (models.Model):
   banco = models.CharField(max_length = 50)
   ativo = models.CharField(max_length = 8)
   quantidade = models.IntegerField()
   valor_compra = models.DecimalField(max_digits=10,decimal_places=2)
   #Fazer request de algum lugar para pegar o restante dos valores
   

#Tabelas para criar
   #Investimentos
   #Bancos
