"""
Configurações centralizadas do aplicativo
"""

import os

# URL base da API
# Prioriza variável de ambiente, senão usa localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")
# Timeout padrão para requisições (em segundos)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
# Número de tentativas em caso de falha
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
# Configurações de desenvolvimento
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
