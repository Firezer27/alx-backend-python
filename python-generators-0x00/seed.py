#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

# ----------------------------------------------------
# 1️ Connect to MySQL server
# ----------------------------------------------------
def connect_db():
    """Connects to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yourpassword'
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# ----------------------------------------------------
# 2️ Create Database ALX_prodev
# ----------------------------------------------------
def create_database(connection):
    """Creates ALX_prodev database if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully (if not existed)")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


# ----------------------------------------------------
# 3️ Connect directly to ALX_prodev
# ----------------------------------------------------
def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# ----------------------------------------------------
# 4️ Create user_data Table
# ----------------------------------------------------
def create_table(connection):
    """Creates user_data table if not exists"""
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


# ----------------------------------------------------
# 5️ Insert Data from CSV
# ----------------------------------------------------
def insert_data(connection, csv_file):
    """Inserts data into user_data table from CSV"""
    try:
        cursor = connection.cursor()

        # Read data from CSV
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age);
                """
                cursor.execute(query, (user_id, name, email, age))

        connection.commit()
        cursor.close()
        print("Data inserted successfully from CSV")

    except FileNotFoundError:
        print("CSV file not found. Please make sure user_data.csv exists in the same directory.")
    except Error as e:
        print(f"Error inserting data: {e}")
