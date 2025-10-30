"""
Complete MySQL Database Setup and Population
Author: Raissa Irutingabo
"""
import os
import pandas as pd
import kagglehub
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(parent_dir, 'src'))

from database.mysql_manager import MySQLDatabaseManager
from database.data_populator import MySQLDataPopulator
from database.data_verifier import MySQLDataVerifier
from utils.data_transformer import DataTransformer


def print_header(title):
    """Print formatted section header"""
    print(f"\n{title}")


def load_dataset():
    """Load and return the student performance dataset"""
    print_header("STEP 1: LOADING DATASET")
    
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("lainguyn123/student-performance-factors")
    print(f"✓ Dataset downloaded to: {path}")
    
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
    
    db_manager.create_database()
    db_manager.execute_schema()
    
    print("\nTesting connection...")
    db_manager.test_connection()


def transform_data(df):
    """Transform dataset to normalized structure"""
    print_header("STEP 3: DATA TRANSFORMATION")
    
    transformer = DataTransformer(df)
    students_df, academic_df, environmental_df = transformer.transform_to_normalized()
    transformer.get_summary()
    
    return students_df, academic_df, environmental_df


def populate_database(db_manager, students_df, academic_df, environmental_df):
    """Populate database with data"""
    print_header("STEP 4: DATABASE POPULATION")
    
    populator = MySQLDataPopulator(db_manager)
    results = populator.populate_all(students_df, academic_df, environmental_df, batch_size=100)
    
    return results


def verify_database(db_manager, expected_count):
    """Verify database integrity"""
    print_header("STEP 5: DATABASE VERIFICATION")
    
    verifier = MySQLDataVerifier(db_manager)
    results = verifier.verify_all(expected_count=expected_count)
    
    return results


def run_complete_setup():
    """Main execution flow"""
    print("\nMYSQL DATABASE SETUP - STUDENT PERFORMANCE PREDICTION SYSTEM")
    print("Author: Raissa Irutingabo")
    
    try:
        df = load_dataset()
        db_manager = MySQLDatabaseManager()
        setup_database(db_manager)
        students_df, academic_df, environmental_df = transform_data(df)
        populate_results = populate_database(db_manager, students_df, academic_df, environmental_df)
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
        
        print("\nMYSQL DATABASE SETUP COMPLETED SUCCESSFULLY!")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        return 1
        
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
