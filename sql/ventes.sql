SELECT
  date,
  SUM(prod_price * prod_qty) as ventes
from
  TRANSACTIONS
WHERE
  date <= '31/12/19'
  AND date >= '01/01/19'
GROUP BY
  date
ORDER BY
  date