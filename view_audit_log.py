"""
View audit log entries
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.mysql_manager import MySQLDatabaseManager
from tabulate import tabulate
import json

def view_audit_log(limit=20):
    """View audit log entries in a table"""
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM audit_log 
        ORDER BY change_timestamp DESC 
        LIMIT %s
    """, (limit,))
    
    logs = cursor.fetchall()
    
    print(f"\nAudit Log Entries (showing last {len(logs)})")
    print("=" * 120)
    
    # Summary table
    table_data = []
    for log in logs:
        old_val = ''
        new_val = ''
        
        if log['old_values']:
            old_data = json.loads(log['old_values'])
            if 'exam_score' in old_data:
                old_val = f"Score: {old_data['exam_score']}"
            else:
                old_val = str(old_data)[:30]
        
        if log['new_values']:
            new_data = json.loads(log['new_values'])
            if 'exam_score' in new_data:
                new_val = f"Score: {new_data['exam_score']}"
            else:
                new_val = str(new_data)[:30]
        
        table_data.append([
            log['log_id'],
            log['table_name'],
            log['operation'],
            log['record_id'],
            old_val,
            new_val,
            log['changed_by'],
            log['change_timestamp'].strftime('%Y-%m-%d %H:%M')
        ])
    
    headers = ['Log ID', 'Table', 'Operation', 'Record', 'Old Value', 'New Value', 'Changed By', 'Timestamp']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Statistics
    cursor.execute("""
        SELECT 
            table_name,
            operation,
            COUNT(*) as count
        FROM audit_log
        GROUP BY table_name, operation
    """)
    
    stats = cursor.fetchall()
    
    print("\n\nAudit Log Statistics:")
    print("-" * 60)
    
    stats_data = [[s['table_name'], s['operation'], s['count']] for s in stats]
    print(tabulate(stats_data, headers=['Table', 'Operation', 'Count'], tablefmt='grid'))
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    limit = 20
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    view_audit_log(limit)



