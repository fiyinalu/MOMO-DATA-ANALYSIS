import xml.etree.ElementTree as ET
import sqlite3
import re
from datetime import datetime

# Function to parse and categorize SMS body text
def parse_sms(body):
    data = {
        'transaction_id': None,
        'type': None,
        'amount': None,
        'sender': None,
        'receiver': None,
        'date': None,
        'raw_text': body
    }

    # Extract transaction ID
    txid_match = re.search(r'TxId[:\s]*([0-9]+)', body, re.IGNORECASE)
    if txid_match:
        data['transaction_id'] = txid_match.group(1)
    else:
        # Try alternate pattern
        txid_match_alt = re.search(r'Transaction ID[:\s]*([0-9]+)', body, re.IGNORECASE)
        if txid_match_alt:
            data['transaction_id'] = txid_match_alt.group(1)

    # Extract amount
    amount_match = re.search(r'(\d+)\s*RWF', body)
    if amount_match:
        data['amount'] = int(amount_match.group(1))

    # Extract date
    date_match = re.search(r'Date[:\s]*([\d\-]+\s[\d:]+)', body)
    if date_match:
        try:
            data['date'] = datetime.strptime(date_match.group(1), '%Y-%m-%d %H:%M:%S')
        except:
            data['date'] = None

    # Categorize transaction type and parties based on keywords
    body_lower = body.lower()

    if 'received' in body_lower:
        data['type'] = 'Incoming Money'
        sender_match = re.search(r'from ([\w\s]+)\.', body, re.IGNORECASE)
        if sender_match:
            data['sender'] = sender_match.group(1)
    elif 'payment' in body_lower:
        data['type'] = 'Payment'
        receiver_match = re.search(r'to ([\w\s]+)', body, re.IGNORECASE)
        if receiver_match:
            data['receiver'] = receiver_match.group(1)
    elif 'withdrawn' in body_lower:
        data['type'] = 'Withdrawal'
        receiver_match = re.search(r'agent: ([\w\s]+)', body, re.IGNORECASE)
        if receiver_match:
            data['receiver'] = receiver_match.group(1)
    elif 'internet bundle' in body_lower or 'voice bundle' in body_lower:
        data['type'] = 'Bundle Purchase'
    else:
        data['type'] = 'Other'

    return data

# Parse XML file and extract SMS messages
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    messages = []

    for sms in root.findall('sms'):
        body_element = sms.find('body')
        if body_element is None:
            continue  # Skip if no body tag
        body = body_element.text
        messages.append(body)

    return messages

# Main function to process XML and insert into DB
def main():
    # Connect to SQLite database (or create it)
    conn = sqlite3.connect('momo_transactions.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            type TEXT,
            amount INTEGER,
            sender TEXT,
            receiver TEXT,
            date TIMESTAMP,
            raw_text TEXT
        )
    ''')

    # Parse SMS data from XML
    messages = parse_xml('modified_sms_v2.xml')

    # Process each message and insert into DB
    for body in messages:
        data = parse_sms(body)
        if data['transaction_id']:
            try:
                cursor.execute('''
                    INSERT INTO transactions (transaction_id, type, amount, sender, receiver, date, raw_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data['transaction_id'], data['type'], data['amount'], data['sender'], data['receiver'], data['date'], data['raw_text']))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Duplicate transaction skipped: {data['transaction_id']}")

    conn.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    main()
