from seed import connect_to_prodev
import json
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from the user_data table in batches.

    Args:
        batch_size (int): The number of rows to fetch per batch.
    
    Yields:
        list: A list of user dictionaries (one batch).
    """
    connection = connect_to_prodev()
    if not connection:
        return

    # Use dictionary=True for dict output, buffered=False for better streaming 
    # (though fetchmany is typically buffered, this is good practice).
    cursor = connection.cursor(dictionary=True, buffered=False) 
    query = "SELECT user_id, name, email, age FROM user_data"

    try:
        cursor.execute(query)
        
        # Loop 1: Continues until fetchmany returns an empty list
        while True:
            # Fetch the next batch of data (up to batch_size rows)
            batch = cursor.fetchmany(batch_size)
            
            # If the batch is empty, we've reached the end of the data
            if not batch:
                break
                
            # Yield the entire list/batch of rows
            yield batch
            
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Generator that processes batches to filter users over the age of 25.

    Args:
        batch_size (int): The batch size to use for streaming data.

    Yields:
        dict: A dictionary representing a user who is older than 25.
    """
    # Loop 2: Iterates over the batches yielded by the streaming generator
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Iterates over the individual rows within the current batch
        for user in batch:
            # Filtering logic: check if 'age' is greater than 25
            if user.get('age', 0) > 25:
                # Yield the filtered user data
                yield user


# --- Execution for main script ---

# The 2-main.py script is expecting the output to be printed.
# We modify the function call to use the batch_processing generator 
# and print the results one by one.

def process_and_print(batch_size):
    """Consumes the generator and prints the results."""
    # This acts as the consuming code in 2-main.py
    for user in batch_processing(batch_size):
        # Print the user dict to stdout, matching the expected output format
        print(json.dumps(user)) 

if __name__ == '__main__':
    # Simulating the behavior of 2-main.py
    
    # NOTE: The provided 2-main.py snippet calls 'processing.batch_processing(50)'
    # We assume 'processing' is the module '1-batch_processing.py' itself.
    # The expected output suggests the batch_processing function is *both* the processor 
    # AND the final printer/yield-er. 
    # Therefore, let's assume the user wants the final function call to 
    # output the data.
    
    # We call the function and iterate over its yielded results
    # The actual 2-main.py script will look like:
    # for user in processing.batch_processing(50):
    #     print(user) # (or similar printing mechanism)

    # If you need to test locally:
    # print("--- First 5 Processed Users ---")
    # count = 0
    # for user in batch_processing(50):
    #     if count < 5:
    #         print(user)
    #         count += 1
    #     else:
    #         break
    
    pass