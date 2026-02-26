from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Executado quando o Django inicia
        Verifica e gera lançamentos recorrentes automaticamente
        """
        # Importar aqui para evitar erros de importação circular
        from core.signals import verificar_lancamentos_recorrentes_startup
        
        # Registrar verificação automática
        import sys
        
        # Executar apenas se não for comando de migração
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            from django.db.models.signals import post_migrate
            post_migrate.connect(verificar_lancamentos_recorrentes_startup, sender=self)
