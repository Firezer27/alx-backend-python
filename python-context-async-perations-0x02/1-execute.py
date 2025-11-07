import sqlite3

class ExecuteQuery:
    def __init___(self,filename,query,params=None):
        self.filename = filename
        self.query = query
        self.params = params 
    def __enter__(self):
        print("Opening database connection...")
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

        #execute the query
        self.cursor.execute(self.query,self.params)

        self.results = self.cursor.fetchall()
        return self.results
    def __exit__(self,type,value,traceback):
        print("data connection closed.")

query = "SELECT * FROM users where age = ?"
params=(25,)
with ExecuteQuery('users.db',query,params) as results:
    print(results)
