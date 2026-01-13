import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the LPR database and table if they don't exist"""
    connection = None
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'lpr_database')}")
        cursor.execute(f"USE {os.getenv('DB_NAME', 'lpr_database')}")
        
        # Create table for license plates
        create_table_query = """
        CREATE TABLE IF NOT EXISTS license_plates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plate_number VARCHAR(20) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            confidence_score FLOAT,
            image_path VARCHAR(255),
            camera_location VARCHAR(100)
        )
        """
        cursor.execute(create_table_query)
        
        print("Database and table created successfully!")
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
