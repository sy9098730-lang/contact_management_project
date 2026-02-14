# contact_management_project

rom cryptography.fernet import Fernet
import hashlib
import _sqlite3

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

conn = _sqlite3.connect("contact.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
	username TEXT PRIMARY KEY,
	password TEXT
	)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	owner TEXT,
	name TEXT,
	phone BLOB
	"""))
