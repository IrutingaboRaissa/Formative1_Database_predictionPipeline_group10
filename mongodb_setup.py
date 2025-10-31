#!/usr/bin/env python3
"""
MongoDB Database Setup
This script creates MongoDB collections and populates them with student performance data
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import kagglehub
import pandas as pd

# Load environment variables
load_dotenv()

class MongoDBManager:
    """Handles MongoDB connection and database operations"""
    
    def __init__(self):
        # Get MongoDB connection details from environment variables
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.db_name = os.getenv('MONGO_DATABASE', 'student_performance_db')
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Create connection string
            connection_string = f"mongodb://{self.host}:{self.port}/"
            
            # Connect to MongoDB
            self.client = MongoClient(connection_string)
            self.db = self.client[self.db_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"Connected to MongoDB: {self.db_name}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False
    
    def drop_database(self):
        """Drop existing database to start fresh"""
        try:
            self.client.drop_database(self.db_name)
            print(f"Dropped database: {self.db_name}")
        except Exception as e:
            print(f"Error dropping database: {e}")
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")


class MongoDBPopulator:
    """Handles data insertion into MongoDB collections"""
    
    def __init__(self, db):
        self.db = db
    
    def create_collections(self):
        """Create MongoDB collections"""
        collections = ['students', 'academic_records', 'environmental_factors', 'predictions']
        
        for collection_name in collections:
            if collection_name in self.db.list_collection_names():
                self.db.drop_collection(collection_name)
            
            self.db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
    
    def populate_students(self, df):
        """Insert student records into students collection"""
        students_collection = self.db['students']
        
        # Prepare student documents
        students = []
        for idx, row in df.iterrows():
            student_doc = {
                'student_id': int(idx + 1),
                'gender': row['Gender'],
                'learning_disabilities': row['Learning_Disabilities'],
                'distance_from_home': row['Distance_from_Home']
            }
            students.append(student_doc)
        
        # Insert all students
        result = students_collection.insert_many(students)
        print(f"Inserted {len(result.inserted_ids)} students")
        return len(result.inserted_ids)
    
    def populate_academic_records(self, df):
        """Insert academic records into academic_records collection"""
        academic_collection = self.db['academic_records']
        
        # Prepare academic record documents
        records = []
        for idx, row in df.iterrows():
            record_doc = {
                'student_id': int(idx + 1),
                'hours_studied': int(row['Hours_Studied']),
                'attendance': int(row['Attendance']),
                'previous_scores': int(row['Previous_Scores']),
                'tutoring_sessions': int(row['Tutoring_Sessions']),
                'exam_score': int(row['Exam_Score'])
            }
            records.append(record_doc)
        
        # Insert all records
        result = academic_collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} academic records")
        return len(result.inserted_ids)
    
    def populate_environmental_factors(self, df):
        """Insert environmental factors into environmental_factors collection"""
        env_collection = self.db['environmental_factors']
        
        # Prepare environmental factor documents
        factors = []
        for idx, row in df.iterrows():
            factor_doc = {
                'student_id': int(idx + 1),
                'parental_involvement': row['Parental_Involvement'],
                'access_to_resources': row['Access_to_Resources'],
                'extracurricular_activities': row['Extracurricular_Activities'],
                'sleep_hours': int(row['Sleep_Hours']),
                'motivation_level': row['Motivation_Level'],
                'internet_access': row['Internet_Access'],
                'family_income': row['Family_Income'],
                'teacher_quality': row['Teacher_Quality'],
                'school_type': row['School_Type'],
                'peer_influence': row['Peer_Influence'],
                'physical_activity': int(row['Physical_Activity']),
                'parental_education_level': row['Parental_Education_Level']
            }
            factors.append(factor_doc)
        
        # Insert all factors
        result = env_collection.insert_many(factors)
        print(f"Inserted {len(result.inserted_ids)} environmental factors")
        return len(result.inserted_ids)
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        # Index on student_id for faster lookups
        self.db['students'].create_index('student_id', unique=True)
        self.db['academic_records'].create_index('student_id')
        self.db['environmental_factors'].create_index('student_id')
        
        # Index on exam_score for performance queries
        self.db['academic_records'].create_index('exam_score')
        
        print("Created indexes on collections")


class MongoDBVerifier:
    """Verifies data integrity in MongoDB"""
    
    def __init__(self, db):
        self.db = db
    
    def verify_collections(self):
        """Verify all collections were created"""
        expected_collections = ['students', 'academic_records', 'environmental_factors', 'predictions']
        actual_collections = self.db.list_collection_names()
        
        print("\nCollection Verification:")
        for collection in expected_collections:
            if collection in actual_collections:
                count = self.db[collection].count_documents({})
                print(f"  {collection}: {count} documents")
            else:
                print(f"  {collection}: MISSING")
    
    def verify_data_integrity(self):
        """Check if data is properly linked"""
        students_count = self.db['students'].count_documents({})
        academic_count = self.db['academic_records'].count_documents({})
        env_count = self.db['environmental_factors'].count_documents({})
        
        print("\nData Integrity Check:")
        print(f"  Students: {students_count}")
        print(f"  Academic Records: {academic_count}")
        print(f"  Environmental Factors: {env_count}")
        
        if students_count == academic_count == env_count:
            print("  Status: All collections have matching record counts")
        else:
            print("  Status: WARNING - Record count mismatch")
    
    def sample_query(self):
        """Run a sample query to test MongoDB functionality"""
        print("\nSample Query - Top 5 Students by Exam Score:")
        
        pipeline = [
            {
                '$lookup': {
                    'from': 'students',
                    'localField': 'student_id',
                    'foreignField': 'student_id',
                    'as': 'student_info'
                }
            },
            {'$unwind': '$student_info'},
            {'$sort': {'exam_score': -1}},
            {'$limit': 5},
            {
                '$project': {
                    'student_id': 1,
                    'exam_score': 1,
                    'hours_studied': 1,
                    'gender': '$student_info.gender'
                }
            }
        ]
        
        results = list(self.db['academic_records'].aggregate(pipeline))
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. Student {result['student_id']}: Score {result['exam_score']} "
                  f"(Studied {result['hours_studied']}h, Gender: {result['gender']})")


def load_dataset():
    """Download and load the Kaggle dataset"""
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("lainguyn123/student-performance-factors")
    csv_file = os.path.join(path, "StudentPerformanceFactors.csv")
    
    df = pd.read_csv(csv_file)
    print(f"Loaded dataset: {len(df)} records")
    return df


def main():
    """Main function to set up and populate MongoDB"""
    print("MongoDB Database Setup - Student Performance")
    print("-" * 50)
    
    # Load dataset
    df = load_dataset()
    
    # Connect to MongoDB
    mongo_manager = MongoDBManager()
    if not mongo_manager.connect():
        return 1
    
    # Drop existing database to start fresh
    mongo_manager.drop_database()
    mongo_manager.connect()  # Reconnect after drop
    
    # Create and populate collections
    populator = MongoDBPopulator(mongo_manager.db)
    populator.create_collections()
    
    print("\nPopulating collections...")
    populator.populate_students(df)
    populator.populate_academic_records(df)
    populator.populate_environmental_factors(df)
    
    # Create indexes
    populator.create_indexes()
    
    # Verify data
    verifier = MongoDBVerifier(mongo_manager.db)
    verifier.verify_collections()
    verifier.verify_data_integrity()
    verifier.sample_query()
    
    # Close connection
    mongo_manager.close()
    
    print("\nMongoDB setup completed successfully")
    return 0


if __name__ == "__main__":
    exit(main())
