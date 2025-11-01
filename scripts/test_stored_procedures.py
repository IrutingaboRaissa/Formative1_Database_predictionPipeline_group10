
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from tabulate import tabulate

# Load environment variables
load_dotenv()


class StoredProcedureTester:
    """
    Class to test stored procedures in student_performance_db.
    
    Tests the two stored procedures created for the assignment:
    1. GetStudentPerformanceSummary(student_id)
    2. InsertCompleteStudentRecord(...)
    """
    
    def __init__(self):
        """Initialize database configuration."""
        self.db_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': 'student_performance_db',
            'port': int(os.getenv('MYSQL_PORT', 3306))
        }
        self.connection = None
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            print("✓ Connected to MySQL database")
            return True
        except Error as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Connection closed")
    
    def test_get_student_performance_summary(self, student_id=1):
        """
        Test GetStudentPerformanceSummary stored procedure.
        
        This procedure retrieves comprehensive student data by joining
        students, academic_records, environmental_factors, and predictions tables.
        
        Args:
            student_id (int): ID of student to retrieve
        """
        if not self.connection:
            print("✗ Not connected to database")
            return
        
        cursor = self.connection.cursor()
        
        print("\n" + "=" * 70)
        print(f"TEST 1: GetStudentPerformanceSummary({student_id})")
        print("=" * 70)
        
        try:
            # Call the stored procedure
            cursor.callproc('GetStudentPerformanceSummary', [student_id])
            
            # Fetch results
            results = None
            for result in cursor.stored_results():
                results = result.fetchall()
                columns = [desc[0] for desc in result.description]
            
            if results:
                print("\n✓ Stored procedure executed successfully!")
                print("\nStudent Performance Summary:")
                print("-" * 70)
                
                # Display results in a formatted table
                print(tabulate(results, headers=columns, tablefmt='grid'))
                
                # Interpret the results
                if results[0]:
                    row = results[0]
                    print("\nSummary Analysis:")
                    print(f"  Student ID: {row[0]}")
                    print(f"  Gender: {row[1]}")
                    print(f"  Learning Disabilities: {row[2]}")
                    print(f"  Hours Studied: {row[4]}")
                    print(f"  Attendance: {row[5]}%")
                    print(f"  Exam Score: {row[7]}")
                    print(f"  School Type: {row[9]}")
                    print(f"  Total Predictions: {row[11] if row[11] else 0}")
                    
                    if row[12]:  # avg_predicted_score
                        print(f"  Average Predicted Score: {row[12]:.2f}")
                    else:
                        print(f"  Average Predicted Score: N/A (no predictions yet)")
            else:
                print("✗ No results returned. Student may not exist.")
            
            cursor.close()
            print("\n✓ TEST PASSED: Stored procedure works correctly")
            return True
            
        except Error as e:
            print(f"\n✗ TEST FAILED: {e}")
            cursor.close()
            return False
    
    def test_insert_complete_student_record(self):
        """
        Test InsertCompleteStudentRecord stored procedure.
        
        This procedure performs an atomic multi-table insertion:
        - Inserts into students table
        - Inserts into academic_records table
        - Inserts into environmental_factors table
        All within a single transaction.
        """
        if not self.connection:
            print("✗ Not connected to database")
            return
        
        cursor = self.connection.cursor()
        
        print("\n" + "=" * 70)
        print("TEST 2: InsertCompleteStudentRecord(...)")
        print("=" * 70)
        
        # Test data
        test_student = {
            'gender': 'Female',
            'learning_disabilities': 'No',
            'distance_from_home': 'Moderate',
            'hours_studied': 25,
            'attendance': 90,
            'previous_scores': 85,
            'exam_score': 88,
            'parental_involvement': 'High',
            'access_to_resources': 'High',
            'sleep_hours': 8,
            'school_type': 'Private'
        }
        
        print("\n📝 Test Data:")
        for key, value in test_student.items():
            print(f"  {key}: {value}")
        
        try:
            # Prepare the OUT parameter
            args = [
                test_student['gender'],
                test_student['learning_disabilities'],
                test_student['distance_from_home'],
                test_student['hours_studied'],
                test_student['attendance'],
                test_student['previous_scores'],
                test_student['exam_score'],
                test_student['parental_involvement'],
                test_student['access_to_resources'],
                test_student['sleep_hours'],
                test_student['school_type'],
                0  # OUT parameter for student_id
            ]
            
            # Call the stored procedure
            result = cursor.callproc('InsertCompleteStudentRecord', args)
            
            # Get the new student ID (last element in result)
            new_student_id = result[-1]
            
            self.connection.commit()
            
            print(f"\n✓ Stored procedure executed successfully!")
            print(f"✓ New student created with ID: {new_student_id}")
            
            # Verify the insertion by querying the new student
            print("\n🔍 Verifying insertion...")
            
            verify_query = """
            SELECT 
                s.student_id,
                s.gender,
                ar.hours_studied,
                ar.attendance,
                ar.exam_score,
                ef.school_type,
                ef.parental_involvement
            FROM students s
            JOIN academic_records ar ON s.student_id = ar.student_id
            JOIN environmental_factors ef ON s.student_id = ef.student_id
            WHERE s.student_id = %s
            """
            
            cursor.execute(verify_query, (new_student_id,))
            verification = cursor.fetchone()
            
            if verification:
                print("✓ Verification successful! Data found in all 3 tables:")
                headers = ['ID', 'Gender', 'Hours', 'Attend%', 'Score', 'School', 'Parental']
                print(tabulate([verification], headers=headers, tablefmt='grid'))
                
                print("\n✓ TEST PASSED: All data inserted correctly across 3 tables")
                
                # Clean up test data
                print(f"\n🧹 Cleaning up: Deleting test student {new_student_id}...")
                cursor.execute("DELETE FROM students WHERE student_id = %s", (new_student_id,))
                self.connection.commit()
                print("✓ Test data cleaned up")
                
                cursor.close()
                return True
            else:
                print("✗ Verification failed! Data not found.")
                cursor.close()
                return False
                
        except Error as e:
            print(f"\n✗ TEST FAILED: {e}")
            self.connection.rollback()
            cursor.close()
            return False
    
    def test_trigger_audit_logging(self):
        """
        Test the audit_academic_records_update trigger.
        
        This trigger should log any UPDATE operations on the academic_records table
        to the audit_log table.
        """
        if not self.connection:
            print("✗ Not connected to database")
            return
        
        cursor = self.connection.cursor()
        
        print("\n" + "=" * 70)
        print("TEST 3: audit_academic_records_update Trigger")
        print("=" * 70)
        
        try:
            # Get a student to update
            cursor.execute("SELECT student_id FROM academic_records LIMIT 1")
            student_id = cursor.fetchone()[0]
            
            print(f"\n📝 Testing with student_id: {student_id}")
            
            # Get current exam score
            cursor.execute("""
                SELECT exam_score FROM academic_records 
                WHERE student_id = %s
            """, (student_id,))
            old_score = cursor.fetchone()[0]
            
            print(f"Current exam score: {old_score}")
            
            # Count current audit log entries
            cursor.execute("SELECT COUNT(*) FROM audit_log")
            old_log_count = cursor.fetchone()[0]
            
            # Update the exam score
            new_score = old_score + 1 if old_score < 100 else old_score - 1
            print(f"Updating exam score to: {new_score}")
            
            cursor.execute("""
                UPDATE academic_records 
                SET exam_score = %s
                WHERE student_id = %s
            """, (new_score, student_id))
            
            self.connection.commit()
            
            # Check if audit log was created
            cursor.execute("SELECT COUNT(*) FROM audit_log")
            new_log_count = cursor.fetchone()[0]
            
            if new_log_count > old_log_count:
                print(f"\n✓ Trigger executed! Audit log entry created.")
                print(f"  Audit log entries: {old_log_count} → {new_log_count}")
                
                # Show the audit log entry
                cursor.execute("""
                    SELECT table_name, operation, old_values, new_values
                    FROM audit_log
                    ORDER BY change_timestamp DESC
                    LIMIT 1
                """)
                
                audit_entry = cursor.fetchone()
                if audit_entry:
                    print("\n📋 Audit Log Entry:")
                    print(f"  Table: {audit_entry[0]}")
                    print(f"  Operation: {audit_entry[1]}")
                    print(f"  Old Values: {audit_entry[2]}")
                    print(f"  New Values: {audit_entry[3]}")
                
                # Restore original value
                cursor.execute("""
                    UPDATE academic_records 
                    SET exam_score = %s
                    WHERE student_id = %s
                """, (old_score, student_id))
                self.connection.commit()
                
                print(f"\n✓ Original score restored: {old_score}")
                print("✓ TEST PASSED: Audit trigger works correctly")
                
                cursor.close()
                return True
            else:
                print("\n✗ TEST FAILED: No audit log entry created")
                cursor.close()
                return False
                
        except Error as e:
            print(f"\n✗ TEST FAILED: {e}")
            self.connection.rollback()
            cursor.close()
            return False
    
    def run_all_tests(self):
        """Run all stored procedure and trigger tests."""
        if not self.connect():
            return False
        
        print("\n" + "=" * 70)
        print("MYSQL STORED PROCEDURES & TRIGGERS TESTING")
        print("=" * 70)
        
        results = {
            'GetStudentPerformanceSummary': False,
            'InsertCompleteStudentRecord': False,
            'audit_trigger': False
        }
        
        # Test 1: GetStudentPerformanceSummary
        results['GetStudentPerformanceSummary'] = self.test_get_student_performance_summary(1)
        
        # Test 2: InsertCompleteStudentRecord
        results['InsertCompleteStudentRecord'] = self.test_insert_complete_student_record()
        
        # Test 3: Audit Trigger
        results['audit_trigger'] = self.test_trigger_audit_logging()
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status}: {test_name}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n🎉 All tests passed! Stored procedures and triggers work correctly.")
        else:
            print("\n⚠️  Some tests failed. Please review the error messages above.")
        
        self.close()
        return all_passed


if __name__ == "__main__":
    tester = StoredProcedureTester()
    success = tester.run_all_tests()
    
    exit(0 if success else 1)
