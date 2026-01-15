🐍 Pipeline Python (Pandas) – ETL & Métricas | Restaurante

Este diretório contém a implementação de um pipeline analítico em Python, responsável por extrair, transformar, consolidar métricas e exportar dados para consumo no BigQuery e visualização no Looker Studio.

O projeto foi estruturado seguindo boas práticas de engenharia analítica, com separação clara entre RAW → MÉTRICAS → GOLD.

🎯 Objetivo: demonstrar domínio em Python para Dados, organização de pipelines, geração de métricas fora do BI e integração com BigQuery + Looker Studio.

🧱 Arquitetura do Pipeline
BigQuery (view restaurante.fato_pedidos)
        ↓
01_extract   → extração dos dados (CSV / Parquet)
        ↓
02_transform → limpeza, tipagem e enriquecimento
        ↓
03_eda       → validações e análise exploratória
        ↓
04_metrics   → KPIs de negócio (diários, mensais, gerais)
        ↓
05_exports   → arquivos finais (camada GOLD)
        ↓
06_load      → carga no BigQuery (tabelas analíticas)
        ↓
Looker Studio → dashboards

📁 Estrutura de Pastas
08_python/
├── 01_extract/        # Extração de dados do BigQuery
├── 02_transform/      # Limpeza, tipagem e enriquecimento
├── 03_eda/            # Análise exploratória e validações
├── 04_metrics/        # Cálculo de métricas de negócio
├── 05_exports/        # Saídas finais (CSV / Parquet)
├── 06_load/           # Carga das métricas no BigQuery
├── requirements.txt   # Dependências do projeto
└── README_python.md   # Documentação do pipeline

🧮 Métricas Geradas (Camada GOLD)

As métricas são calculadas em Python, não no BI.

KPIs Gerais

Faturamento total

Total de pedidos

Ticket médio

Quantidade total de itens

KPIs Diários

Faturamento diário

Pedidos diários

Ticket médio diário

KPIs Mensais

Faturamento mensal

Pedidos mensais

Ticket médio mensal

Essas métricas são exportadas em CSV e carregadas no BigQuery, sendo consumidas via views GOLD no Looker Studio.

🛠️ Requisitos

Python 3.10+

Conta Google com acesso ao BigQuery

Projeto: carbide-crowbar-483718-i8

Permissão de leitura na view:

restaurante.fato_pedidos


Instalação das dependências:

pip install -r requirements.txt

🔐 Autenticação com BigQuery

⚠️ Credenciais NÃO são versionadas no GitHub

Opção recomendada (ADC via gcloud)
gcloud auth application-default login
gcloud config set project carbide-crowbar-483718-i8

Alternativa (JSON local – fora do Git)

PowerShell

$env:GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\para\credentials.json"


CMD

set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\para\credentials.json

▶️ Como Executar o Pipeline
1️⃣ Extração

Extrai os dados da view fato_pedidos:

cd 08_python/01_extract
python extract_fato_pedidos.py


Saídas

05_exports/fato_pedidos.csv
05_exports/fato_pedidos.parquet

2️⃣ Transformação

Limpeza e enriquecimento dos dados:

cd ../02_transform
python transform_fato_pedidos.py


Inclui:

Tipagem correta de datas

Normalização de textos

Criação de colunas derivadas

3️⃣ EDA (Análise Exploratória)
cd ../03_eda
python eda_fato_pedidos.py


Valida:

Nulos e duplicados

Distribuições

Outliers

Consistência das métricas

4️⃣ Métricas
cd ../04_metrics
python metrics_fato_pedidos.py


Gera:

kpis_gerais.csv

kpis_diarios.csv

kpis_mensais.csv

5️⃣ Load no BigQuery
cd ../06_load
python load_kpis_bigquery.py


Resultado:

Tabelas analíticas criadas no dataset restaurante

Prontas para consumo no Looker Studio

📊 Visualização (Looker Studio)

O Looker Studio se conecta exclusivamente às tabelas / views GOLD no BigQuery.

Nenhuma lógica de negócio é implementada no BI.

🚀 Boas Práticas Aplicadas

Métricas fora do BI

Separação RAW / GOLD

Tipagem explícita

Pipeline reproduzível

Código modular e legível

Documentação clara

👤 Autor

Gustavo Carvalho
Analista de Dados / BI

Projeto desenvolvido para estudo, prática profissional e portfólio, simulando um pipeline real de dados usado em ambientes corporativos.
