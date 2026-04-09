--- Gasto Total 
SELECT 
    SUM(valor_brl) AS total_gasto_brl
FROM fato_transacao
WHERE valor_brl > 0;

--- Evoluçao de gastos por mês 
SELECT 
    d.mes,
    d.ano,
    SUM(f.valor_brl) AS total_mensal
FROM fato_transacao f
JOIN dim_data d ON f.id_data = d.id_data
WHERE f.valor_brl > 0
GROUP BY d.ano, d.mes
ORDER BY d.ano DESC, d.mes DESC;

--- Gastos por Categoria
SELECT 
    c.nome_categoria,
    SUM(f.valor_brl) AS total_por_categoria,
    COUNT(f.id_transacao) AS quantidade_transacoes
FROM fato_transacao f
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
WHERE f.valor_brl > 0
GROUP BY c.nome_categoria
ORDER BY total_por_categoria DESC;

--- Top 10 Estabelecimentos 
SELECT 
    e.nome_estabelecimento,
    SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
JOIN dim_estabelecimento e ON f.id_estabelecimento = e.id_estabelecimento
WHERE f.valor_brl > 0
GROUP BY e.nome_estabelecimento
ORDER BY total_gasto DESC
LIMIT 10;

--- Média Gasto Titular 
SELECT 
    t.nome_titular,
    ROUND(AVG(f.valor_brl), 2) AS media_por_transacao,
    SUM(f.valor_brl) AS total_acumulado
FROM fato_transacao f
JOIN dim_titular t ON f.id_titular = t.id_titular
WHERE f.valor_brl > 0
GROUP BY t.nome_titular;