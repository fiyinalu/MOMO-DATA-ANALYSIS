import sqlite3
from lxml import etree
import re
from datetime import datetime

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect('momo_data.db')
cursor = conn.cursor()

# Create transactions table schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_id TEXT UNIQUE,
    transaction_type TEXT,
    amount INTEGER,
    fee INTEGER,
    sender TEXT,
    receiver TEXT,
    date TEXT,
    raw_message TEXT
)
''')
conn.commit()

def parse_sms_body(body):
    # Extract details from message body using regex
    tx_id = None
    amount = None
    fee = 0
    sender = None
    receiver = None
    date = None
    transaction_type = None

    # Extract transaction id
    tx_id_search = re.search(r'TxId:?(\d+)', body, re.I)
    if tx_id_search:
        tx_id = tx_id_search.group(1)
    
    # Extract amount
    amount_search = re.search(r'(\d{1,10}) RWF', body)
    if amount_search:
        amount = int(amount_search.group(1))

    # Extract fee if any
    fee_search = re.search(r'Fee: (\d+) RWF', body)
    if fee_search:
        fee = int(fee_search.group(1))

    # Extract date
    date_search = re.search(r'Date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
    if date_search:
        date = date_search.group(1)
    
    # Categorize transaction type (simple keywords matching)
    if 'received' in body.lower():
        transaction_type = 'Incoming Money'
    elif 'payment' in body.lower():
        transaction_type = 'Payments'
    elif 'withdrawn' in body.lower():
        transaction_type = 'Withdrawals'
    elif 'purchased an internet bundle' in body.lower():
        transaction_type = 'Internet Bundle Purchase'
    else:
        transaction_type = 'Other'

    # Extract sender and receiver (very simplified)
    sender_search = re.search(r'from ([\w\s]+)\.', body)
    if sender_search:
        sender = sender_search.group(1).strip()
    receiver_search = re.search(r'to ([\w\s]+) has', body)
    if receiver_search:
        receiver = receiver_search.group(1).strip()

    return {
        'tx_id': tx_id,
        'transaction_type': transaction_type,
        'amount': amount,
        'fee': fee,
        'sender': sender,
        'receiver': receiver,
        'date': date,
        'raw_message': body
    }

def main():
    # Load and parse XML
    tree = etree.parse('momo_sms.xml')  # Replace with your actual XML file name
    root = tree.getroot()

    ignored_messages = []

    for sms in root.findall('sms'):
        body = sms.find('body').text
        if not body:
            continue

        data = parse_sms_body(body)

        if data['tx_id'] is None or data['amount'] is None:
            ignored_messages.append(body)
            continue

        # Insert into database with duplicate check
        try:
            cursor.execute('''
                INSERT INTO transactions (tx_id, transaction_type, amount, fee, sender, receiver, date, raw_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['tx_id'], data['transaction_type'], data['amount'], data['fee'], 
                data['sender'], data['receiver'], data['date'], data['raw_message']
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Duplicate transaction id skipped: {data['tx_id']}")

    # Save ignored messages to a file
    with open('ignored_messages.txt', 'w') as f:
        for msg in ignored_messages:
            f.write(msg + '\n')

if __name__ == '__main__':
    main()
