"""Debug schema execution to see what SQL is being executed"""
import sys
sys.path.append('src')

# Read the schema file
with open('schema_ddl_only.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Split by semicolon
statements = sql_script.split(';')

print(f"Total statements found: {len(statements)}\n")
print("=" * 80)

for i, statement in enumerate(statements, 1):
    statement = statement.strip()
    
    print(f"\n{'-'*80}")
    print(f"Statement #{i}:")
    print(f"  Length: {len(statement)} characters")
    print(f"  Starts with '--': {statement.startswith('--')}")
    print(f"  Is empty: {len(statement) == 0}")
    
    if not statement:
        print(f"  >> SKIP (Empty)")
        continue
        
    if statement.startswith('--'):
        print(f"  >> SKIP (Comment): {statement[:50]}")
        continue
    
    # Show first 150 chars
    preview = statement.replace('\n', ' ')[:150]
    stmt_type = "UNKNOWN"
    
    if 'DROP DATABASE' in statement.upper():
        stmt_type = "DROP DATABASE"
    elif 'CREATE DATABASE' in statement.upper():
        stmt_type = "CREATE DATABASE"
    elif 'USE' in statement.upper():
        stmt_type = "USE DATABASE"
    elif 'CREATE TABLE' in statement.upper():
        stmt_type = "CREATE TABLE"
        # Extract table name
        try:
            table_part = statement.upper().split('CREATE TABLE')[1]
            table_name = table_part.split('(')[0].strip()
            stmt_type = f"CREATE TABLE {table_name}"
        except:
            pass
    
    print(f"  Type: [{stmt_type}]")
    print(f"  Preview: {preview}...")
