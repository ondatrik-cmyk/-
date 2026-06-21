import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ОЧИЩЕННЯ ТА ПІДГОТОВКА БД ДО РОБОТИ

def get_prepared_data():

    HERE = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(HERE, 'online_store.db')

    def load_table(table_name):
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            return df

    df_categories = load_table('categories')
    df_customer_pii = load_table('customer_pii')
    df_customers = load_table('customers')
    df_employee_salaries = load_table('employee_salaries')
    df_employees = load_table('employees')
    df_inventory = load_table('inventory')
    df_order_items = load_table('order_items')
    df_orders = load_table('orders')
    df_payments = load_table('payments')
    df_products = load_table('products')
    df_promotions = load_table('promotions')
    df_returns = load_table('returns')
    df_reviews = load_table('reviews')
    df_shipments = load_table('shipments')
    df_shippers = load_table('shippers')
    df_sqlite_master = load_table('sqlite_master')
    df_suppliers = load_table('suppliers')
    df_warehouses = load_table('warehouses')

    # 2. Проведіть підготовку та очищення даних:
    # * опрацюйте пропущені значення;
    # * приведіть дані до коректних типів;
    # * уніфікуйте регістр текстових полів;
    # * усуньте дублікати та інші виявлені проблеми якості даних;
    # * за потреби виконайте додаткову обробку для забезпечення коректності аналізу.

    # 2.1. Опрацьовуємо пропущені значення в усіх таблицях.

    all_dfs = {
        'categories': df_categories,
        'customer_pii': df_customer_pii,
        'customers': df_customers,
        'employee_salaries': df_employee_salaries,
        'employees': df_employees,
        'inventory': df_inventory,
        'order_items': df_order_items,
        'orders': df_orders,
        'payments': df_payments,
        'products': df_products,
        'promotions': df_promotions,
        'returns': df_returns,
        'reviews': df_reviews,
        'shipments': df_shipments,
        'shippers': df_shippers,
        'sqlite_master': df_sqlite_master,
        'suppliers': df_suppliers,
        'warehouses': df_warehouses
    }

    for name, df in all_dfs.items():
        null_counts = df.isnull().sum().sum()
        if null_counts > 0:
            print(f"У таблиці '{name}' знайдено пропусків: {null_counts}")
        else:
            print(f"У таблиці '{name}' пропусків немає.")

    # Виправляю пропуски по конці promotion_id в таблиці order_items на "0", тому що це значення дає розуміння ,
    # що товар був проданий без акції , тоб-то по повній ціні.

    # Перевіряю пропуски в таблиці  order_items.

    print("Пошук пропусків в таблиці order_items:")
    print(df_order_items.isnull().sum())

    df_order_items['promotion_id'] = df_order_items['promotion_id'].fillna(0)

    print("Пропуски після очищення в таблиці order_items :")
    print(df_order_items['promotion_id'].isnull().sum())

    # Перевіряю пропуски в таблиці  categories.

    print("Пошук пропусків в таблиці categories:")
    print(df_categories.isnull().sum())

    df_categories['parent_id'] = df_categories['parent_id'].fillna(0)

    print("Пропуски після очищення:")
    print(df_categories['parent_id'].isnull().sum())

    # Перевіряю пропуски в таблиці  customers.

    print("Пошук пропусків в таблиці customers:")
    print(df_customers.isnull().sum())

    df_customers['email'] = df_customers['email'].fillna('no_email@example.com')

    df_customers['birth_date'] = df_customers['birth_date'].fillna('1900-01-01')

    print("Пропуски після очищення:")
    print(df_customers.isnull().sum())

    # Перевіряю пропуски в таблиці  employees.

    print("Пошук пропусків в таблиці employees:")
    print(df_employees.isnull().sum())

    df_employees['manager_id'] = df_employees['manager_id'].fillna(0)

    print("Пропуски після очищення:")
    print(df_employees['manager_id'].isnull().sum())


    # 2.2.Приводимо  дані усіх таблиць до коректних типів;

    def optimize_data_types(df):
        for col in df.columns:

            is_date_col = ('date' in col.lower() or 'at' in col.lower()) and \
                          not any(x in col.lower() for x in ['id', 'rating', 'status', 'name'])

            if is_date_col:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')

            elif 'id' in col.lower() or 'rating' in col.lower() or 'quantity' in col.lower():
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            elif 'price' in col.lower() or 'amount' in col.lower() or 'cost' in col.lower() or 'discount' in col.lower():
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

        return df


    for name, df in all_dfs.items():
        all_dfs[name] = optimize_data_types(df)
        print(f"Таблицю '{name}' оптимізовано.")

    # 2.3.Уніфікація регістру текстових полів та назв країн.

    country_map = {
        'u.s.a.': 'usa', 'united states': 'usa', 'us': 'usa',
        'u.k.': 'uk', 'united kingdom': 'uk', 'britain': 'uk',
        'deutschland': 'germany', 'de': 'germany',
        'españa': 'spain', 'es': 'spain',
        'italia': 'italy', 'it': 'italy',
        'polska': 'poland', 'pl': 'poland', 'fr': 'france'
    }

    for name, df in all_dfs.items():

        text_cols = df.select_dtypes(include=['object', 'string']).columns

        for col in text_cols:

            df[col] = df[col].astype(str).str.lower().str.strip()

            if col == 'country':
                df[col] = df[col].replace(country_map)

        print(f"Таблицю '{name}' уніфіковано (текст + країни).")

    # 2.4. Перевірка на дублікати
    for name, df in all_dfs.items():
        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < initial_rows:
            print(f"У таблиці '{name}' видалено {initial_rows - len(df)} дублікатів.")
        else:
            print(f"Таблиця '{name}' без дублікатів.")

    return all_dfs