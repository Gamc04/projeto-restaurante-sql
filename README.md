# Projeto Restaurante – SQL | Análise de Dados

Este projeto simula o banco de dados de um restaurante, desenvolvido com foco em
**modelagem relacional, manipulação de dados e análise SQL**, aplicando boas
práticas de organização, legibilidade e performance.

O objetivo é demonstrar competências em **SQL aplicado a cenários reais**,
com consultas que geram insights relevantes para análise de dados e apoio à
tomada de decisão.

---

## Modelagem do Banco de Dados

O banco de dados `restaurante` foi modelado para representar operações reais,
incluindo:

- Clientes
- Funcionários
- Produtos
- Pedidos
- Informações adicionais de produtos

Foram aplicados conceitos como:
- Chaves primárias e estrangeiras
- Integridade referencial
- Tipos de dados adequados
- Relacionamentos entre tabelas

---

## Conteúdos Abordados

### Manipulação de Dados
- INSERT, UPDATE e DELETE
- Controle de integridade
- Ajustes de estrutura para diferentes cenários

### Consultas SQL
- SELECT simples e condicionais
- Filtros com WHERE, LIKE, IN e BETWEEN
- Ordenação e paginação (ORDER BY, LIMIT, OFFSET)

### Agregações e Análises
- COUNT, AVG, MIN, MAX
- GROUP BY e HAVING
- Análises por categoria, cliente e fornecedor

### Joins e Relacionamentos
- INNER JOIN e LEFT JOIN
- Consultas envolvendo múltiplas tabelas
- Identificação de clientes sem pedidos
- Total de pedidos por cliente

### Views e Funções
- Criação de VIEW para simplificação de análises
- Funções para encapsular regras de negócio
- Uso de EXPLAIN para compreensão de performance

---

## Organização do Repositório

```text
01_modelagem              → Criação das tabelas e estrutura do banco
02_manipulacao_dados      → Inserts, updates e ajustes de dados
03_consultas_basicas      → Consultas SQL simples
04_condicionais           → Condições, filtros e lógica SQL
05_agregacoes             → Consultas com funções de agregação
06_joins                  → Consultas envolvendo múltiplas tabelas
07_views_e_funcoes        → Views, functions e consultas avançadas
