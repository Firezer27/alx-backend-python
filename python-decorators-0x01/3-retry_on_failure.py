import time
import sqlite3
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn= sqlite3.connect('users.db')
        print("Establishing database connection...")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("Database connection closed.")
    return wrapper

""" your code goes here"""
#---------------------------------
# retry_on_failure decorator
#---------------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            for attempt in range(1,retries+1):
                try:
                    return func(*args,**kwargs)
                except sqlite3.OperationalError as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise
            return wrapper
        return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
