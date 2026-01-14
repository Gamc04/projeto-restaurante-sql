USE restaurante;

SELECT COUNT(*) AS qtd_pedidos
FROM pedidos;

SELECT COUNT(DISTINCT id_cliente) AS qtd_clientes_unicos_com_pedido
FROM pedidos;

SELECT AVG(preco) AS media_preco_produtos
FROM produtos;

SELECT MIN(preco) AS preco_minimo,
       MAX(preco) AS preco_maximo
FROM produtos;

SELECT
  nome,
  preco,
  DENSE_RANK() OVER (ORDER BY preco DESC) AS ranking_preco
FROM produtos
ORDER BY preco DESC
LIMIT 5;

SELECT
  categoria,
  AVG(preco) AS media_preco_categoria
FROM produtos
GROUP BY categoria
ORDER BY categoria;

SELECT
  fornecedor,
  COUNT(*) AS qtd_produtos
FROM info_produtos
GROUP BY fornecedor
ORDER BY qtd_produtos DESC, fornecedor;

SELECT
  fornecedor,
  COUNT(*) AS qtd_produtos
FROM info_produtos
GROUP BY fornecedor
HAVING COUNT(*) > 1
ORDER BY qtd_produtos DESC, fornecedor;

SELECT
  c.id_cliente,
  c.nome,
  COUNT(p.id_pedido) AS qtd_pedidos
FROM pedidos p
JOIN clientes c ON c.id_cliente = p.id_cliente
GROUP BY c.id_cliente, c.nome
HAVING COUNT(p.id_pedido) = 1
ORDER BY c.nome;
