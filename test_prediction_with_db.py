"""
Test script to save predictions directly to database
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, 'prediction')

from database.mysql_manager import MySQLDatabaseManager
from prediction.model_loader import ModelLoader

def save_prediction_to_db(student_id, predicted_score, confidence_score, actual_score=None):
    """Save prediction directly to predictions table"""
    db = MySQLDatabaseManager()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO predictions (student_id, predicted_score, actual_score, confidence_score, prediction_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            student_id,
            predicted_score,
            actual_score,
            confidence_score,
            datetime.now()
        ))
        
        conn.commit()
        prediction_id = cursor.lastrowid
        
        print(f"\nPrediction saved successfully!")
        print(f"  Prediction ID: {prediction_id}")
        print(f"  Student ID: {student_id}")
        print(f"  Predicted Score: {predicted_score:.2f}")
        print(f"  Confidence: {confidence_score:.4f}")
        if actual_score:
            print(f"  Actual Score: {actual_score}")
        
        cursor.close()
        return prediction_id
        
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_student_data(student_id):
    """Get complete student data from database"""
    db = MySQLDatabaseManager()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
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
        WHERE s.student_id = %s
        """
        
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        cursor.close()
        
        return result
        
    except Exception as e:
        print(f"Error getting student data: {e}")
        return None
    finally:
        if conn:
            conn.close()

def test_prediction_with_db_save():
    """Test prediction and save to database"""
    print("\nTesting Prediction with Database Save")
    print("=" * 70)
    
    # Load model
    print("\n[1/4] Loading ML model...")
    loader = ModelLoader()
    loader.load_model()
    
    # Get a student from database
    print("\n[2/4] Getting student data from database...")
    student_id = 1  # Test with student ID 1
    student_data = get_student_data(student_id)
    
    if not student_data:
        print(f"Student ID {student_id} not found in database!")
        return False
    
    print(f"Found student ID {student_id}")
    print(f"  Hours Studied: {student_data.get('hours_studied')}")
    print(f"  Attendance: {student_data.get('attendance')}%")
    print(f"  Previous Scores: {student_data.get('previous_scores')}")
    
    # Make prediction
    print("\n[3/4] Making prediction...")
    
    # Prepare data for prediction
    prediction_data = {
        'Hours_Studied': student_data.get('hours_studied'),
        'Attendance': student_data.get('attendance'),
        'Previous_Scores': student_data.get('previous_scores'),
        'Tutoring_Sessions': student_data.get('tutoring_sessions'),
        'Gender': student_data.get('gender'),
        'Learning_Disabilities': student_data.get('learning_disabilities'),
        'Parental_Involvement': student_data.get('parental_involvement'),
        'Access_to_Resources': student_data.get('access_to_resources'),
        'Extracurricular_Activities': student_data.get('extracurricular_activities'),
        'Sleep_Hours': student_data.get('sleep_hours'),
        'Motivation_Level': student_data.get('motivation_level'),
        'Internet_Access': student_data.get('internet_access'),
        'Family_Income': student_data.get('family_income'),
        'Teacher_Quality': student_data.get('teacher_quality'),
        'School_Type': student_data.get('school_type'),
        'Peer_Influence': student_data.get('peer_influence'),
        'Physical_Activity': student_data.get('physical_activity'),
        'Parental_Education_Level': student_data.get('parental_education_level'),
        'Distance_from_Home': student_data.get('distance_from_home')
    }
    
    predicted_score, confidence = loader.predict(prediction_data)
    actual_score = student_data.get('exam_score')
    
    # Save to database
    print("\n[4/4] Saving prediction to database...")
    prediction_id = save_prediction_to_db(
        student_id=student_id,
        predicted_score=predicted_score,
        confidence_score=confidence,
        actual_score=actual_score
    )
    
    if prediction_id:
        print("\n" + "=" * 70)
        print("Test completed successfully!")
        print("Check the predictions table to see the saved data")
        print("=" * 70)
        return True
    else:
        print("\nFailed to save prediction")
        return False

if __name__ == "__main__":
    success = test_prediction_with_db_save()
    sys.exit(0 if success else 1)



