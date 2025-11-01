"""
Test the prediction model without API
"""
import sys
import pandas as pd

sys.path.insert(0, 'prediction')

from prediction.model_loader import ModelLoader

def test_prediction():
    """Test prediction with sample student data"""
    print("\nTesting Student Performance Prediction Model")
    print("-" * 60)
    
    # Load the trained model
    print("\n[1/3] Loading ML model...")
    loader = ModelLoader()
    loader.load_model()  # Actually load the model
    
    # Create sample student data
    print("\n[2/3] Creating sample student data...")
    sample_student = {
        'Hours_Studied': 20,
        'Attendance': 85,
        'Previous_Scores': 75,
        'Tutoring_Sessions': 3,
        'Gender': 'Male',
        'Learning_Disabilities': 'No',
        'Parental_Involvement': 'High',
        'Access_to_Resources': 'Medium',
        'Extracurricular_Activities': 'Yes',
        'Sleep_Hours': 7,
        'Motivation_Level': 'High',
        'Internet_Access': 'Yes',
        'Family_Income': 'Medium',
        'Teacher_Quality': 'High',
        'School_Type': 'Public',
        'Peer_Influence': 'Positive',
        'Physical_Activity': 4,
        'Parental_Education_Level': 'College',
        'Distance_from_Home': 'Near'
    }
    
    print("Sample student profile:")
    print(f"  Hours Studied: {sample_student['Hours_Studied']}")
    print(f"  Attendance: {sample_student['Attendance']}%")
    print(f"  Previous Scores: {sample_student['Previous_Scores']}")
    print(f"  Tutoring Sessions: {sample_student['Tutoring_Sessions']}")
    print(f"  Sleep Hours: {sample_student['Sleep_Hours']}")
    
    # Make prediction
    print("\n[3/3] Making prediction...")
    prediction, confidence = loader.predict(sample_student)
    
    if prediction is not None:
        print("\nPrediction Result:")
        print(f"  Predicted Exam Score: {prediction:.2f}")
        print(f"  Confidence: {confidence:.4f}")
        print("\nPrediction test completed successfully!")
        return True
    else:
        print("\nPrediction failed!")
        return False

if __name__ == "__main__":
    success = test_prediction()
    sys.exit(0 if success else 1)



