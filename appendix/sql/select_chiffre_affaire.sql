SELECT 
    date, 
    sum(prod_price * prod_qty) AS ventes
FROM TRANSACTION
WHERE date BETWEEN '01/01/2019' AND '12/31/2019'
GROUP BY date
ORDER BY date ASC;