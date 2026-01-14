🍽️ Projeto Restaurante – SQL | Análise de Dados & BI

Este projeto simula o banco de dados e a operação analítica de um restaurante, desenvolvido com foco em modelagem relacional, manipulação de dados, análise SQL e Business Intelligence.

O objetivo é demonstrar competências em SQL aplicado a cenários reais, organização de dados e construção de métricas de negócio que geram insights relevantes para análise de dados e apoio à tomada de decisão.

🎯 Objetivos do Projeto

Simular um ambiente real de dados de um restaurante

Aplicar boas práticas de modelagem relacional

Desenvolver consultas SQL para análise exploratória e analítica

Criar métricas de negócio utilizadas em BI

Estruturar dados para visualização em dashboards

🏗️ Arquitetura do Projeto
MySQL (dados transacionais)
        ↓
BigQuery (camada analítica e views)
        ↓
Looker Studio (dashboards interativos)

🗄️ Modelagem do Banco de Dados

O banco de dados restaurante foi modelado para representar operações reais do negócio, incluindo as seguintes entidades:

Clientes

Funcionários

Produtos

Pedidos

Informações adicionais de produtos

Conceitos aplicados

Chaves primárias e estrangeiras

Integridade referencial

Tipos de dados adequados

Relacionamentos entre tabelas

Organização orientada à performance e legibilidade

📁 Organização do Repositório
01_modelagem           → Criação das tabelas e estrutura do banco
02_manipulacao_dados   → Inserts, updates e ajustes de dados
03_consultas_basicas   → Consultas SQL simples
04_condicionais        → Condições, filtros e lógica SQL
05_agregacoes          → Consultas com funções de agregação
06_joins               → Consultas envolvendo múltiplas tabelas
07_views_e_funcoes     → Views, functions e consultas avançadas

🧠 Conteúdos Abordados
🔧 Manipulação de Dados

INSERT, UPDATE e DELETE

Controle de integridade dos dados

Ajustes de estrutura para diferentes cenários de negócio

🔍 Consultas SQL

SELECT simples e condicionais

Filtros com WHERE, LIKE, IN e BETWEEN

Ordenação e paginação (ORDER BY, LIMIT, OFFSET)

📊 Agregações e Análises

Funções de agregação: COUNT, AVG, MIN, MAX

GROUP BY e HAVING

Análises por categoria, cliente, produto e fornecedor

🔗 Joins e Relacionamentos

INNER JOIN e LEFT JOIN

Consultas envolvendo múltiplas tabelas

Identificação de clientes sem pedidos

Total de pedidos por cliente

🧩 Views e Funções

Criação de VIEW para simplificação de análises

Construção de funções SQL para encapsular regras de negócio

Uso de EXPLAIN para compreensão de performance das consultas

📈 Camada Analítica e BI

Os dados foram estruturados no BigQuery, com a criação de uma view analítica (fato_pedidos), utilizada como base para os dashboards.

Métricas de Negócio Criadas

Receita Total

Quantidade de Pedidos

Ticket Médio

Itens Vendidos

Itens por Pedido (média)

Receita por Categoria

Receita por Produto

Receita por Cliente

Receita e Ticket Médio por Funcionário

Distribuição de Status dos Pedidos

Análise de Dias de Pico e Dias Fracos

📊 Dashboards – Looker Studio

O projeto conta com dashboards interativos organizados em páginas temáticas:

📌 Página 1 – Visão Geral

KPIs principais

Receita ao longo do tempo

Receita por categoria

Top produtos por receita

📌 Página 2 – Análise de Produtos

Top 10 produtos por receita

Top 10 produtos por quantidade vendida

Receita por categoria

📌 Página 3 – Clientes & Funcionários

Clientes com mais pedidos

Receita por cliente

Receita por funcionário

Distribuição de status dos pedidos

📌 Página 4 – Operacional & Eficiência

Pedidos por dia (picos e vales)

Ticket médio por dia

Itens por pedido (média)

Status dos pedidos ao longo do tempo

Ticket médio e volume por funcionário

💡 Principais Insights Obtidos

Pratos principais concentram a maior parte da receita

Alguns clientes geram alto valor mesmo com poucos pedidos

Funcionários apresentam diferenças entre volume de vendas e ticket médio

Dias de pico possuem comportamento distinto de consumo

A maioria dos pedidos é concluída, com pontos específicos de atenção operacional

🚀 Próximas Evoluções

Análises avançadas com Python (Pandas)

Curva ABC de produtos

Análise de recorrência de clientes

Simulação de cenários promocionais

Otimização de consultas e custos no BigQuery

🛠️ Tecnologias Utilizadas

SQL (MySQL)

Google BigQuery

Looker Studio

GitHub

👤 Autor

Gustavo Carvalho
Analista de Dados / BI

Projeto desenvolvido para fins de estudo, prática profissional e portfólio.
