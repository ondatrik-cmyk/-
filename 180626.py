import sqlite3
import pandas as pd

conn = sqlite3.connect("online_store.db")

query = """
SELECT
    p.product_id,
    p.name AS product_name,
    SUM(i.quantity) AS total_stock
FROM inventory i
JOIN products p
    ON p.product_id = i.product_id
JOIN warehouses w
    ON w.warehouse_id = i.warehouse_id
GROUP BY p.product_id, p.name
ORDER BY total_stock DESC
"""

df = pd.read_sql_query(query, conn)

print(df.head(5))