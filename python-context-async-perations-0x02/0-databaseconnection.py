import sqlite3

class DatabaseConnection:
    def __init__(self,filename,method='w'):
        self.filename = filename
    def __enter__(self):
        print("Opening database connection...")
        self.conn = sqlite3.connect(self.filename)
        return self.conn
    def __exit__(self,type,value,traceback):
        self.conn.close()
        print("Database connection closed.")


with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
