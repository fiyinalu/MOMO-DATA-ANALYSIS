import xml.etree.ElementTree as ET
from datetime import datetime

# Load your XML file
tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()

# Confirm it's the correct XML format
if root.tag != 'smses':
    print(f"Unexpected root tag: {root.tag}")
else:
    for sms in root.findall('sms'):
        address = sms.attrib.get('address')
        date_ms = int(sms.attrib.get('date'))
        date = datetime.fromtimestamp(date_ms / 1000)  # Convert milliseconds to seconds
        body = sms.attrib.get('body')
        sms_type = sms.attrib.get('type')  # '1' is received, '2' is sent

        direction = 'Received' if sms_type == '1' else 'Sent'

        print(f"{direction} from/to {address} on {date.strftime('%Y-%m-%d %H:%M:%S')}: {body}")
