from seed import connect_to_prodev

import mysql.connector

def stream_users():
    """
    Creates a generator that fetches rows from the user_data table one by one.

    This function uses a server-side cursor to fetch rows iteratively, 
    minimizing the memory footprint for large datasets.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    # Use buffered=False to enable server-side cursors (unbuffered iteration)
    # This is essential for large datasets as it prevents fetching all results 
    # into client memory at once. 
    cursor = connection.cursor(dictionary=True, buffered=False)
    
    query = "SELECT user_id, name, email, age FROM user_data"

    try:
        cursor.execute(query)
        

        for row in cursor:
            yield row
            
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        
    finally:
        cursor.close()
        connection.close()