import sqlite3
import functools

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn,*args,**kwargs):
        conn =sqlite3.connect('users.db')
        try:
            print("transaction started...")
            result = func(conn,*args,**kwargs)
            conn.commit()
            print("transaction committed...")
            return result
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back")
        finally:
            conn.close()
            print("connection closed")
    return wrapper



@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
cursor = conn.cursor()
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
