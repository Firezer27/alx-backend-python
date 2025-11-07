import time
import sqlite3
import functools

#---------------------------
#with_db_connection decorator
#---------------------------
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

query_cache = {}

"""your code goes here"""
#---------------------------
# cache_query decorator
#---------------------------
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        query = kwargs.get('query', args[0] if args else None)

        if query in query_cache:
            print("returning cached result for query:", query)
            return query_cache[query]

        result = func(*args,**kwargs)
        query_cache[query] = result
        return result
    return wrapper


def
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
