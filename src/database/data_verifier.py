"""
MySQL Data Verifier - Validates database integrity and data quality
"""
from mysql.connector import Error
from .mysql_manager import MySQLDatabaseManager


class MySQLDataVerifier:
    """Verifies database population and data integrity"""
    
    def __init__(self, db_manager: MySQLDatabaseManager):
        """
        Initialize data verifier
        
        Args:
            db_manager: MySQLDatabaseManager instance
        """
        self.db_manager = db_manager
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        self.connection = self.db_manager.get_connection()
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_table_counts(self):
        """
        Get record counts for all tables
        
        Returns:
            Dictionary with table counts
        """
        cursor = self.connection.cursor()
        
        tables = ['students', 'academic_records', 'environmental_factors', 'predictions', 'audit_log']
        counts = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        
        cursor.close()
        return counts
    
    def verify_referential_integrity(self):
        """Check referential integrity between tables"""
        cursor = self.connection.cursor()
        issues = []
        
        # Check orphaned academic records
        cursor.execute("""
            SELECT COUNT(*) FROM academic_records ar
            LEFT JOIN students s ON ar.student_id = s.student_id
            WHERE s.student_id IS NULL
        """)
        orphaned_academic = cursor.fetchone()[0]
        if orphaned_academic > 0:
            issues.append(f"Found {orphaned_academic} orphaned academic records")
        
        # Check orphaned environmental factors
        cursor.execute("""
            SELECT COUNT(*) FROM environmental_factors ef
            LEFT JOIN students s ON ef.student_id = s.student_id
            WHERE s.student_id IS NULL
        """)
        orphaned_env = cursor.fetchone()[0]
        if orphaned_env > 0:
            issues.append(f"Found {orphaned_env} orphaned environmental records")
        
        cursor.close()
        return issues
    
    def get_sample_data(self, limit=3):
        """
        Get sample joined data
        
        Args:
            limit: Number of sample records to retrieve
            
        Returns:
            List of sample records
        """
        cursor = self.connection.cursor()
        
        query = """
        SELECT 
            s.student_id,
            s.gender,
            s.learning_disabilities,
            ar.hours_studied,
            ar.attendance,
            ar.exam_score,
            ef.school_type,
            ef.motivation_level
        FROM students s
        JOIN academic_records ar ON s.student_id = ar.student_id
        JOIN environmental_factors ef ON s.student_id = ef.student_id
        LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def verify_all(self, expected_count=None):
        """
        Run complete verification
        
        Args:
            expected_count: Expected number of student records
            
        Returns:
            Verification results dictionary
        """
        print("\nDATABASE VERIFICATION")
        
        self.connect()
        
        try:
            # Get table counts
            counts = self.get_table_counts()
            
            print("\nTable Record Counts:")
            print("-" * 70)
            for table, count in counts.items():
                print(f"  {table:25s}: {count:,} records")
            
            # Check referential integrity
            print("\nReferential Integrity Check:")
            print("-" * 70)
            issues = self.verify_referential_integrity()
            if issues:
                for issue in issues:
                    print(f"  ✗ {issue}")
            else:
                print("  ✓ All foreign key relationships are valid")
            
            # Display sample data
            print("\nSample Data (First 3 Records):")
            print("-" * 70)
            samples = self.get_sample_data(3)
            
            print(f"{'ID':<5} {'Gender':<8} {'Disabilities':<13} {'Hours':<7} {'Attend':<7} {'Score':<7} {'School':<8} {'Motivation'}")
            print("-" * 90)
            for row in samples:
                print(f"{row[0]:<5} {row[1]:<8} {row[2]:<13} {row[3]:<7} {row[4]:<7} {row[5]:<7} {row[6]:<8} {row[7]}")
            
            # Verification summary
            print("\nVERIFICATION SUMMARY")
            
            total_records = counts['students'] + counts['academic_records'] + counts['environmental_factors']
            print(f"Total Records in Database: {total_records:,}")
            
            if expected_count:
                expected_total = expected_count * 3
                print(f"Expected Records: {expected_total:,}")
                
                if counts['students'] == expected_count:
                    print("Status: ✓ SUCCESS - All records inserted correctly")
                else:
                    print(f"Status: ✗ INCOMPLETE - Missing {expected_count - counts['students']} students")
            
            return {
                'counts': counts,
                'integrity_issues': issues,
                'total_records': total_records,
                'status': 'SUCCESS' if not issues else 'ISSUES_FOUND'
            }
            
        except Error as e:
            print(f"✗ Verification error: {e}")
            return {'status': 'ERROR', 'error': str(e)}
            
        finally:
            self.disconnect()
