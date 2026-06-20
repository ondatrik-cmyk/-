# виявити товари з крит залишками

inventory = dfs['inventory']
products = dfs['products']
warehouses = dfs['warehouses']

merged = (inventory
          .merge(products, on='product_id')
          .merge(warehouses, on='warehouse_id'))

print(merged.columns)

min_quantity = merged[merged['quantity']< 5]

print(f'critically low stock items: \n', min_quantity[['product_id','name_x', 'quantity']])

# «На якому складі найбільше товару?»
# Розрахувати сумарний залишок товарів (`inventory.quantity`) для кожного складу.
# Побудувати один barplot.

inventory_quantity = (merged.groupby('name_y', as_index=False)['quantity'].sum())

print(f'Total remaining inventory for each warehouse:')
print(inventory_quantity[['warehouses_id', 'name_y', 'quantity']])

plt.figure(figsize=(15,8))

sns.barplot(data=inventory_quantity, x='name_y', y='quantity', hue='name_y', palette='viridis')
plt.xticks(rotation=90)

plt.title('Inventory Quantity of goods in warehouses')
plt.xticks(rotation=45)
plt.xlabel('Warehouse')
plt.ylabel('Quantity')
plt.tight_layout()

plt.show()