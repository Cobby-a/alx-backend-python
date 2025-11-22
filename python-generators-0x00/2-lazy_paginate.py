import mysql.connector
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.

    Args:
        page_size (int): The maximum number of rows to return.
        offset (int): The starting row index for the fetch.

    Returns:
        list: A list of user dictionaries.
    """
    connection = connect_to_prodev()
    if not connection:
        return []
        
    cursor = connection.cursor(dictionary=True)
    
    # SQL query using LIMIT (page_size) and OFFSET (offset) for pagination
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()


def lazy_pagination(page_size):
    """
    Generator that lazily loads pages of user data from the database.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list: A page (list of user dictionaries) of data.
    """
    # Start at the beginning of the table
    offset = 0
    
    # Only ONE loop is allowed
    while True:
        # 1. Fetch the next page of data
        page = paginate_users(page_size, offset)
        
        # 2. Termination condition: If the page is empty, we've reached the end
        if not page:
            break
            
        # 3. Yield the entire page (a list of dictionaries)
        # Execution pauses here until the next page is requested
        yield page
        
        # 4. Update the offset for the next page fetch
        offset += page_size