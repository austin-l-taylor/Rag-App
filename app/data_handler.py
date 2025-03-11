import sqlite3
import os
import shutil
import pyodbc
from dotenv import load_dotenv
load_dotenv()

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

# def push_chat_content(message):
#     """summary: Pushes the chat content to the SQL database.

#     Args:
#         message (dict): The message to be pushed to the database.   
#     """
#     try:
        
#         str_server = os.getenv("SQL_SERVER")   
#         str_database = os.getenv("SQL_DATABASE")
#         username = os.getenv("SQL_USERNAME")
#         password = os.getenv("SQL_PASSWORD")

#         # Create the connection string
#         connection_string = (
#             f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#             f"SERVER={str_server};"
#             f"DATABASE={str_database};"
#             f"UID={username};"
#             f"PWD={password};"
#             "TrustServerCertificate=yes;"
#             "Encrypt=yes;"
#         )

#         connection = pyodbc.connect(connection_string)  
#         cursor  = connection.cursor()   
        
#         print("SQL Connection Established")
        
#     except Exception as e:
#         print(f"ERROR connecting to SQL Server or DB push: {e}")
