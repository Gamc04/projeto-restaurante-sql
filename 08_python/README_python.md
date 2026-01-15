# Pipeline Python (Pandas) – ETL & Métricas | Restaurante

Esta pasta contém a evolução do projeto para um **pipeline de dados em Python**, com foco em:
- Extração de dados do BigQuery (view `fato_pedidos`)
- Transformação e limpeza com Pandas
- EDA (análise exploratória)
- Métricas de negócio reutilizáveis
- Exports (CSV/Parquet) para análises e integração com BI

> Objetivo: demonstrar competências em **Python para Dados**, boas práticas de organização e construção de uma camada analítica.

---

## Arquitetura do Pipeline

BigQuery (view `restaurante.fato_pedidos`)  
→ 01_extract (download em CSV/Parquet)  
→ 02_transform (tratamento e enriquecimento)  
→ 03_eda (insights e validações)  
→ 04_metrics (métricas consolidadas)  
→ 05_exports (arquivos finais)

---

## Estrutura de Pastas

text
08_python/
├── 01_extract/      # Extrai dados do BigQuery (fato_pedidos)
├── 02_transform/    # Limpeza, tipagem e enriquecimento (Pandas)
├── 03_eda/          # Análises exploratórias e validações
├── 04_metrics/      # Métricas de negócio (funções/rotinas)
├── 05_exports/      # Saídas: CSV/Parquet
├── requirements.txt # Dependências do projeto
└── README_python.md
