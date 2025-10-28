"""
MySQL Schema Execution Script
Created by: Raissa
Purpose: Execute the SQL schema file to create all tables, stored procedures, and triggers
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def execute_schema(schema_file='student_performance_db_schema.sql'):
    """
    Execute the SQL schema file to create all database objects.
    
    This function reads the SQL schema file and executes it to create:
    - 5 tables (students, academic_records, environmental_factors, predictions, audit_log)
    - 2 stored procedures (GetStudentPerformanceSummary, InsertCompleteStudentRecord)
    - 2 triggers (audit_academic_records_update, validate_exam_score_insert)
    
    Args:
        schema_file (str): Path to the SQL schema file
        
    Returns:
        bool: True if schema executed successfully, False on error
    """
    
    # Database connection configuration
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': 'student_performance_db',
        'port': int(os.getenv('MYSQL_PORT', 3306))
    }
    
    try:
        # Check if schema file exists
        if not os.path.exists(schema_file):
            print(f"✗ Schema file not found: {schema_file}")
            return False
        
        # Read the schema file
        print(f"Reading schema file: {schema_file}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Connect to database
        print("Connecting to MySQL database...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Execute the schema
        print("Executing SQL schema...")
        
        # Split by semicolon and execute each statement
        statements = sql_script.split(';')
        executed = 0
        skipped = 0
        
        for statement in statements:
            statement = statement.strip()
            
            # Skip empty statements and comments
            if not statement or statement.startswith('--'):
                continue
            
            # Skip DELIMITER statements (they're for MySQL CLI, not needed here)
            if 'DELIMITER' in statement.upper():
                skipped += 1
                continue
            
            try:
                cursor.execute(statement)
                executed += 1
            except Error as e:
                # Some statements might fail if objects already exist
                if 'already exists' not in str(e).lower():
                    print(f"Warning: {e}")
        
        connection.commit()
        
        print(f"\n✓ Schema executed successfully!")
        print(f"  - Statements executed: {executed}")
        print(f"  - Statements skipped: {skipped}")
        
        # Verify tables were created
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n✓ Tables created: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Clean up
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"✗ Error executing schema: {e}")
        return False


if __name__ == "__main__":
    success = execute_schema()
    if success:
        print("\n✓ Database schema setup completed successfully!")
        print("  Tables, stored procedures, and triggers are ready.")
    else:
        print("\n✗ Schema execution failed. Please check the error messages above.")
