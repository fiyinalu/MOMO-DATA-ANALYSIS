# MOMO DATA ANALYSIS 📱

## Overview

This project is a simple SMS parsing tool written in Python that extracts SMS messages from an XML file (typically exported from Android phones using apps like SMS Backup & Restore) and converts them into a structured CSV file.

It is part of an academic assignment to demonstrate basic file parsing, data transformation, and export to a user-friendly format.

## Video link to demo explanation
[https://www.loom.com/share/7ace5f72cde544cabf80d8655cd05fec?sid=f9545eb7-35ef-427c-a540-fa36f16c3050]

---

## 📂Some of The Files Included

| File Name              | Description                                          |
|------------------------|------------------------------------------------------|
| `parse_sms.py`         | Python script to parse the SMS XML and generate CSV |
| `modified_sms_v2.xml`  | Sample input XML file with SMS messages              |
| `sms_export.csv`       | Output CSV file generated after parsing              |
| `report.pdf`           | PDF report documenting the approach and challenges   |
| `AUTHORS`              | File listing the author of the project               |
| `README.md`            | This file contains the instructions and project documentation   |

---

## ✅ Features

- Parses Android SMS backup XML files
- Extracts sender, date, time, message body, and message type
- Converts UNIX timestamps to readable date-time format
- Exports parsed SMS data into a clean CSV
- Clear separation of logic for easy editing

---

## ⚙️ How to Run the Script

### Requirements
- Python 3.x installed
- `modified_sms_v2.xml` file in the same folder as the script

### Run with:
```bash
python parse_sms.py

##Once the script runs, you’ll find a new file named sms_export.csv with the parsed data.


📌 CSV Output Fields
| Field     | Description                                  |
| --------- | -------------------------------------------- |
| `address` | The phone number or contact who sent the SMS |
| `date`    | Human-readable date and time of the SMS      |
| `type`    | Type of SMS (1 = received, 2 = sent)         |
| `body`    | The actual content of the SMS message        |
