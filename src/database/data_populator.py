"""
MySQL Data Populator - Handles batch insertion of normalized data
"""
import pandas as pd
from mysql.connector import Error
from .mysql_manager import MySQLDatabaseManager


class MySQLDataPopulator:
    """Handles batch insertion of student performance data into MySQL"""
    
    def __init__(self, db_manager: MySQLDatabaseManager):
        """
        Initialize data populator
        
        Args:
            db_manager: MySQLDatabaseManager instance
        """
        self.db_manager = db_manager
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        self.connection = self.db_manager.get_connection()
        print("✓ Connected to database for data population")
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def insert_students_batch(self, students_df: pd.DataFrame, batch_size=100):
        """
        Insert student records in batches
        
        Args:
            students_df: DataFrame with student data
            batch_size: Number of records per batch
            
        Returns:
            Number of records inserted
        """
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO students (gender, learning_disabilities, distance_from_home)
        VALUES (%s, %s, %s)
        """
        
        total_records = len(students_df)
        records_inserted = 0
        
        print(f"\nInserting {total_records} students in batches of {batch_size}...")
        
        for start_idx in range(0, total_records, batch_size):
            end_idx = min(start_idx + batch_size, total_records)
            batch = students_df.iloc[start_idx:end_idx]
            
            batch_count = 0
            for _, row in batch.iterrows():
                try:
                    cursor.execute(insert_query, (
                        row['gender'],
                        row['learning_disabilities'],
                        row['distance_from_home']
                    ))
                    batch_count += 1
                except Error as e:
                    print(f"  Error in row {start_idx + batch_count}: {e}")
            
            self.connection.commit()
            records_inserted += batch_count
            batch_num = start_idx // batch_size + 1
            print(f"  Batch {batch_num}: {batch_count}/{len(batch)} records (Total: {records_inserted}/{total_records})")
        
        cursor.close()
        print(f"✓ Total students inserted: {records_inserted}")
        return records_inserted
    
    def insert_academic_records_batch(self, academic_df: pd.DataFrame, batch_size=100):
        """
        Insert academic records in batches
        
        Args:
            academic_df: DataFrame with academic data
            batch_size: Number of records per batch
            
        Returns:
            Number of records inserted
        """
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO academic_records 
        (student_id, hours_studied, attendance, previous_scores, tutoring_sessions, exam_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        total_records = len(academic_df)
        records_inserted = 0
        
        print(f"\nInserting {total_records} academic records in batches of {batch_size}...")
        
        for start_idx in range(0, total_records, batch_size):
            end_idx = min(start_idx + batch_size, total_records)
            batch = academic_df.iloc[start_idx:end_idx]
            
            batch_count = 0
            for _, row in batch.iterrows():
                try:
                    cursor.execute(insert_query, (
                        int(row['student_id']),
                        int(row['hours_studied']),
                        int(row['attendance']),
                        int(row['previous_scores']),
                        int(row['tutoring_sessions']),
                        int(row['exam_score'])
                    ))
                    batch_count += 1
                except Error as e:
                    print(f"  Error in row {start_idx + batch_count}: {e}")
            
            self.connection.commit()
            records_inserted += batch_count
            batch_num = start_idx // batch_size + 1
            print(f"  Batch {batch_num}: {batch_count}/{len(batch)} records (Total: {records_inserted}/{total_records})")
        
        cursor.close()
        print(f"✓ Total academic records inserted: {records_inserted}")
        return records_inserted
    
    def insert_environmental_factors_batch(self, environmental_df: pd.DataFrame, batch_size=100):
        """
        Insert environmental factors in batches
        
        Args:
            environmental_df: DataFrame with environmental data
            batch_size: Number of records per batch
            
        Returns:
            Number of records inserted
        """
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO environmental_factors 
        (student_id, parental_involvement, access_to_resources, extracurricular_activities,
         sleep_hours, motivation_level, internet_access, family_income, teacher_quality,
         school_type, peer_influence, physical_activity, parental_education_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        total_records = len(environmental_df)
        records_inserted = 0
        
        print(f"\nInserting {total_records} environmental records in batches of {batch_size}...")
        
        for start_idx in range(0, total_records, batch_size):
            end_idx = min(start_idx + batch_size, total_records)
            batch = environmental_df.iloc[start_idx:end_idx]
            
            batch_count = 0
            for _, row in batch.iterrows():
                try:
                    cursor.execute(insert_query, (
                        int(row['student_id']),
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
                    batch_count += 1
                except Error as e:
                    print(f"  Error in row {start_idx + batch_count}: {e}")
            
            self.connection.commit()
            records_inserted += batch_count
            batch_num = start_idx // batch_size + 1
            print(f"  Batch {batch_num}: {batch_count}/{len(batch)} records (Total: {records_inserted}/{total_records})")
        
        cursor.close()
        print(f"✓ Total environmental records inserted: {records_inserted}")
        return records_inserted
    
    def populate_all(self, students_df: pd.DataFrame, academic_df: pd.DataFrame, 
                     environmental_df: pd.DataFrame, batch_size=100):
        """
        Populate all tables with data
        
        Args:
            students_df: Students DataFrame
            academic_df: Academic records DataFrame
            environmental_df: Environmental factors DataFrame
            batch_size: Batch size for insertions
            
        Returns:
            Dictionary with insertion counts
        """
        print("\nMYSQL DATABASE POPULATION (BATCH MODE)")
        
        self.connect()
        
        try:
            # Insert students
            print("\n1. STUDENTS TABLE")
            print("-" * 70)
            students_count = self.insert_students_batch(students_df, batch_size)
            
            # Insert academic records
            print("\n2. ACADEMIC RECORDS TABLE")
            print("-" * 70)
            academic_count = self.insert_academic_records_batch(academic_df, batch_size)
            
            # Insert environmental factors
            print("\n3. ENVIRONMENTAL FACTORS TABLE")
            print("-" * 70)
            env_count = self.insert_environmental_factors_batch(environmental_df, batch_size)
            
            print("\nDATABASE POPULATION COMPLETED!")
            print(f"Total records inserted: {students_count + academic_count + env_count}")
            print(f"  - Students: {students_count}")
            print(f"  - Academic Records: {academic_count}")
            print(f"  - Environmental Factors: {env_count}")
            
            return {
                'students': students_count,
                'academic': academic_count,
                'environmental': env_count,
                'total': students_count + academic_count + env_count
            }
            
        finally:
            self.disconnect()
