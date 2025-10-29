#!/usr/bin/env python3
"""
MySQL Database Setup and Population - Entry Point
Student Performance Prediction System

Author: Raissa Irutingabo
Course: Formative 1 - Database & Prediction Pipeline
"""

import os
import sys
import pandas as pd
import kagglehub

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.mysql_manager import MySQLDatabaseManager
from database.data_populator import MySQLDataPopulator
from database.data_verifier import MySQLDataVerifier
from utils.data_transformer import DataTransformer


def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def load_dataset():
    """Load and return the student performance dataset"""
    print_header("STEP 1: LOADING DATASET")
    
    # Download dataset from Kaggle
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("lainguyn123/student-performance-factors")
    print(f"✓ Dataset downloaded to: {path}")
    
    # Load CSV
    csv_file = os.path.join(path, "StudentPerformanceFactors.csv")
    df = pd.read_csv(csv_file)
    
    print(f"✓ Dataset loaded successfully!")
    print(f"  - Shape: {df.shape}")
    print(f"  - Records: {df.shape[0]:,}")
    print(f"  - Features: {df.shape[1]}")
    
    return df


def setup_database(db_manager):
    """Setup database and schema"""
    print_header("STEP 2: DATABASE SETUP")
    
    # Create database
    db_manager.create_database()
    
    # Execute schema
    db_manager.execute_schema()
    
    # Test connection
    print("\nTesting connection...")
    db_manager.test_connection()


def transform_data(df):
    """Transform dataset to normalized structure"""
    print_header("STEP 3: DATA TRANSFORMATION")
    
    transformer = DataTransformer(df)
    students_df, academic_df, environmental_df = transformer.transform_to_normalized()
    
    # Show sample
    transformer.get_summary()
    
    return students_df, academic_df, environmental_df


def populate_database(db_manager, students_df, academic_df, environmental_df):
    """Populate database with data"""
    print_header("STEP 4: DATABASE POPULATION")
    
    populator = MySQLDataPopulator(db_manager)
    results = populator.populate_all(
        students_df, 
        academic_df, 
        environmental_df, 
        batch_size=100
    )
    
    return results


def verify_database(db_manager, expected_count):
    """Verify database integrity"""
    print_header("STEP 5: DATABASE VERIFICATION")
    
    verifier = MySQLDataVerifier(db_manager)
    results = verifier.verify_all(expected_count=expected_count)
    
    return results


def main():
    """Main execution flow"""
    print("\n" + "=" * 80)
    print("  MYSQL DATABASE SETUP - STUDENT PERFORMANCE PREDICTION SYSTEM")
    print("  Author: Raissa Irutingabo")
    print("=" * 80)
    
    try:
        # Step 1: Load dataset
        df = load_dataset()
        
        # Step 2: Initialize database manager
        db_manager = MySQLDatabaseManager()
        
        # Step 3: Setup database and schema
        setup_database(db_manager)
        
        # Step 4: Transform data to normalized structure
        students_df, academic_df, environmental_df = transform_data(df)
        
        # Step 5: Populate database
        populate_results = populate_database(db_manager, students_df, academic_df, environmental_df)
        
        # Step 6: Verify database
        verify_results = verify_database(db_manager, expected_count=len(df))
        
        # Final summary
        print_header("EXECUTION SUMMARY")
        print(f"✓ Database: {db_manager.db_name}")
        print(f"✓ Total Records Inserted: {populate_results['total']:,}")
        print(f"  - Students: {populate_results['students']:,}")
        print(f"  - Academic Records: {populate_results['academic']:,}")
        print(f"  - Environmental Factors: {populate_results['environmental']:,}")
        print(f"\n✓ Verification Status: {verify_results['status']}")
        
        if verify_results.get('integrity_issues'):
            print("\n⚠ Integrity Issues Found:")
            for issue in verify_results['integrity_issues']:
                print(f"  - {issue}")
        
        print("\n" + "=" * 80)
        print("  ✓ MYSQL DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        return 1
        
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
