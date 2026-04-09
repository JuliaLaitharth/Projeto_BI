--- Detalhamento Estornos 
SELECT 
    d.id_data AS "Data do Estorno",
    e.nome_estabelecimento AS "Estabelecimento",
    c.nome_categoria AS "Categoria",
    f.valor_brl AS "Valor Estornado"
FROM fato_transacao f
JOIN dim_estabelecimento e ON f.id_estabelecimento = e.id_estabelecimento
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
JOIN dim_data d ON f.id_data = d.id_data
WHERE f.valor_brl < 0 
ORDER BY d.id_data DESC;

--- Credito por Categoria 
SSELECT 
    c.nome_categoria,
    ABS(SUM(f.valor_brl)) AS "Total Recuperado (R$)"
FROM fato_transacao f
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
WHERE f.valor_brl < 0
GROUP BY c.nome_categoria
ORDER BY "Total Recuperado (R$)" DESC;

--- Total Geral de Estornos 
SELECT 
    ABS(SUM(valor_brl)) AS total_estornado_periodo
FROM fato_transacao
WHERE valor_brl < 0;