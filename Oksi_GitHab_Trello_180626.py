
#=====================================================================
# робимо об’єднання таблиць для аналізу:
# Поєднюємо та досліджуємо дані користуючись таблицями suppliers і products

# <<<<<<< onalivka-tech-patch-1
# df_inventory = df['inventory']
# df_products = df['products']
# df_warehouses = df['warehouses']
# df_suppliers = df['suppliers']

# full_data = (df_inventory
#           .merge(df_products, on='product_id')
#           .merge(df_warehouses, on='warehouse_id'))

# print(full_data.columns)
# =======
# # df_inventory = df['inventory']
# # df_products = df['products']
# # df_warehouses = df['warehouses']
# # df_suppliers = df['suppliers']
# #
# # full_data = (df_inventory
# #           .merge(df_products, on='product_id')
# #           .merge(df_warehouses, on='warehouse_id'))
# #
# # print(full_data.columns)
# >>>>>>> main

df_inventory = df['inventory']
df_products = df['products']
df_warehouses = df['warehouses']
df_suppliers = df['suppliers']

full_data = (df_inventory
          .merge(df_products, on='product_id')
          .merge(df_warehouses, on='warehouse_id'))

print(full_data.columns)

full_data_1 = (df_inventory
          .merge(df_products, on='product_id')
          .merge(df_suppliers, on='supplier_id')
)

print(full_data_1.columns)

#=====================================================================
# виявити товари з крит залишками (використовувати таблиці inventory, products і warehouses)

# використовую об’єднанняя яке вже створив Дмитро: full_data (таблиці inventory, products і warehouses)

min_quantity = full_data[full_data['quantity']< 5]

print(f'critically low stock items: \n', min_quantity[['product_id','name_x', 'quantity']])

#=====================================================================
# «На якому складі найбільше товару?»
# Розрахувати сумарний залишок товарів (`inventory.quantity`) для кожного складу.
# Побудувати один barplot.

# використовую об’єднанняя яке вже створив Дмитро: full_data (таблиці inventory, products і warehouses)

inventory_quantity = (full_data.groupby('name_y', as_index=False)['quantity'].sum())

print(f'Total remaining inventory for each warehouse:')
print(inventory_quantity[['name_y', 'quantity']])

plt.figure(figsize=(15,8))

sns.barplot(data=inventory_quantity, x='name_y', y='quantity', hue='name_y', palette='viridis')
plt.xticks(rotation=90)

plt.title('Inventory Quantity of goods in warehouses')
plt.xticks(rotation=45)
plt.xlabel('Warehouse')
plt.ylabel('Quantity')
plt.tight_layout()

plt.show()

#=====================================================================
# Рейтинг постачальників та їхню частку в асортименті

# We count the number of goods from each supplier.
rating_suppliers = (
    full_data_1.groupby(['supplier_id'], as_index=False)['product_id']
    .count()
    .rename(columns={'product_id': 'product_count'})
)

# We count the percentage share.
total_assortment = rating_suppliers['product_count'].sum()
rating_suppliers ['share_percent'] = ((rating_suppliers['product_count']) / total_assortment*100).round(2)

# Sort from largest to smallest
rating_suppliers = rating_suppliers.sort_values('product_count', ascending=False)

print(rating_suppliers)

plt.figure(figsize=(8,8))

plt.pie(
    rating_suppliers['product_count'],
    labels= rating_suppliers['supplier_id'],
    autopct='%1.1f%%',
    colors= sns.color_palette())
plt.title('Rating suppliers by product count')
plt.show()

#=====================================================================
# Внесок у продажі та географію постачальників (країни походження)
# Поєднати та дослідити дані користуючись таблицями suppliers і products
# Внесок у продажі - це загальна сума cost в розрізі постачальників

# Total cost by supplier and country
total_cost_by_supplier =(
    full_data_1.groupby(['supplier_id', 'name_y', 'country'], as_index=False)['cost']
    .sum()
    .rename(columns={'cost': 'total_cost'})
)

#Total sales volume
total_amount_sales = total_cost_by_supplier['total_cost'].sum()
print(f'Total amount sales: {total_amount_sales}')

# Add sales contribution (%)
total_cost_by_supplier ['contribution_to_sales_percent'] = (
        total_cost_by_supplier['total_cost']/ total_amount_sales * 100
).round(2)

# Sort by sales contribution
total_cost_by_supplier = total_cost_by_supplier.sort_values('total_cost', ascending=False)

print(f'Contribution of each supplier to sales and Geography of suppliers (country of origin):')
print(total_cost_by_supplier[['name_y', 'country', 'total_cost','contribution_to_sales_percent']])
