import mysql.connector
import csv
import uuid

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0243',
    'raise_on_warnings': True,
    'port': 3306,
    "autocommit": True,
}
DATABASE_NAME = "ALX_prodev"

def connect_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"[connect_db] Error connecting to MySQL: {err}")
        return None
    
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database {DATABASE_NAME} ensured.")
    except mysql.connector.Error as err:
        print(f"[create_database] Failed creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    prodev_config = DB_CONFIG.copy()
    prodev_config['database'] = DATABASE_NAME
    
    try:
        connection = mysql.connector.connect(**prodev_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DATABASE_NAME}: {err}")
        return None
    
def create_table(connection):
    cursor = connection.cursor()
    table_creation_query = f"""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
    """
    try:
        cursor.execute(table_creation_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, data_file):
    cursor = connection.cursor()
    
    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        if count > 0:
            print("Data already exists in user_data. Skipping insertion.")
            cursor.close()
            return
    except mysql.connector.Error as err:
        print(f"Error checking data existence: {err}")
        cursor.close()
        return

    try:
        with open(data_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row (e.g., user_id,name,email,age)
            
            rows_to_insert = []
            for row in csv_reader:
                new_uuid = str(uuid.uuid4())

                # The CSV row is already in the correct order: [user_id, name, email, age]
                # We need to convert 'age' to an integer for the INT column
                try:
                    age = int(row[2]) # Convert age from string to int
                    # rows_to_insert.append(tuple(row))
                except ValueError as e:
                    print(f"Skipping row due to invalid age: {row}. Error: {e}")
                    continue

                data_tuple = (new_uuid, row[0], row[1], age)
                rows_to_insert.append(data_tuple)
            
            # Using executemany to insert all rows in one go for efficiency
            if rows_to_insert:
                cursor.executemany(insert_query, rows_to_insert)
                connection.commit()
                print(f"Successfully inserted {cursor.rowcount} rows into user_data.")

    except FileNotFoundError:
        print(f"Error: The file {data_file} was not found.")
    except mysql.connector.Error as err:
        print(f"Failed to insert data: {err}")
        connection.rollback()
    finally:
        cursor.close()