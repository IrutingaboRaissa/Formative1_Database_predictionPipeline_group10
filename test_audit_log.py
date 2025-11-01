import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.mysql_manager import MySQLDatabaseManager

def manual_audit_log(table_name, operation, record_id, old_values=None, new_values=None):
    """Manually insert into audit log"""
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values, changed_by, change_timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (
        table_name,
        operation,
        record_id,
        json.dumps(old_values) if old_values else None,
        json.dumps(new_values) if new_values else None,
        'test_script',
        datetime.now()
    ))
    
    conn.commit()
    log_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return log_id

def update_academic_record_with_audit(record_id, new_exam_score):
    """Update academic record and log to audit"""
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get old values
    cursor.execute("SELECT * FROM academic_records WHERE record_id = %s", (record_id,))
    old_record = cursor.fetchone()
    
    if not old_record:
        print(f"Record {record_id} not found")
        cursor.close()
        conn.close()
        return None
    
    old_score = old_record['exam_score']
    
    # Update the record
    cursor.execute(
        "UPDATE academic_records SET exam_score = %s WHERE record_id = %s",
        (new_exam_score, record_id)
    )
    
    # Get new values
    cursor.execute("SELECT * FROM academic_records WHERE record_id = %s", (record_id,))
    new_record = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Log to audit
    old_values = {
        'exam_score': old_score,
        'hours_studied': old_record['hours_studied'],
        'attendance': old_record['attendance']
    }
    
    new_values = {
        'exam_score': new_exam_score,
        'hours_studied': new_record['hours_studied'],
        'attendance': new_record['attendance']
    }
    
    log_id = manual_audit_log('academic_records', 'UPDATE', record_id, old_values, new_values)
    
    print(f"Updated record {record_id}: {old_score} -> {new_exam_score}")
    print(f"Audit log entry created: {log_id}")
    
    return log_id

def insert_test_student_with_audit():
    """Insert a new student and log to audit"""
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Insert student
    cursor.execute("""
        INSERT INTO students (gender, learning_disabilities, distance_from_home)
        VALUES (%s, %s, %s)
    """, ('Male', 'No', 'Near'))
    
    student_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Log to audit
    new_values = {
        'student_id': student_id,
        'gender': 'Male',
        'learning_disabilities': 'No',
        'distance_from_home': 'Near'
    }
    
    log_id = manual_audit_log('students', 'INSERT', student_id, None, new_values)
    
    print(f"Inserted new student: {student_id}")
    print(f"Audit log entry created: {log_id}")
    
    return student_id, log_id

def populate_audit_log():
    """Populate audit log with test operations"""
    print("\nPopulating Audit Log")
    print("=" * 70)
    
    print("\n[1] Inserting test student...")
    student_id, log_id = insert_test_student_with_audit()
    
    print("\n[2] Updating academic records...")
    # Update a few exam scores
    for record_id in [1, 2, 3, 4, 5]:
        update_academic_record_with_audit(record_id, record_id + 75)
    
    print("\n[3] Viewing audit log...")
    view_audit_log()
    
    print("\n" + "=" * 70)
    print("Audit log populated successfully!")
    print("=" * 70)

def view_audit_log():
    """View audit log entries"""
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM audit_log 
        ORDER BY change_timestamp DESC 
        LIMIT 20
    """)
    
    logs = cursor.fetchall()
    
    print(f"\nTotal audit entries: {len(logs)}")
    print("-" * 70)
    
    for log in logs:
        print(f"\nLog ID: {log['log_id']}")
        print(f"  Table: {log['table_name']}")
        print(f"  Operation: {log['operation']}")
        print(f"  Record ID: {log['record_id']}")
        print(f"  Changed By: {log['changed_by']}")
        print(f"  Timestamp: {log['change_timestamp']}")
        
        if log['old_values']:
            print(f"  Old Values: {log['old_values']}")
        if log['new_values']:
            print(f"  New Values: {log['new_values']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    populate_audit_log()
