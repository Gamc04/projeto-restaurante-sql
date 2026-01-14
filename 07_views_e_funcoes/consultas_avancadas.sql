DROP VIEW IF EXISTS resumo_pedido;

CREATE VIEW resumo_pedido AS
SELECT
  p.id_pedido,
  p.quantidade,
  p.data_pedido,
  c.nome  AS nome_cliente,
  c.email AS email_cliente,
  f.nome  AS nome_funcionario,
  pr.nome AS nome_produto,
  pr.preco
FROM pedidos p
JOIN clientes c      ON c.id_cliente = p.id_cliente
JOIN funcionarios f  ON f.id_funcionario = p.id_funcionario
JOIN produtos pr     ON pr.id_produto = p.id_produto;

SELECT
  id_pedido,
  nome_cliente,
  (quantidade * preco) AS total
FROM resumo_pedido;

CREATE OR REPLACE VIEW resumo_pedido AS
SELECT
  p.id_pedido,
  p.quantidade,
  p.data_pedido,
  c.nome  AS nome_cliente,
  c.email AS email_cliente,
  f.nome  AS nome_funcionario,
  pr.nome AS nome_produto,
  pr.preco,
  (p.quantidade * pr.preco) AS total
FROM pedidos p
JOIN clientes c      ON c.id_cliente = p.id_cliente
JOIN funcionarios f  ON f.id_funcionario = p.id_funcionario
JOIN produtos pr     ON pr.id_produto = p.id_produto;

SELECT
  id_pedido,
  nome_cliente,
  total
FROM resumo_pedido;

EXPLAIN
SELECT
  id_pedido,
  nome_cliente,
  total
FROM resumo_pedido;

DROP FUNCTION IF EXISTS BuscaIngredientesProduto;
DELIMITER $$

CREATE FUNCTION BuscaIngredientesProduto(p_id_produto INT)
RETURNS TEXT
DETERMINISTIC
READS SQL DATA
BEGIN
  DECLARE v_ingredientes TEXT;

  SELECT ingredientes
    INTO v_ingredientes
  FROM info_produtos
  WHERE id_produto = p_id_produto
  LIMIT 1;

  RETURN v_ingredientes;
END$$

DELIMITER ;

SELECT BuscaIngredientesProduto(10) AS ingredientes_produto_10;

DROP FUNCTION IF EXISTS mediaPedido;
DELIMITER $$

CREATE FUNCTION mediaPedido(p_id_pedido INT)
RETURNS VARCHAR(60)
DETERMINISTIC
READS SQL DATA
BEGIN
  DECLARE v_total_pedido DECIMAL(10,2);
  DECLARE v_media_total  DECIMAL(10,2);

  SELECT total
    INTO v_total_pedido
  FROM resumo_pedido
  WHERE id_pedido = p_id_pedido
  LIMIT 1;

  SELECT AVG(total)
    INTO v_media_total
  FROM resumo_pedido;

  IF v_total_pedido IS NULL THEN
    RETURN 'Pedido não encontrado';
  END IF;

  IF v_total_pedido > v_media_total THEN
    RETURN 'Acima da média';
  ELSEIF v_total_pedido < v_media_total THEN
    RETURN 'Abaixo da média';
  ELSE
    RETURN 'Igual à média';
  END IF;
END$$

DELIMITER ;

SELECT 5 AS id_pedido, mediaPedido(5) AS comparacao;
SELECT 6 AS id_pedido, mediaPedido(6) AS comparacao;
