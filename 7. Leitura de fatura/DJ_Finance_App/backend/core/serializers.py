from rest_framework import serializers
from .models import Lancamento

class LancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = [
            'id',
            'descricao',
            'data',
            'categoria',
            'tipo',
            'metodo_pagamento',
            'valor',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_valor(self, value):
        """Valida se o valor é positivo"""
        if value <= 0:
            raise serializers.ValidationError("Valor deve ser maior que zero")
        return value
    
    def validate_data(self, value):
        """Valida se a data não é futura"""
        if value > date.today():
            raise serializers.ValidationError("Data não pode ser no futuro")
        return value
