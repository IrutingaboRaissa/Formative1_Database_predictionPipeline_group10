"""
Make predictions using REAL student data from database
Shows input features and predicted output
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, 'prediction')

from database.mysql_manager import MySQLDatabaseManager
from prediction.model_loader import ModelLoader
from datetime import datetime
from tabulate import tabulate

def make_real_predictions(num_students=10):
    """Make real predictions using ML model and student data"""
    print(f"\nMaking Real Predictions for {num_students} Students")
    print("Using actual student data from database + trained ML model")
    print("=" * 100)
    
    # Load model
    print("\nStep 1: Loading trained ML model...")
    loader = ModelLoader()
    loader.load_model()
    print("Model ready\n")
    
    # Get students from database
    print(f"Step 2: Fetching {num_students} students with complete data...")
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        s.student_id, s.gender, s.learning_disabilities, s.distance_from_home,
        a.hours_studied, a.attendance, a.previous_scores, a.tutoring_sessions, a.exam_score,
        e.parental_involvement, e.access_to_resources, e.extracurricular_activities,
        e.sleep_hours, e.motivation_level, e.internet_access, e.family_income,
        e.teacher_quality, e.school_type, e.peer_influence, e.physical_activity,
        e.parental_education_level
    FROM students s
    JOIN academic_records a ON s.student_id = a.student_id
    JOIN environmental_factors e ON s.student_id = e.student_id
    WHERE a.exam_score IS NOT NULL
    LIMIT %s
    """
    
    cursor.execute(query, (num_students,))
    students = cursor.fetchall()
    print(f"Found {len(students)} students with complete data\n")
    
    print("Step 3: Making predictions using ML model...")
    print("-" * 100)
    
    predictions_data = []
    
    for i, student in enumerate(students, 1):
        student_id = student['student_id']
        
        # Show what the model sees (input features)
        print(f"\nStudent {i} (ID: {student_id}):")
        print(f"  Input Features:")
        print(f"    Hours Studied: {student['hours_studied']}")
        print(f"    Attendance: {student['attendance']}%")
        print(f"    Previous Scores: {student['previous_scores']}")
        print(f"    Tutoring Sessions: {student['tutoring_sessions']}")
        print(f"    Sleep Hours: {student['sleep_hours']}")
        print(f"    Motivation: {student['motivation_level']}")
        print(f"    Parental Involvement: {student['parental_involvement']}")
        
        # Prepare data for model
        prediction_input = {
            'Hours_Studied': student['hours_studied'],
            'Attendance': student['attendance'],
            'Previous_Scores': student['previous_scores'],
            'Tutoring_Sessions': student['tutoring_sessions'],
            'Gender': student['gender'],
            'Learning_Disabilities': student['learning_disabilities'],
            'Parental_Involvement': student['parental_involvement'],
            'Access_to_Resources': student['access_to_resources'],
            'Extracurricular_Activities': student['extracurricular_activities'],
            'Sleep_Hours': student['sleep_hours'],
            'Motivation_Level': student['motivation_level'],
            'Internet_Access': student['internet_access'],
            'Family_Income': student['family_income'],
            'Teacher_Quality': student['teacher_quality'],
            'School_Type': student['school_type'],
            'Peer_Influence': student['peer_influence'],
            'Physical_Activity': student['physical_activity'],
            'Parental_Education_Level': student['parental_education_level'],
            'Distance_from_Home': student['distance_from_home']
        }
        
        # Model makes prediction
        predicted_score, confidence = loader.predict(prediction_input)
        actual_score = student['exam_score']
        error = abs(predicted_score - actual_score)
        
        print(f"  Model Output:")
        print(f"    Predicted Exam Score: {predicted_score:.2f}")
        print(f"    Actual Exam Score: {actual_score}")
        print(f"    Prediction Error: {error:.2f} points")
        print(f"    Confidence: {confidence:.4f}")
        
        # Save to database
        insert_query = """
        INSERT INTO predictions (student_id, predicted_score, actual_score, confidence_score, prediction_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            student_id,
            predicted_score,
            actual_score,
            confidence,
            datetime.now()
        ))
        
        predictions_data.append([
            student_id,
            student['hours_studied'],
            f"{student['attendance']}%",
            student['previous_scores'],
            f"{predicted_score:.2f}",
            actual_score,
            f"{error:.2f}",
            f"{confidence:.4f}"
        ])
    
    conn.commit()
    
    # Summary table
    print("\n" + "=" * 100)
    print("PREDICTION SUMMARY")
    print("=" * 100)
    
    headers = ['Student ID', 'Hours', 'Attend', 'Prev Score', 'Predicted', 'Actual', 'Error', 'Confidence']
    print(tabulate(predictions_data, headers=headers, tablefmt='grid'))
    
    # Calculate statistics
    errors = [abs(float(row[6])) for row in predictions_data]
    avg_error = sum(errors) / len(errors)
    
    print(f"\nPrediction Statistics:")
    print(f"  Total predictions: {len(predictions_data)}")
    print(f"  Average error: {avg_error:.2f} points")
    print(f"  Min error: {min(errors):.2f} points")
    print(f"  Max error: {max(errors):.2f} points")
    
    print(f"\nAll {len(predictions_data)} predictions saved to database!")
    print("Run 'python view_predictions.py' to see all predictions")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    num = 5  # Default to 5 students for clearer output
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    make_real_predictions(num)



