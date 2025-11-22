# 0x00. Python Generators

## Project: Implementing Memory-Efficient Data Processing with Python Generators

This project focuses on leveraging Python's generator functions and the `yield` keyword to efficiently handle large datasets, implement batch processing, and simulate live data streaming scenarios. The goal is to optimize memory usage and performance in data-driven applications.

---

## 💾 Task 0: Database Seeding

This initial task involves setting up the necessary MySQL database and populating a table with sample data from a CSV file (`user_data.csv`). This groundwork is essential for the subsequent tasks involving data streaming via generators.

### File: `seed.py`

The `seed.py` module contains all the necessary functions for database connection, creation, table definition, and data insertion.

| Function Prototype | Description |
| :--- | :--- |
| `def connect_db()` | Connects to the generic MySQL server instance. |
| `def create_database(connection)` | Creates the `ALX_prodev` database if it doesn't exist. |
| `def connect_to_prodev()` | Connects specifically to the `ALX_prodev` database. |
| `def create_table(connection)` | Creates the `user_data` table with `user_id`, `name`, `email`, and `age` fields. |
| `def insert_data(connection, data_file)` | Reads the CSV file and inserts data into the `user_data` table using `executemany` for efficiency, only if the table is empty. |

### Database Schema

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | `VARCHAR(36)` | `PRIMARY KEY`, `NOT NULL` | Stores the UUID for the user. |
| `name` | `VARCHAR(255)` | `NOT NULL` | User's full name. |
| `email` | `VARCHAR(255)` | `NOT NULL` | User's email address. |
| `age` | `INT` | `NOT NULL` | User's age. |

### How to Run

1.  **Install MySQL Connector:** Ensure you have the required Python library installed:
    ```bash
    pip install mysql-connector-python
    ```
2.  **Configure Credentials:** Update the `DB_CONFIG` dictionary in `seed.py` with your local MySQL credentials (host, user, password).
3.  **Execute the Main Script:** The setup is triggered by the `0-main.py` script (provided for testing).
    ```bash
    ./0-main.py
    ```

### Expected Output

Running the main script should result in an output similar to this, confirming successful database, table, and data creation:

```text
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]