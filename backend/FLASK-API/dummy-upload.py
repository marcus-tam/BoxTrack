from api import app, db
import os

# Path to the SQL file
sql_file_path = 'dummy-upload.sql'

# Function to execute the SQL file
def execute_sql_file(file_path):
    with app.app_context():  # Ensure the Flask app context is active
        with open(file_path, 'r') as file:
            sql_commands = file.read()  # Read the SQL file
            
        # Use a connection object to execute the SQL commands
        with db.engine.connect() as connection:
            connection.execute(sql_commands)  # Execute the SQL commands

# Run the function
if __name__ == '__main__':
    execute_sql_file(sql_file_path)
    print("SQL file executed successfully.")