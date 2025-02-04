import sqlite3
import os
import shutil

def clear_db(): 
    # Delete every file in the db folder
    folder = 'db'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def push_chat_content(message):
    """summary: Pushes the chat content to the SQL database.

    Args:
        message (dict): The message to be pushed to the database.   
    """
    #create a SQL lite database
    conn = sqlite3.connect("db/chat_log.db")    
    
    try:
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create a table if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_log (
                role TEXT,
                content TEXT
            )
            """
        )
        
        # Insert the message into the table
        cursor.execute(
            """
            INSERT INTO chat_log (role, content) VALUES (?, ?)
            """,
            (message["role"], message["content"]),
        )
        
        # Commit the changes
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"An error occurred while writing to SQL: {e}")
        raise
    
    # cursor = conn.cursor()
    # #print the contents of the database
    # cursor.execute("SELECT * FROM chat_log")
    # print(cursor.fetchall())