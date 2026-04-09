--- Compras Internacionais com Cotaçao 
SELECT 
    d.id_data AS "Data da Compra",
    e.nome_estabelecimento AS "Estabelecimento",
    f.valor_usd AS "Valor (USD)",
    f.valor_brl AS "Valor (BRL)",
    ROUND((f.valor_brl / f.valor_usd), 2) AS "Cotação Aplicada"
FROM fato_transacao f
JOIN dim_estabelecimento e ON f.id_estabelecimento = e.id_estabelecimento
JOIN dim_data d ON f.id_data = d.id_data
WHERE f.valor_usd > 0 
  AND f.valor_usd IS NOT NULL
ORDER BY d.id_data DESC;

--- Dolar x Reais 
SELECT 
    SUM(valor_usd) AS total_dolar,
    SUM(valor_brl) AS total_convertido_brl,
    ROUND(AVG(valor_brl / valor_usd), 2) AS cotacao_media_periodo
FROM fato_transacao
WHERE valor_usd > 0;

--- Maiores gastos por Categorias 
SELECT 
    c.nome_categoria,
    SUM(f.valor_usd) AS total_usd,
    COUNT(*) AS qtd_compras
FROM fato_transacao f
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
WHERE f.valor_usd > 0
GROUP BY c.nome_categoria
ORDER BY total_usd DESC;