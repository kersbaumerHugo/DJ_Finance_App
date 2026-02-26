import os
import sys
import django
from pathlib import Path

# Adicionar o diretório backend ao Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def pytest_configure():
    """
    Configura o Django antes de rodar os testes
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        django.setup()
    except Exception as e:
        print(f"Erro ao configurar Django: {e}")
        raise
