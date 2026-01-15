🍽️ Projeto Restaurante – SQL, Python, BigQuery & BI

Este repositório apresenta um projeto completo de dados, simulando um ambiente real de Analytics / BI, desde a modelagem relacional em SQL até a construção de dashboards analíticos.

O projeto demonstra competências em:

SQL (modelagem, consultas, views e funções)

Python para dados (Pandas, ETL, métricas)

BigQuery (camada analítica / GOLD)

Looker Studio (visualização)

🎯 Objetivo do Projeto

Construir um pipeline analítico de ponta a ponta para um restaurante fictício, permitindo:

Estruturação e modelagem dos dados

Exploração e transformação dos dados

Criação de métricas de negócio reutilizáveis

Armazenamento analítico otimizado

Visualização clara para tomada de decisão

Projeto desenvolvido para estudo, prática profissional e portfólio.

🧱 Arquitetura Geral
Banco Relacional (SQL)
        ↓
BigQuery (view fato_pedidos)
        ↓
Python (Pandas)
  ├─ Extract
  ├─ Transform
  ├─ EDA
  ├─ Metrics
  ├─ Load
        ↓
BigQuery (Camada GOLD)
        ↓
Looker Studio (Dashboards)

🗂️ Estrutura do Repositório
projeto-restaurante-sql/
├── 01_modelagem/            
├── 02_manipulacao_dados/    
├── 03_consultas_basicas/    
├── 04_condicionais/         
├── 05_agregacoes/           
├── 06_joins/               
├── 07_views_e_funcoes/      
│
├── 08_python/               
│   ├── 01_extract/          
│   ├── 02_transform/        
│   ├── 03_eda/              
│   ├── 04_metrics/          
│   ├── 05_exports/          
│   ├── 06_load/             
│   ├── README_python.md     
│   └── requirements.txt
│
├── assets/                  # Imagens, prints e diagramas
├── .gitattributes
└── README.md                

🛢️ Camada SQL

A parte SQL do projeto cobre desde o básico até o avançado, com foco em clareza e progressão didática:

Modelagem de tabelas

Manipulação de dados

Consultas analíticas

Agregações

JOINs

Views e funções reutilizáveis

A view principal utilizada no pipeline é:

restaurante.fato_pedidos


Ela consolida todas as informações necessárias para análise.

🐍 Pipeline Python (08_python)

O pipeline Python é responsável por:

Extrair dados do BigQuery

Limpar, tipar e enriquecer os dados

Validar qualidade (EDA)

Gerar métricas de negócio

Exportar dados analíticos

Carregar a camada GOLD no BigQuery

📄 Documentação detalhada:
👉 08_python/README_python.md

📊 Métricas de Negócio (Camada GOLD)

As métricas são calculadas fora do BI, garantindo performance e consistência.

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

Essas tabelas são consumidas diretamente pelo BI.

📈 Visualização – Looker Studio

O Looker Studio se conecta exclusivamente à camada GOLD, garantindo:

Dashboards mais leves

Lógica centralizada fora do BI

Facilidade de manutenção e evolução

Exemplos de análises:

Receita ao longo do tempo

Performance por categoria

Produtos mais vendidos

Tendência de pedidos e ticket médio

🛠️ Tecnologias Utilizadas

SQL

Python (Pandas)

Google BigQuery

Looker Studio

Git & GitHub

✅ Boas Práticas Aplicadas

Separação entre SQL, Python e BI

Métricas fora do dashboard

Camada GOLD para consumo analítico

Tipagem explícita de dados

Pipeline reprodutível

Estrutura organizada e documentada

👤 Autor

Gustavo Carvalho
Analista de Dados / BI

Projeto desenvolvido para fins de aprendizado, prática profissional e portfólio, simulando um ambiente real de dados corporativos.
