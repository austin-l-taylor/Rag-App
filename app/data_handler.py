import sqlite3
import pandas as pd
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

def sql_push(combined_df):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("db/chat_log.db")
    
    # Write the DataFrame to the SQL table
    try:
        combined_df.to_sql("chat_log", conn, if_exists="append", index=False)
    except Exception as e:
        print(f"An error occurred while writing to SQL: {e}")
        raise
    
    # Close the database connection
    conn.close()

def push_chat_content(chat_history):
    # Convert the chat history list to a pandas DataFrame
    chat_history_df = pd.DataFrame(chat_history)
    
    # Separate user and assistant content
    user_content = chat_history_df[chat_history_df["role"] == "user"]["content"].values
    assistant_content = chat_history_df[chat_history_df["role"] == "assistant"]["content"].values
    
    # Combine user and assistant content into a single DataFrame
    combined_df = pd.DataFrame({"user": user_content, "assistant": assistant_content})
    
    print(f"Combined Data {combined_df}")
    
    # Push the combined DataFrame to the SQLite table
    sql_push(combined_df)
    
