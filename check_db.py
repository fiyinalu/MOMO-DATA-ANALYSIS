import sqlite3

conn = sqlite3.connect('momo_data.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# If your table is named 'transactions', check sample data:
if ('transactions',) in tables:
    cursor.execute("SELECT * FROM transactions LIMIT 5;")
    rows = cursor.fetchall()
    print("Sample rows:")
    for row in rows:
        print(row)
else:
    print("Table 'transactions' not found in the database.")

conn.close()

