SELECT 
    t.client_id AS client_id,
    SUM(case when n.product_type = 'MEUBLE' then (t.prod_price * t.prod_qty) else 0 end) AS ventes_meuble,
    SUM(case when n.product_type = 'DECO' then (t.prod_price * t.prod_qty) else 0 end) AS ventes_deco
FROM TRANSACTION t
INNER JOIN PRODUCT_NOMENCLATURE n
ON t.prod_id = n.product_id
WHERE date BETWEEN '01/01/2020' AND '12/31/2020'
GROUP BY 1;