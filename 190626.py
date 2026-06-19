# Проаналізувати поле shipments.cost
#
# середню вартість доставки за перевізниками;
#
# середню вартість доставки за регіонами;
#
# частку логістичних витрат у доході від замовлення.

import sqlite3
import pandas as pd


conn = sqlite3.connect("online_store.db")


# 1. середню вартість доставки за перевізниками;
query_shippers = """
SELECT
    sp.name AS shipper_name,
    ROUND(AVG(s.cost), 2) AS avg_shipping_cost
FROM shipments AS s
JOIN shippers AS sp
    ON sp.shipper_id = s.shipper_id
GROUP BY sp.shipper_id, sp.name
ORDER BY avg_shipping_cost DESC
"""

df_shippers = pd.read_sql_query(query_shippers, conn)

print("середню вартість доставки за перевізниками:")
print(df_shippers)


# 2. середню вартість доставки за регіонами;
query_regions = """
SELECT
    e.region,
    ROUND(AVG(s.cost), 2) AS avg_shipping_cost
FROM shipments AS s
JOIN orders AS o
    ON o.order_id = s.order_id
JOIN employees AS e
    ON e.employee_id = o.employee_id
GROUP BY e.region
ORDER BY avg_shipping_cost DESC
"""

df_regions = pd.read_sql_query(query_regions, conn)

print("\nСередня вартість доставки за регіонами:")
print(df_regions)


# 3. частку логістичних витрат у доході від замовлення.
query_logistics_share = """
WITH order_revenue AS (
    SELECT
        order_id,
        SUM(quantity * unit_price * (1 - discount)) AS revenue
    FROM order_items
    GROUP BY order_id
)
SELECT
    s.order_id,
    ROUND(r.revenue, 2) AS order_revenue,
    ROUND(s.cost, 2) AS shipping_cost,
    ROUND(
        s.cost / NULLIF(r.revenue, 0) * 100,
        2
    ) AS logistics_share_pct
FROM shipments AS s
JOIN order_revenue AS r
    ON r.order_id = s.order_id
ORDER BY logistics_share_pct DESC
"""

df_logistics = pd.read_sql_query(query_logistics_share, conn)

print("\nДоля логистических расходов в доходе заказа:")
print(df_logistics.head(10))


conn.close()