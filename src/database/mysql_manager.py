
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


class MySQLDatabaseManager:

    
    def __init__(self, config_path=".env"):
       
        load_dotenv(config_path, override=True)
        
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'student_performance_db')
        }
        
        self.db_name = self.config['database']
        self._validate_config()
    
    def _validate_config(self):
      
        if not self.config['password']:
            raise ValueError(
                "MySQL password not found! Please set MYSQL_PASSWORD in .env file"
            )
        print("✓ Database configuration loaded successfully")
        print(f"  Host: {self.config['host']}")
        print(f"  User: {self.config['user']}")
        print(f"  Database: {self.db_name}")
    
    def get_connection(self, include_db=True):
       
        try:
            if include_db:
                conn = mysql.connector.connect(**self.config)
            else:
                conn = mysql.connector.connect(
                    host=self.config['host'],
                    user=self.config['user'],
                    password=self.config['password']
                )
            return conn
        except Error as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}")
    
    def create_database(self):
        print("\nCREATING DATABASE")
        
        try:
            connection = self.get_connection(include_db=False)
            cursor = connection.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            print(f"✓ Database '{self.db_name}' created or already exists")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            print(f"✗ Error creating database: {e}")
            raise
    
    def execute_schema(self, schema_file='schema_ddl_only.sql'):
       
        print("\nEXECUTING DATABASE SCHEMA")
        
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        try:
            # Connect WITHOUT selecting database (so we can DROP/CREATE it)
            connection = self.get_connection(include_db=False)
            cursor = connection.cursor()
            
            # Read schema file
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            tables_created = 0
            database_dropped = False
            database_created = False
            
            for statement in statements:
                statement = statement.strip()
                
                # Skip empty statements
                if not statement:
                    continue
                
              
                lines = statement.split('\n')
                sql_lines = []
                for line in lines:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    if line.startswith('--'):  # Skip comment-only lines
                        continue
                    sql_lines.append(line)

               
                if sql_lines and sql_lines[0].startswith('--'):
                    sql_lines[0] = sql_lines[0][2:].strip()

                clean_statement = '\n'.join(sql_lines)
                
                # Skip if nothing left after removing comments
                if not clean_statement:
                    continue
                
                try:
                    cursor.execute(clean_statement)
                    
                    # Track operations
                    if 'DROP DATABASE' in clean_statement.upper():
                        database_dropped = True
                        print(f"  Dropped existing database")
                    elif 'CREATE DATABASE' in clean_statement.upper():
                        database_created = True
                        print(f"  Created database: student_performance_db")
                    elif 'USE' in clean_statement.upper():
                        print(f"  Selected database: student_performance_db")
                    elif 'CREATE TABLE' in clean_statement.upper():
                        # Extract table name
                        table_part = clean_statement.upper().split('CREATE TABLE')[1]
                        table_name = table_part.split('(')[0].strip()
                        print(f"  Created table: {table_name}")
                        tables_created += 1
                        
                except Error as e:
                    error_msg = str(e).lower()
                    # Show warnings for database operations that fail
                    if 'drop database' in clean_statement.lower() or 'create database' in clean_statement.lower():
                        print(f" Database operation: {e}")
                        # If can't drop, likely because it's in use
                        if 'drop' in clean_statement.lower():
                            print(f" Database may be in use - close MySQL Workbench and try again")
                    elif 'already exists' not in error_msg:
                        print(f"  Warning: {e}")
            
            connection.commit()
            
            if tables_created == 0:
                print(f"\nWARNING: No tables were created!")
                print(f" Database dropped: {database_dropped}")
                print(f" Database created: {database_created}")
            else:
                print(f"\nSchema executed successfully! ({tables_created} tables created)")

            cursor.close()
            connection.close()
            return tables_created > 0
            
        except Error as e:
            print(f"Error executing schema: {e}")
            raise
    
    def drop_database(self):
    
        try:
            connection = self.get_connection(include_db=False)
            cursor = connection.cursor()
            
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            print(f" Database '{self.db_name}' dropped successfully")
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(f"Error dropping database: {e}")
            raise
    
    def execute_procedures_and_triggers(self, procedures_file='stored_procedures_and_triggers.sql'):
        """Execute stored procedures and triggers from SQL file"""
        print("\nEXECUTING STORED PROCEDURES AND TRIGGERS")
        
        if not os.path.exists(procedures_file):
            print(f"⚠ Warning: {procedures_file} not found - skipping procedures/triggers")
            return False
        
        try:
            connection = self.get_connection(include_db=True)
            cursor = connection.cursor()
            
            # Read procedures file
            with open(procedures_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Split by DELIMITER to handle procedure/trigger definitions
            # Replace DELIMITER statements and split properly
            sql_script = sql_script.replace('DELIMITER //', '<<<DELIM>>>')
            sql_script = sql_script.replace('DELIMITER ;', '<<<ENDDELIM>>>')
            
            parts = sql_script.split('<<<DELIM>>>')
            
            procedures_created = 0
            triggers_created = 0
            
            for part in parts:
                if '<<<ENDDELIM>>>' in part:
                    # This is a procedure/trigger definition
                    proc_def = part.split('<<<ENDDELIM>>>')[0].strip()
                    
                    if proc_def and not proc_def.startswith('--'):
                        try:
                            # Execute the procedure/trigger
                            cursor.execute(proc_def)
                            
                            if 'CREATE PROCEDURE' in proc_def.upper():
                                proc_name = proc_def.split('PROCEDURE')[1].split('(')[0].strip()
                                print(f"  ✓ Created procedure: {proc_name}")
                                procedures_created += 1
                            elif 'CREATE TRIGGER' in proc_def.upper():
                                trigger_name = proc_def.split('TRIGGER')[1].split('\n')[0].strip()
                                print(f"  ✓ Created trigger: {trigger_name}")
                                triggers_created += 1
                        except Error as e:
                            if 'already exists' not in str(e).lower():
                                print(f"  ⚠ Warning: {e}")
                else:
                    # Regular SQL statements (DROP statements, etc.)
                    statements = part.split(';')
                    for stmt in statements:
                        stmt = stmt.strip()
                        if stmt and not stmt.startswith('--') and 'USE ' not in stmt.upper() and 'SELECT' not in stmt.upper():
                            try:
                                cursor.execute(stmt)
                            except Error as e:
                                # Silently skip DROP statements for non-existent objects
                                if 'does not exist' not in str(e).lower() and 'unknown' not in str(e).lower():
                                    print(f"  ⚠ {e}")
            
            connection.commit()
            
            print(f"\n✓ Procedures & Triggers setup complete!")
            print(f"  - Stored Procedures: {procedures_created}")
            print(f"  - Triggers: {triggers_created}")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            print(f"✗ Error executing procedures/triggers: {e}")
            return False
    
    def test_connection(self):
        try:
            connection = self.get_connection(include_db=True)
            cursor = connection.cursor()
            
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            
            print(f"✓ Connected to database: {db_name}")
            print(f"  MySQL version: {version}")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            print(f"✗ Connection test failed: {e}")
            return False



