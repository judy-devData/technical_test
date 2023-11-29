
SELECT
  client_id,
  SUM(
    CASE WHEN product_type = "MEUBLE" THEN prod_price * prod_qty END
  ) AS ventes_meuble,
  SUM(
    CASE WHEN product_type = "DECO" THEN prod_price * prod_qty END
  ) AS ventes_deco
FROM transaction as T
  LEFT JOIN product_nomenclature as P
       ON T.prop_id = P.product_id
WHERE
  date <= '31/12/19'
  AND date >= '01/01/19'
GROUP BY
  client_id