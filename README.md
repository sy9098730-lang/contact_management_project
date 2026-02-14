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

class Auth:
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, name, password):
        hash_password = self.hash_password(password)
        try:
            cursor.execute("INSERT INTO users VALUES(?,?)", (name, hash_password))   
            conn.commit()
            print("Registration Successfull")
            
        except:
          print("User Already Exists")  