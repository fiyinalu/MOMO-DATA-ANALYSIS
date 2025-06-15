from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def fetch_transactions():
    conn = sqlite3.connect('momo_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT transaction_type, amount FROM transactions')
    data = cursor.fetchall()
    conn.close()
    return [{'transaction_type': row[0], 'amount': row[1]} for row in data]

@app.route('/api/transactions')
def get_transactions():
    data = fetch_transactions()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
