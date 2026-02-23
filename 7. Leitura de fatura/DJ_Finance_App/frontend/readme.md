# 💰 DJ Finance App - Frontend

Interface web desenvolvida com **Streamlit** para gestão financeira pessoal.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![Plotly](https://img.shields.io/badge/Plotly-6.5-purple)

---

## 📐 Arquitetura Frontend

O frontend segue os princípios de **separação de responsabilidades** e **modularização** para garantir manutenibilidade e escalabilidade.
frontend/
├── config/                 # Configurações centralizadas
│   ├── __init__.py
│   └── settings.py        # Variáveis de ambiente (API_BASE_URL, timeouts)
│
├── services/              # Camada de comunicação com API
│   ├── __init__.py
│   └── api.py            # Funções HTTP (GET, POST, PUT, DELETE)
│
├── components/            # Componentes reutilizáveis de UI
│   ├── __init__.py
│   ├── metrics.py        # Cards de métricas (receitas, despesas, saldo)
│   ├── graphs.py         # Gráficos Plotly (gauge, linha, pizza, barras)
│   ├── layouts.py        # Layouts complexos (interpretação de saúde)
│   └── tables.py         # Tabelas editáveis e estilizadas
│
├── tables/                # Transformações de DataFrames
│   ├── __init__.py
│   ├── tables.py         # Formatação de tabelas (base_table, financial_table)
│   └── transformers.py   # Processamento de dados (processar_evolucao_diaria)
│
├── pages/                 # Páginas do aplicativo (apenas orquestração)
│   ├── 1_Resumo.py       # Dashboard principal com analytics
│   ├── 2_Editar_Lancamentos.py  # Edição mensal de entradas/saídas
│   ├── 3_Investimentos.py       # Gestão de investimentos
│   └── 20_Lançamento.py         # CRUD de lançamentos
│
├── tests/                 # Testes automatizados
│   ├── conftest.py       # Fixtures compartilhadas
│   ├── unit/             # Testes unitários
│   │   ├── test_api.py
│   │   ├── test_components.py
│   │   ├── test_graphs.py
│   │   └── test_transformers.py
│   └── integration/      # Testes de integração
│       └── test_analytics_flow.py
│
├── Hub.py                # Página inicial (navegação)
├── requirements.txt      # Dependências Python
└── pytest.ini           # Configuração de testes

## 🎯 Princípios de Design
### 1. Separação de Responsabilidades
ERRADO - Lógica misturada:
def dashboard():
    data = requests.get("http://api.com/data").json()
    total = sum([x['valor'] for x in data])
    st.metric("Total", total)
CORRETO - Separação clara:
from services.api import get_analytics_financeiro
from components.metrics import metric_card
def dashboard():
    analytics = get_analytics_financeiro()
    metric_card("Total", analytics['total'])
### 2. Componentes Reutilizáveis
Cada componente em components/ é independente e testável:
def metric_card(label, value, icon=""):
    st.metric(f"{icon} {label}", value)
metric_card("Receitas", "R$ 10.000", "💵")
metric_card("Despesas", "R$ 6.000", "💸")
### 3. Pages como Orquestradores
As páginas em pages/ NÃO devem ter lógica de negócio.
Apenas orquestram componentes e serviços.

## 🔌 Comunicação com Backend

### Camada de Serviço (services/api.py)

Todas as chamadas HTTP são centralizadas e tratam erros:

class APIException(Exception):
    pass

def get_analytics_financeiro(mes=None, ano=None):
    try:
        url = f"{API_BASE_URL}/analytics/"
        response = requests.get(url, params={'mes': mes, 'ano': ano})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        _handle_request_error(e, "buscar analytics")

### Configuração (config/settings.py)

import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

## 🚀 Como Executar

### Pré-requisitos
- Python >= 3.12
- pip >= 23.0

### Instalação

1. Criar ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

2. Instalar dependências:
pip install -r requirements.txt

### Executar Aplicação

1. Certifique-se que o backend está rodando em http://localhost:8000

2. Rodar Streamlit:
streamlit run Hub.py

### Configurar Variáveis de Ambiente

Linux/Mac:
export API_BASE_URL=http://localhost:8000/api
export REQUEST_TIMEOUT=30

Windows:
set API_BASE_URL=http://localhost:8000/api
set REQUEST_TIMEOUT=30

## 📦 Dependências Principais

| Biblioteca | Versão | Propósito |
|-----------|--------|-----------|
| streamlit | 1.54.0 | Framework web |
| pandas | 2.3.3 | Manipulação de dados |
| plotly | 6.5.2 | Visualizações interativas |
| requests | 2.32.5 | Requisições HTTP |
| pytest | 9.0.2 | Testes automatizados |
| black | 26.1.0 | Formatação de código |

## 🧪 Testes

Executar todos os testes:
pytest tests/ -v

Apenas unitários:
pytest tests/unit/ -v

Com cobertura:
pytest --cov=services --cov=components --cov-report=html

## 🎨 Padrões de Código

### Convenções
- Arquivos: snake_case.py
- Classes: PascalCase
- Funções: snake_case()
- Constantes: UPPER_CASE
- Type hints: Sempre que possível

Exemplo:
def processar_dados(dados: List[Dict]) -> pd.DataFrame:
    """
    Processa lista de dicionários em DataFrame
    
    Args:
        dados: Lista de dicionários com dados brutos
        
    Returns:
        DataFrame processado e limpo
    """
    return pd.DataFrame(dados)

### Formatação

Formatar código:
black frontend/

Verificar estilo:
flake8 frontend/

Analisar código:
pylint frontend/services/

## 🤝 Contribuindo

1. Crie uma branch: git checkout -b feature/nova-funcionalidade
2. Implemente mudanças seguindo os padrões
3. Adicione testes: tests/unit/test_nova_funcionalidade.py
4. Rode testes: pytest tests/ -v
5. Formate código: black frontend/
6. Commit: git commit -m "feat: adiciona nova funcionalidade"
7. Push: git push origin feature/nova-funcionalidade

## 📞 Suporte

Documentação Streamlit: https://docs.streamlit.io
Documentação Plotly: https://plotly.com/python/

## 📄 Licença

Este projeto é de uso pessoal.
