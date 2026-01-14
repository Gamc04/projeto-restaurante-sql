
SELECT
  p.id_produto AS id,
  p.nome,
  p.descricao,
  ip.ingredientes
FROM produtos p
LEFT JOIN info_produtos ip
  ON ip.id_produto = p.id_produto;

SELECT
  pe.id_pedido AS id,
  pe.quantidade,
  pe.data_pedido,
  c.nome,
  c.email
FROM pedidos pe
JOIN clientes c
  ON c.id_cliente = pe.id_cliente;

SELECT
  pe.id_pedido AS id,
  pe.quantidade,
  pe.data_pedido,
  c.nome AS nome_cliente,
  c.email,
  f.nome AS nome_funcionario
FROM pedidos pe
JOIN clientes c
  ON c.id_cliente = pe.id_cliente
JOIN funcionarios f
  ON f.id_funcionario = pe.id_funcionario;

SELECT
  pe.id_pedido AS id,
  pe.quantidade,
  pe.data_pedido,
  c.nome AS nome_cliente,
  c.email,
  f.nome AS nome_funcionario,
  pr.nome AS nome_produto,
  pr.preco
FROM pedidos pe
JOIN clientes c
  ON c.id_cliente = pe.id_cliente
JOIN funcionarios f
  ON f.id_funcionario = pe.id_funcionario
JOIN produtos pr
  ON pr.id_produto = pe.id_produto;

SELECT
  pe.id_pedido,
  c.nome AS nome_cliente,
  pe.status
FROM pedidos pe
JOIN clientes c
  ON c.id_cliente = pe.id_cliente
WHERE pe.status = 'Pendente'
ORDER BY pe.id_pedido DESC;

SELECT
  c.id_cliente,
  c.nome,
  c.email
FROM clientes c
LEFT JOIN pedidos pe
  ON pe.id_cliente = c.id_cliente
WHERE pe.id_pedido IS NULL
ORDER BY c.nome;

SELECT
  c.id_cliente,
  c.nome,
  COUNT(pe.id_pedido) AS total_pedidos
FROM clientes c
LEFT JOIN pedidos pe
  ON pe.id_cliente = c.id_cliente
GROUP BY c.id_cliente, c.nome
ORDER BY total_pedidos DESC, c.nome;

SELECT
  pe.id_pedido,
  pe.quantidade,
  pr.preco,
  (pe.quantidade * pr.preco) AS total_pedido
FROM pedidos pe
JOIN produtos pr
  ON pr.id_produto = pe.id_produto
ORDER BY pe.id_pedido;
