import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


conn = sqlite3.connect("online_store.db")

query = """
SELECT
    country AS "Країна",
    COUNT(*) AS "Кількість постачальників"
FROM suppliers
GROUP BY country
ORDER BY "Кількість постачальників" DESC
LIMIT 10
"""

df_suppliers = pd.read_sql_query(query, conn)

print(df_suppliers)

conn.close()


plt.figure(figsize=(10, 6))

sns.barplot(
    data=df_suppliers,
    x="Країна",
    y="Кількість постачальників",
    color="steelblue"
)

plt.title("ТОП-10 країн за кількістю постачальників")
plt.xlabel("Країна")
plt.ylabel("Кількість постачальників")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()