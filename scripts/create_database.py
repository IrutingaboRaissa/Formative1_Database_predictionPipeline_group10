"""
MySQL Database Creation Script
Created by: Raissa
Purpose: Initialize student_performance_db database
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """
    Create the student_performance_db database if it doesn't exist.
    
    This function connects to MySQL server without specifying a database,
    then creates the student_performance_db database if it doesn't already exist.
    
    Returns:
        bool: True if database was created or already exists, False on error
    """
    
    # Database connection configuration
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'port': int(os.getenv('MYSQL_PORT', 3306))
    }
    
    try:
        # Connect to MySQL server (without database)
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Create database
        print("Creating database 'student_performance_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_performance_db")
        
        print("✓ Database 'student_performance_db' created successfully or already exists")
        
        # Clean up
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False


if __name__ == "__main__":
    success = create_database()
    if success:
        print("\nDatabase creation completed successfully!")
    else:
        print("\nDatabase creation failed. Please check your MySQL connection settings.")
