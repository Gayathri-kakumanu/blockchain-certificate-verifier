import qrcode
import sqlite3

conn = sqlite3.connect("certificates.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates(
    reg_no TEXT PRIMARY KEY,
    student_name TEXT,
    certificate_hash TEXT,
    certificate_id TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")