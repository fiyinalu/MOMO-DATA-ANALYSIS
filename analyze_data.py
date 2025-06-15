import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your SQLite database
conn = sqlite3.connect('momo_data.db')  # use your actual DB file name

# Read the entire transactions table into a DataFrame
df = pd.read_sql_query("SELECT * FROM transactions;", conn)

# Check first few rows to understand data structure
print(df.head())

# Close connection
conn.close()
