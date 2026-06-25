import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_loader16062026 import get_prepared_data

# Завдання 4.
# Порівняти складські залишки та обсяги продажів.
# Визначити:
# -товарів і категорій із високою оборотністю;
# -товарів і категорій, що тривалий час залишаються на складі.

data = get_prepared_data()

df_inventory = data['inventory']
df_order_items = data['order_items']
df_products = data['products']
df_categories = data['categories']

inventory_totals = df_inventory.groupby('product_id')['quantity'].sum().reset_index()


sales_totals = df_order_items.groupby('product_id')['quantity'].sum().reset_index()

sales_totals.rename(columns={'quantity': 'total_sold'}, inplace=True)

final_data = df_products[['product_id', 'name', 'category_id']].copy()


final_data = final_data.merge(inventory_totals, on='product_id', how='left')


final_data = final_data.merge(sales_totals, on='product_id', how='left')


final_data = final_data.merge(df_categories[['category_id', 'name']],
                              on='category_id',
                              suffixes=('_product', '_category'))

final_data = final_data.fillna(0)

high_turnover = final_data.sort_values(by='total_sold', ascending=False)

slow_moving = final_data[(final_data['total_sold'] == 0) & (final_data['quantity'] > 0)]


category_turnover = final_data.groupby('name_category')[['quantity', 'total_sold']].sum()

category_turnover['turnover_ratio'] = category_turnover['total_sold'] / category_turnover['quantity'].replace(0, 1)

rez_analiz_categories = category_turnover.sort_values(by='turnover_ratio', ascending=False)

print("Загальна аналітична таблиця:")
print(final_data)

print("Топ товарів за обсягом продажів (Висока оборотність)")
print(high_turnover.head(10))

print("Товари, що залежуються (Мертвий вантаж)")
print(slow_moving.head(10))

print("Аналіз по категоріях (відношення продажів до залишків):")
print(rez_analiz_categories)


