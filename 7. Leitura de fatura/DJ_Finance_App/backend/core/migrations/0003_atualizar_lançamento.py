from django.db import migrations, models

def migrar_status_para_tipo_e_metodo(apps, schema_editor):
    """
    Converte dados antigos para novo formato
    """
    Lancamento = apps.get_model('core', 'Lancamento')
    
    for lanc in Lancamento.objects.all():
        # Mapear status antigo para tipo novo
        if lanc.status == 'Receita':
            lanc.tipo = 'ENTRADA'
            lanc.metodo_pagamento = 'TRANSFERENCIA'  # Padrão
        elif lanc.status == 'Despesa':
            lanc.tipo = 'SAIDA'
            lanc.metodo_pagamento = 'PREVISIONADO'  # Padrão
        
        lanc.save()

class Migration(migrations.Migration):
  dependencies = [
        ('core', '0002_investimentos_faturas_limite_total_and_more'),
    ]
  operations = [
        # Adicionar novos campos
        migrations.AddField(
            model_name='lancamento',
            name='tipo',
            field=models.CharField(
                max_length=20,
                choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')],
                default='SAIDA'
            ),
        ),
        migrations.AddField(
            model_name='lancamento',
            name='metodo_pagamento',
            field=models.CharField(
                max_length=50,
                default='PREVISIONADO'
            ),
        ),
        
        # Migrar dados
        migrations.RunPython(migrar_status_para_tipo_e_metodo),
        
        # Remover campo antigo (opcional)
        # migrations.RemoveField(
        #     model_name='lancamento',
        #     name='status',
        # ),
    ]
