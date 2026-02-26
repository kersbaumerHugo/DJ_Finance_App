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
    STATUS_PAGAMENTO_CHOICES = [
        ('PAGO', 'Pago'),
        ('PREVISIONADO', 'Previsionado'),
        ('PENDENTE', 'Pendente'),
    ]
    
    status_pagamento = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO_CHOICES,
        default='PAGO',
        help_text='Status do pagamento'
    )
    
    is_recorrente = models.BooleanField(
        default=False,
        help_text='Se este lançamento foi criado por uma recorrência'
    )
    
    recorrencia_origem_id = models.IntegerField(
        null=True, 
        blank=True,
        help_text='ID da recorrência que gerou este lançamento'
    )
    
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
    
class Recorrencia(models.Model):
    """
    Model para gerenciar lançamentos recorrentes (salários, assinaturas, etc)
    """
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]
    
    descricao = models.CharField(max_length=200, help_text='Ex: Salário Hugo, YouTube Premium')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=50)
    valor_padrao = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Valor padrão (pode ser ajustado manualmente após criação)'
    )
    dia_vencimento = models.IntegerField(
        help_text='Dia do mês (1-31). Use 5 para "5º dia útil"'
    )
    metodo_pagamento = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)
    
    # Flag especial para dia útil
    usa_dia_util = models.BooleanField(
        default=False,
        help_text='Se True, considera dia_vencimento como "Xº dia útil"'
    )
    
    # Matching para baixa automática
    palavras_chave_matching = models.CharField(
        max_length=200,
        blank=True,
        help_text='Palavras para identificar na fatura (separadas por vírgula). Ex: "youtube,premium"'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recorrencias'
        verbose_name = 'Recorrência'
        verbose_name_plural = 'Recorrências'
        ordering = ['dia_vencimento', 'descricao']
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor_padrao} (Dia {self.dia_vencimento})"
   
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
