from seed import connect_to_prodev
import mysql.connector

def stream_user_ages():
    """
    Generator that fetches and yields user ages one by one from the database.
    
    Yields:
        int: The age of a single user.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    # Use buffered=False for server-side cursor to stream results one by one
    cursor = connection.cursor(buffered=False) 
    
    # Query only the 'age' column
    query = "SELECT age FROM user_data"

    try:
        cursor.execute(query)
        
        # Loop 1: Iterates over the results being streamed from the database
        for (age,) in cursor:
            # Yield only the age (the result of the SELECT query is a tuple (age,))
            yield age
            
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        
    finally:
        # Crucial to close resources
        cursor.close()
        connection.close()


def calculate_average_age():
    """
    Calculates the average age of users by consuming the age generator.
    
    This avoids loading the entire dataset into memory.
    """
    total_age = 0
    user_count = 0

    # Loop 2: Consumes the stream of ages from the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
        # Execution pauses between ages; only one age and the two running totals 
        # (total_age, user_count) are in memory at any time.

    # Check to avoid division by zero
    if user_count > 0:
        average_age = total_age / user_count
        # Print the final result in the required format
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("Average age of users: 0.00 (No users found)")


if __name__ == '__main__':
    calculate_average_age()