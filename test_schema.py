"""Test schema execution only"""
import sys
sys.path.append('src')

from database.mysql_manager import MySQLDatabaseManager

def main():
    print("="*80)
    print("TESTING SCHEMA EXECUTION")
    print("="*80)
    
    # Initialize database manager
    db_manager = MySQLDatabaseManager()
    
    # Test connection
    print("\n1. Testing MySQL connection...")
    if db_manager.test_connection():
        print("✓ MySQL connection successful!")
    else:
        print("✗ MySQL connection failed!")
        return
    
    # Execute schema (this will DROP and CREATE database + tables)
    print("\n2. Executing schema...")
    if db_manager.execute_schema('schema_ddl_only.sql'):
        print("\n✓ Schema executed successfully!")
    else:
        print("\n✗ Schema execution failed!")
        return
    
    # Verify tables were created
    print("\n3. Verifying tables...")
    try:
        conn = db_manager.get_connection(include_db=True)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} tables:")
        for (table_name,) in tables:
            print(f"  - {table_name}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*80)
        print("✓ SCHEMA TEST COMPLETED SUCCESSFULLY!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error verifying tables: {e}")

if __name__ == "__main__":
    main()
