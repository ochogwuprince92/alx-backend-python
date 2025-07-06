import mysql.connector
import csv
import os
from uuid import UUID

# Function to connect to the MySQL server
def connect_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='devuser',
            password='Devpass123!'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Function to create ALX_prodev database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()

# Function to connect to the ALX_prodev database
def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='devuser',
            password='Devpass123!', 
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# Function to create the user_data table
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# Function to insert data into the table from CSV
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Ensure user_id is valid UUID
                UUID(row['user_id'], version=4)
                # Check if user_id exists
                cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
                if cursor.fetchone():
                    continue  # Skip if exists
                insert_query = '''
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (
                    row['user_id'],
                    row['name'],
                    row['email'],
                    row['age']
                ))
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    connection.commit()
    cursor.close()

# Add the generator function 
def stream_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
