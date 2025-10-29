"""Force drop and recreate the database"""
import sys
sys.path.append('src')

from database.mysql_manager import MySQLDatabaseManager
import mysql.connector
from mysql.connector import Error

def force_reset_database():
    print("="*80)
    print("FORCE RESET DATABASE")
    print("="*80)
    print("\n⚠ This will DROP the existing database and all its data!")
    print("  Then recreate it fresh with the schema.\n")
    
    # Initialize database manager
    db_manager = MySQLDatabaseManager()
    
    try:
        # Connect WITHOUT specifying the database
        print("1. Connecting to MySQL...")
        connection = mysql.connector.connect(
            host=db_manager.config['host'],
            user=db_manager.config['user'],
            password=db_manager.config['password']
        )
        cursor = connection.cursor()
        print("  ✓ Connected to MySQL")
        
        # Force drop any connections to the database
        print("\n2. Dropping existing database...")
        cursor.execute(f"DROP DATABASE IF EXISTS student_performance_db")
        print("  ✓ Database dropped")
        
        cursor.close()
        connection.close()
        
        # Now execute the schema
        print("\n3. Executing schema to create fresh database and tables...")
        if db_manager.execute_schema('schema_ddl_only.sql'):
            print("\n" + "="*80)
            print("✓ DATABASE RESET SUCCESSFUL!")
            print("="*80)
            
            # Verify
            conn = db_manager.get_connection(include_db=True)
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\nCreated {len(tables)} tables:")
            for (table_name,) in tables:
                print(f"  - {table_name}")
            cursor.close()
            conn.close()
        else:
            print("\n✗ Schema execution failed!")
            
    except Error as e:
        print(f"\n✗ Error: {e}")
        print("\nIf you get 'Access denied' or connection errors:")
        print("1. Make sure MySQL Workbench is CLOSED")
        print("2. Check your .env file has correct password")
        print("3. Verify MySQL service is running")

if __name__ == "__main__":
    force_reset_database()
