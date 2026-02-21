from cryptography.fernet import Fernet
import hashlib
import mariadb
import os

if not os.path.exists("master.key"):
    with open("master.key", "wb") as f:
        f.write(Fernet.generate_key())

with open("master.key", "rb") as f:
    KEY = f.read()

cipher = Fernet(KEY)



import mysql.connector

pip install mysql-connector-python

conn = mysql.connector.connect(
    host="localhost",
    user="root",          # change if different
    password="your_mysql_password",
    database="secure_contacts"
)

cursor = conn.cursor()



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
          
    def login(self, username, password):
        hash_password = self.hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password))
        return cursor.fetchone()
    
    
class ContactManager():
    def __init__(self, owner):
        self.owner = owner
        
    def encrypt(self, phone):
        return cipher.encrypt(phone.encode())
    
    def decrypt(self, phone):
        return cipher.decrypt(phone).decode()

        
    def add_contact(self, name, phone):
        encrypted_phone = self.encrypt(phone)
        cursor.execute("INSERT INTO contacts (owner,name,phone) VALUES(?, ?, ?)", (self.owner, name, encrypted_phone))
        conn.commit()
        print("-------------------------------")
        
        
    def view_contacts(self):
        cursor.execute("SELECT * FROM contacts WHERE owner=?", (self.owner, ))
        records = cursor.fetchall()
        
        if not records:
            print("No Contacts found")
            return
          
        for row in records:  
            decrypte_phone = self.decrypt(row[3])
            print(f"Name = {row[2]} : Contact = {decrypte_phone}")
            print("-------------------------------")
            
        
    def delete_contact(self):
        cursor.execute("DELETE FROM contacts WHERE owner=?", (self.owner, ))
        conn.commit()
        print("Contact Successfully Deleted")
        print("-------------------------------")
    
          
auth = Auth()

print("1 to Register")
print("2 to Login")

choice = input("Enter your choice: ")
if choice == "1":
    usr = input("Enter your name: ")
    password = input("Enter your password: ")
    auth.register(usr, password)
    
    
elif choice == "2":
    usr = input("Enter your name: ")
    password = input("Enter your password: ")
    print("-------------------------------")

    if auth.login(usr, password):
        manager = ContactManager(usr)
        while True:
            print("1 Add Contact")
            print("2 View Contacts")
            print("3 Delete Constact")
            print("4 Exit")
            print("-------------------------------")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                name = input("Enter the name: ")
                phone = input("Enter the contact number: ")
                manager.add_contact(name, phone)
                
            elif choice == "2":
                manager.view_contacts()
                
            elif choice == "3":
                manager.delete_contact()
                
            elif choice == "4":
                print("Code Exited")
                break
            
            else:
                print("Invalid Choice\nTry Again")
                print("--------------------")
                
    else:
        print("Invalid Login")       
            
else:
    print("Invalid Choice\nTry Again")