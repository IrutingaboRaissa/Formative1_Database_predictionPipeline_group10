"""
Data Transformer - Converts flat dataset to normalized structure
"""
import pandas as pd


class DataTransformer:
    """Transforms flat student performance data into normalized DataFrames"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize transformer with dataset
        
        Args:
            df: Raw student performance DataFrame
        """
        self.df = df
        self.students_df = None
        self.academic_df = None
        self.environmental_df = None
    
    def transform_to_normalized(self):
        """
        Transform flat dataset into 3NF normalized structure
        
        Returns:
            Tuple of (students_df, academic_df, environmental_df)
        """
        print("\nTRANSFORMING DATASET TO NORMALIZED STRUCTURE")
        
        students_data = []
        academic_records_data = []
        environmental_factors_data = []
        
        for index, row in self.df.iterrows():
            student_id = index + 1  # Start from 1
            
            # Students table data
            students_data.append({
                'student_id': student_id,
                'gender': row['Gender'],
                'learning_disabilities': row['Learning_Disabilities'],
                'distance_from_home': row['Distance_from_Home'] if pd.notna(row['Distance_from_Home']) else 'Moderate'
            })
            
            # Academic records data
            academic_records_data.append({
                'student_id': student_id,
                'hours_studied': int(row['Hours_Studied']),
                'attendance': int(row['Attendance']), 
                'previous_scores': int(row['Previous_Scores']),
                'tutoring_sessions': int(row['Tutoring_Sessions']),
                'exam_score': int(row['Exam_Score'])
            })
            
            # Environmental factors data
            environmental_factors_data.append({
                'student_id': student_id,
                'parental_involvement': row['Parental_Involvement'],
                'access_to_resources': row['Access_to_Resources'],
                'extracurricular_activities': row['Extracurricular_Activities'],
                'sleep_hours': int(row['Sleep_Hours']),
                'motivation_level': row['Motivation_Level'],
                'internet_access': row['Internet_Access'],
                'family_income': row['Family_Income'],
                'teacher_quality': row['Teacher_Quality'] if pd.notna(row['Teacher_Quality']) else 'Medium',
                'school_type': row['School_Type'],
                'peer_influence': row['Peer_Influence'],
                'physical_activity': int(row['Physical_Activity']),
                'parental_education_level': row['Parental_Education_Level'] if pd.notna(row['Parental_Education_Level']) else 'High School'
            })
        
        # Convert to DataFrames
        self.students_df = pd.DataFrame(students_data)
        self.academic_df = pd.DataFrame(academic_records_data)
        self.environmental_df = pd.DataFrame(environmental_factors_data)
        
        print(f"✓ Data transformation completed:")
        print(f"  - Students: {len(self.students_df):,} records")
        print(f"  - Academic Records: {len(self.academic_df):,} records")
        print(f"  - Environmental Factors: {len(self.environmental_df):,} records")
        
        return self.students_df, self.academic_df, self.environmental_df
    
    def get_summary(self):
        """Get summary of transformed data"""
        if self.students_df is None:
            raise ValueError("Data not transformed yet. Call transform_to_normalized() first.")
        
        print("\nNormalized Data Summary:")
        print("-" * 70)
        print("\nStudents DataFrame:")
        print(self.students_df.head(3))
        print("\nAcademic Records DataFrame:")
        print(self.academic_df.head(3))
        print("\nEnvironmental Factors DataFrame:")
        print(self.environmental_df[['student_id', 'parental_involvement', 'school_type', 'motivation_level']].head(3))



