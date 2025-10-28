"""
MySQL Database Verification Script
Created by: Raissa
Purpose: Verify data integrity and completeness of populated MySQL database
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from tabulate import tabulate

# Load environment variables
load_dotenv()


class MySQLVerifier:
    """
    Class to verify MySQL database population and integrity.
    
    This class provides methods to check that all data was inserted correctly
    and that the database schema is functioning as expected.
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
            return True
        except Error as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def check_table_counts(self):
        """
        Check record counts in all tables.
        
        Returns:
            dict: Dictionary with table names and their record counts
        """
        if not self.connection:
            return None
        
        cursor = self.connection.cursor()
        tables = ['students', 'academic_records', 'environmental_factors', 
                 'predictions', 'audit_log']
        
        counts = {}
        
        print("\n" + "=" * 60)
        print("TABLE RECORD COUNTS")
        print("=" * 60)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            counts[table] = count
            status = "✓" if count > 0 or table in ['predictions', 'audit_log'] else "✗"
            print(f"{status} {table:25s}: {count:>6,} records")
        
        cursor.close()
        return counts
    
    def verify_referential_integrity(self):
        """
        Verify that foreign key relationships are intact.
        
        Checks that all student_id references in child tables
        exist in the students table.
        """
        if not self.connection:
            return False
        
        cursor = self.connection.cursor()
        
        print("\n" + "=" * 60)
        print("REFERENTIAL INTEGRITY CHECK")
        print("=" * 60)
        
        checks = [
            ("academic_records", "student_id"),
            ("environmental_factors", "student_id"),
            ("predictions", "student_id")
        ]
        
        all_valid = True
        
        for table, fk_column in checks:
            # Check for orphaned records
            query = f"""
            SELECT COUNT(*) 
            FROM {table} t
            LEFT JOIN students s ON t.{fk_column} = s.student_id
            WHERE s.student_id IS NULL
            """
            
            cursor.execute(query)
            orphaned = cursor.fetchone()[0]
            
            if orphaned == 0:
                print(f"✓ {table}.{fk_column} - All references valid")
            else:
                print(f"✗ {table}.{fk_column} - {orphaned} orphaned records found!")
                all_valid = False
        
        cursor.close()
        return all_valid
    
    def get_sample_data(self, limit=5):
        """
        Retrieve sample data from all tables joined together.
        
        Args:
            limit (int): Number of sample records to retrieve
            
        Returns:
            list: List of tuples with sample data
        """
        if not self.connection:
            return None
        
        cursor = self.cursor()
        
        query = """
        SELECT 
            s.student_id,
            s.gender,
            s.learning_disabilities,
            ar.hours_studied,
            ar.attendance,
            ar.exam_score,
            ef.school_type,
            ef.motivation_level,
            ef.parental_involvement
        FROM students s
        JOIN academic_records ar ON s.student_id = ar.student_id
        JOIN environmental_factors ef ON s.student_id = ef.student_id
        ORDER BY s.student_id
        LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        print("\n" + "=" * 60)
        print(f"SAMPLE DATA (First {limit} Complete Records)")
        print("=" * 60)
        
        headers = ['ID', 'Gender', 'Disabilities', 'Hours', 'Attend%', 
                  'Score', 'School', 'Motivation', 'Parental']
        
        print(tabulate(results, headers=headers, tablefmt='grid'))
        
        cursor.close()
        return results
    
    def check_data_quality(self):
        """
        Check for data quality issues like NULL values, invalid ranges, etc.
        
        Returns:
            dict: Dictionary with data quality metrics
        """
        if not self.connection:
            return None
        
        cursor = self.connection.cursor()
        
        print("\n" + "=" * 60)
        print("DATA QUALITY CHECKS")
        print("=" * 60)
        
        issues = []
        
        # Check for NULL values in required fields
        cursor.execute("SELECT COUNT(*) FROM students WHERE gender IS NULL")
        null_gender = cursor.fetchone()[0]
        if null_gender > 0:
            issues.append(f"✗ {null_gender} students with NULL gender")
        else:
            print("✓ No NULL values in students.gender")
        
        # Check exam score ranges
        cursor.execute("""
            SELECT COUNT(*) FROM academic_records 
            WHERE exam_score < 0 OR exam_score > 110
        """)
        invalid_scores = cursor.fetchone()[0]
        if invalid_scores > 0:
            issues.append(f"✗ {invalid_scores} invalid exam scores (outside 0-110 range)")
        else:
            print("✓ All exam scores within valid range (0-110)")
        
        # Check attendance ranges
        cursor.execute("""
            SELECT COUNT(*) FROM academic_records 
            WHERE attendance < 0 OR attendance > 100
        """)
        invalid_attendance = cursor.fetchone()[0]
        if invalid_attendance > 0:
            issues.append(f"✗ {invalid_attendance} invalid attendance values")
        else:
            print("✓ All attendance values within valid range (0-100)")
        
        cursor.close()
        
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("\n✓ All data quality checks passed!")
            return True
    
    def run_full_verification(self):
        """
        Run all verification checks.
        
        Returns:
            bool: True if all checks passed, False otherwise
        """
        if not self.connect():
            print("✗ Failed to connect to database")
            return False
        
        print("\n" + "=" * 60)
        print("MYSQL DATABASE VERIFICATION")
        print("=" * 60)
        
        # Check table counts
        counts = self.check_table_counts()
        
        # Verify referential integrity
        integrity_ok = self.verify_referential_integrity()
        
        # Check data quality
        quality_ok = self.check_data_quality()
        
        # Show sample data
        try:
            self.get_sample_data(3)
        except Exception as e:
            print(f"Warning: Could not retrieve sample data: {e}")
        
        # Final summary
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        
        total_records = sum([counts.get('students', 0), 
                           counts.get('academic_records', 0),
                           counts.get('environmental_factors', 0)])
        
        print(f"Total data records: {total_records:,}")
        print(f"Referential integrity: {'PASS' if integrity_ok else 'FAIL'}")
        print(f"Data quality: {'PASS' if quality_ok else 'FAIL'}")
        
        all_ok = integrity_ok and quality_ok
        
        if all_ok:
            print("\n✓ Database verification completed successfully!")
            print("  All checks passed. Database is ready for use.")
        else:
            print("\n✗ Database verification found issues!")
            print("  Please review the messages above.")
        
        self.close()
        return all_ok


if __name__ == "__main__":
    verifier = MySQLVerifier()
    success = verifier.run_full_verification()
    
    exit(0 if success else 1)
