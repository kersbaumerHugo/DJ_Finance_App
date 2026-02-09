A ideia é que os módulos sejam modulares e definidos de forma a permitir rodar testes unitários para cada parte do sistema.

Dessa forma temos a seguinte estrutura:

# Arquitetura do Projeto — DJ Finance App

Este documento descreve a arquitetura do *DJ Finance App*, explicando a organização das pastas, o fluxo de dados e os motivos por trás de cada decisão estrutural.

O objetivo da arquitetura é garantir:
- separação clara de responsabilidades
- escalabilidade do frontend
- baixo acoplamento entre UI, dados e backend
- facilidade de manutenção e evolução do sistema

---

## 📐 Visão Geral da Arquitetura


┌──────────────────────────────┐
│          BACKEND             │
│        Django REST API       │
│                              │
│  ┌──────── Models ────────┐  │
│  │  Regras de negócio     │  │
│  │  Persistência          │  │
│  └─────────▲──────────────┘  │
│            │ JSON (HTTP)     │
└────────────┼─────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│                 FRONTEND                    │
│                Streamlit                    │
│                                             │
│  ┌──────────── services/ ───────────────┐   │
│  │ Comunicação com a API Django         │   │
│  │ (requests, auth, headers, erros)     │   │
│  └──────────────▲───────────────────────┘   │
│                 │                           │
│  ┌──────────── tables/base.py ──────────┐   │
│  │ Fonte única da verdade (DataFrame)   │   │
│  │ Normalização e cache de dados        │   │
│  └──────────────▲───────────────────────┘   │
│                 │                           │
│  ┌──────────── tables/views ────────────┐   │
│  │ Transformações e visões derivadas    │   │
│  │ (resumo, despesas, categorias, etc)  │   │
│  └──────────────▲───────────────────────┘   │
│                 │                           │
│  ┌──────────── pages/ ──────────────────┐   │
│  │ Camada de UI                         │   │
│  │ Tabelas, gráficos, inputs e ações    │   │
│  └──────────────▲───────────────────────┘   │
│                 │                           │
│  ┌──────────── state/ ──────────────────┐   │
│  │ Controle de sessão e cache local     │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────── utils/ ──────────────────┐   │
│  │ Funções auxiliares reutilizáveis     │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘