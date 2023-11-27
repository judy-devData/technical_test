WITH join_query as (
  SELECT
    *
  FROM
    TRANSACTIONS
    JOIN PRODUCT_NOMENCLATURE ON TRANSACTIONS.prop_id = PRODUCT_NOMENCLATURE.product_id
)

SELECT
  client_id,
  SUM(
    CASE WHEN product_type = "MEUBLE" THEN prod_price * prod_qty END
  ) AS ventes_meuble,
  SUM(
    CASE WHEN product_type = "DECO" THEN prod_price * prod_qty END
  ) AS ventes_deco
FROM
  join_query
WHERE
  date <= '31/12/19'
  AND date >= '01/01/19'
GROUP BY
  client_id