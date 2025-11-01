import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, 'prediction')

from database.mysql_manager import MySQLDatabaseManager
from prediction.model_loader import ModelLoader

def generate_predictions(num_students=10):
    """Generate predictions for multiple students"""
    print(f"\nGenerating Predictions for {num_students} Students")
    print("=" * 70)
    
    # Load model
    print("\nLoading ML model...")
    loader = ModelLoader()
    loader.load_model()
    
    db = MySQLDatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get students
    print(f"Fetching {num_students} students from database...")
    query = """
    SELECT 
        s.*,
        a.hours_studied, a.attendance, a.previous_scores, a.tutoring_sessions, a.exam_score,
        e.parental_involvement, e.access_to_resources, e.extracurricular_activities,
        e.sleep_hours, e.motivation_level, e.internet_access, e.family_income,
        e.teacher_quality, e.school_type, e.peer_influence, e.physical_activity,
        e.parental_education_level
    FROM students s
    LEFT JOIN academic_records a ON s.student_id = a.student_id
    LEFT JOIN environmental_factors e ON s.student_id = e.student_id
    LIMIT %s
    """
    
    cursor.execute(query, (num_students,))
    students = cursor.fetchall()
    
    print(f"Found {len(students)} students\n")
    
    predictions_saved = 0
    
    for student in students:
        student_id = student['student_id']
        
        # Prepare data
        prediction_data = {
            'Hours_Studied': student.get('hours_studied'),
            'Attendance': student.get('attendance'),
            'Previous_Scores': student.get('previous_scores'),
            'Tutoring_Sessions': student.get('tutoring_sessions'),
            'Gender': student.get('gender'),
            'Learning_Disabilities': student.get('learning_disabilities'),
            'Parental_Involvement': student.get('parental_involvement'),
            'Access_to_Resources': student.get('access_to_resources'),
            'Extracurricular_Activities': student.get('extracurricular_activities'),
            'Sleep_Hours': student.get('sleep_hours'),
            'Motivation_Level': student.get('motivation_level'),
            'Internet_Access': student.get('internet_access'),
            'Family_Income': student.get('family_income'),
            'Teacher_Quality': student.get('teacher_quality'),
            'School_Type': student.get('school_type'),
            'Peer_Influence': student.get('peer_influence'),
            'Physical_Activity': student.get('physical_activity'),
            'Parental_Education_Level': student.get('parental_education_level'),
            'Distance_from_Home': student.get('distance_from_home')
        }
        
        # Make prediction
        predicted_score, confidence = loader.predict(prediction_data)
        actual_score = student.get('exam_score')
        
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
        
        predictions_saved += 1
        print(f"Student {student_id}: Predicted={predicted_score:.2f}, Actual={actual_score}, Error={abs(predicted_score - actual_score):.2f}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n{'=' * 70}")
    print(f"Successfully saved {predictions_saved} predictions to database!")
    print(f"Run 'python view_predictions.py' to see all predictions")
    print("=" * 70)

if __name__ == "__main__":
    num = 10
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    generate_predictions(num)
