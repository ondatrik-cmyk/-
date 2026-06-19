import sqlite3
import pandas as pd


conn = sqlite3.connect("online_store.db")

query = """
SELECT
    p.product_id,
    p.name AS product_name,
    GROUP_CONCAT(DISTINCT w.name) AS warehouses,
    SUM(i.quantity) AS total_stock
FROM inventory AS i
JOIN products AS p
    ON p.product_id = i.product_id
JOIN warehouses AS w
    ON w.warehouse_id = i.warehouse_id
WHERE p.is_active = 0
GROUP BY
    p.product_id,
    p.name
HAVING SUM(i.quantity) > 0
ORDER BY total_stock DESC
"""

df = pd.read_sql_query(query, conn)

print(df.head())

conn.close()
