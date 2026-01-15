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

Requisitos

Python 3.10+

Acesso ao BigQuery no projeto: carbide-crowbar-483718-i8

Permissão de leitura na view: restaurante.fato_pedidos

Instale dependências:

pip install -r requirements.txt

Autenticação (Google Cloud / BigQuery)

⚠️ Credenciais NÃO são versionadas no GitHub.

Opção recomendada (ADC via gcloud)

Instale o Google Cloud SDK

Rode:

gcloud auth application-default login
gcloud config set project carbide-crowbar-483718-i8

Alternativa (variável de ambiente com JSON)

Se você tiver um arquivo JSON local (fora do Git), defina:

PowerShell:

$env:GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\para\credentials.json"


CMD:

set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\para\credentials.json

Como Executar
1) Extração (01_extract)

Gera fato_pedidos.csv e fato_pedidos.parquet em 05_exports/.

cd 08_python/01_extract
python extract_fato_pedidos.py


Saídas esperadas:

08_python/05_exports/fato_pedidos.csv

08_python/05_exports/fato_pedidos.parquet

2) Transformação (02_transform)

Limpa, tipa campos e cria colunas derivadas (ex.: receita, ticket médio, etc.)

cd ../02_transform
python transform_fato_pedidos.py

3) EDA (03_eda)

Valida qualidade e gera insights (ex.: outliers, distribuição por categoria).

cd ../03_eda
python eda_fato_pedidos.py

4) Métricas (04_metrics)

Consolida métricas de negócio reutilizáveis (ex.: receita por categoria, top produtos).

cd ../04_metrics
python metrics.py

Transformações planejadas (02_transform)

Exemplos do que será aplicado:

Padronização de tipos (data_pedido como datetime)

Normalização de textos (categoria, status)

Criação de campos:

receita = quantidade * preco_unitario

ticket_medio = receita / pedidos (por dia)

itens_por_pedido = quantidade / pedidos (por dia)

Checagens de qualidade:

nulos / duplicados

ranges de preço e quantidade

Próximas Evoluções

Curva ABC de produtos (classificação por receita)

Recorrência de clientes (frequência e ticket)

Simulação de promoções (cenários “e se”)

Export final “camada ouro” para BI

Otimização de custo/consulta no BigQuery

Autor

Gustavo Carvalho
Analista de Dados / BI
Projeto desenvolvido para fins de estudo, prática profissional e portfólio.

