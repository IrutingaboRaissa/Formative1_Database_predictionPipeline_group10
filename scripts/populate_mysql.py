"""
MySQL Data Population Script
Created by: Raissa
Purpose: Insert normalized student performance data into MySQL database
"""

import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MySQLDataPopulator:
    """
    Class to handle insertion of normalized data into MySQL database.
    
    This class provides methods to insert student data from pandas DataFrames
    into the student_performance_db database tables.
    """
    
    def __init__(self):
        """Initialize database configuration from environment variables."""
        self.db_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': 'student_performance_db',
            'port': int(os.getenv('MYSQL_PORT', 3306))
        }
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            print("✓ Connected to MySQL database")
            return True
        except Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ MySQL connection closed")
    
    def insert_students(self, students_df):
        """
        Insert student records into the students table.
        
        Args:
            students_df (pd.DataFrame): DataFrame with columns:
                - gender
                - learning_disabilities
                - distance_from_home
                
        Returns:
            int: Number of records inserted
        """
        if not self.connection or not self.connection.is_connected():
            print("✗ Not connected to database")
            return 0
        
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO students (gender, learning_disabilities, distance_from_home)
        VALUES (%s, %s, %s)
        """
        
        records_inserted = 0
        errors = 0
        
        print(f"\nInserting {len(students_df)} student records...")
        
        for idx, row in students_df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row['gender'],
                    row['learning_disabilities'],
                    row['distance_from_home']
                ))
                records_inserted += 1
                
                # Show progress every 1000 records
                if records_inserted % 1000 == 0:
                    print(f"  Progress: {records_inserted}/{len(students_df)} records...")
                    
            except Error as e:
                errors += 1
                if errors <= 5:  # Only show first 5 errors
                    print(f"  Error inserting record {idx}: {e}")
        
        self.connection.commit()
        cursor.close()
        
        print(f"✓ Inserted {records_inserted} students ({errors} errors)")
        return records_inserted
    
    def insert_academic_records(self, academic_df):
        """
        Insert academic records into the academic_records table.
        
        Args:
            academic_df (pd.DataFrame): DataFrame with columns:
                - student_id
                - hours_studied
                - attendance
                - previous_scores
                - tutoring_sessions
                - exam_score
                
        Returns:
            int: Number of records inserted
        """
        if not self.connection or not self.connection.is_connected():
            print("✗ Not connected to database")
            return 0
        
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO academic_records 
        (student_id, hours_studied, attendance, previous_scores, tutoring_sessions, exam_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        records_inserted = 0
        errors = 0
        
        print(f"\nInserting {len(academic_df)} academic records...")
        
        for idx, row in academic_df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row['student_id'],
                    int(row['hours_studied']),
                    int(row['attendance']),
                    int(row['previous_scores']),
                    int(row['tutoring_sessions']),
                    int(row['exam_score'])
                ))
                records_inserted += 1
                
                if records_inserted % 1000 == 0:
                    print(f"  Progress: {records_inserted}/{len(academic_df)} records...")
                    
            except Error as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error inserting record {idx}: {e}")
        
        self.connection.commit()
        cursor.close()
        
        print(f"✓ Inserted {records_inserted} academic records ({errors} errors)")
        return records_inserted
    
    def insert_environmental_factors(self, environmental_df):
        """
        Insert environmental factor records into the environmental_factors table.
        
        Args:
            environmental_df (pd.DataFrame): DataFrame with environmental data
                
        Returns:
            int: Number of records inserted
        """
        if not self.connection or not self.connection.is_connected():
            print("✗ Not connected to database")
            return 0
        
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO environmental_factors 
        (student_id, parental_involvement, access_to_resources, extracurricular_activities,
         sleep_hours, motivation_level, internet_access, family_income, teacher_quality,
         school_type, peer_influence, physical_activity, parental_education_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        records_inserted = 0
        errors = 0
        
        print(f"\nInserting {len(environmental_df)} environmental factor records...")
        
        for idx, row in environmental_df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row['student_id'],
                    row['parental_involvement'],
                    row['access_to_resources'],
                    row['extracurricular_activities'],
                    int(row['sleep_hours']),
                    row['motivation_level'],
                    row['internet_access'],
                    row['family_income'],
                    row['teacher_quality'],
                    row['school_type'],
                    row['peer_influence'],
                    int(row['physical_activity']),
                    row['parental_education_level']
                ))
                records_inserted += 1
                
                if records_inserted % 1000 == 0:
                    print(f"  Progress: {records_inserted}/{len(environmental_df)} records...")
                    
            except Error as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error inserting record {idx}: {e}")
        
        self.connection.commit()
        cursor.close()
        
        print(f"✓ Inserted {records_inserted} environmental records ({errors} errors)")
        return records_inserted
    
    def populate_all(self, students_df, academic_df, environmental_df):
        """
        Populate all tables with data.
        
        Args:
            students_df: DataFrame with student data
            academic_df: DataFrame with academic data
            environmental_df: DataFrame with environmental data
            
        Returns:
            dict: Dictionary with counts of records inserted per table
        """
        if not self.connect():
            return None
        
        print("\n" + "=" * 60)
        print("MYSQL DATABASE POPULATION")
        print("=" * 60)
        
        results = {
            'students': self.insert_students(students_df),
            'academic_records': self.insert_academic_records(academic_df),
            'environmental_factors': self.insert_environmental_factors(environmental_df)
        }
        
        total = sum(results.values())
        
        print("\n" + "=" * 60)
        print("POPULATION SUMMARY")
        print("=" * 60)
        print(f"Students: {results['students']}")
        print(f"Academic Records: {results['academic_records']}")
        print(f"Environmental Factors: {results['environmental_factors']}")
        print(f"\nTotal Records Inserted: {total}")
        
        self.close()
        return results


if __name__ == "__main__":
    print("This script should be imported and used with pandas DataFrames.")
    print("See the Jupyter notebook for usage example.")
