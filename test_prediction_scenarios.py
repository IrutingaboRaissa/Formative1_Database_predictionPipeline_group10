"""
Comprehensive Prediction Tests
Test the model with different student profiles
"""
import sys

sys.path.insert(0, 'prediction')

from prediction.model_loader import ModelLoader

def test_multiple_scenarios():
    """Test prediction with multiple student profiles"""
    print("\nComprehensive Prediction Tests")
    print("=" * 70)
    
    # Load model once
    print("\nLoading ML model...")
    loader = ModelLoader()
    loader.load_model()
    print("Model loaded successfully\n")
    
    # Test scenarios
    scenarios = [
        {
            'name': 'High Performer',
            'data': {
                'Hours_Studied': 25,
                'Attendance': 95,
                'Previous_Scores': 90,
                'Tutoring_Sessions': 5,
                'Gender': 'Female',
                'Learning_Disabilities': 'No',
                'Parental_Involvement': 'High',
                'Access_to_Resources': 'High',
                'Extracurricular_Activities': 'Yes',
                'Sleep_Hours': 8,
                'Motivation_Level': 'High',
                'Internet_Access': 'Yes',
                'Family_Income': 'High',
                'Teacher_Quality': 'High',
                'School_Type': 'Private',
                'Peer_Influence': 'Positive',
                'Physical_Activity': 5,
                'Parental_Education_Level': 'Postgraduate',
                'Distance_from_Home': 'Near'
            }
        },
        {
            'name': 'Average Student',
            'data': {
                'Hours_Studied': 15,
                'Attendance': 75,
                'Previous_Scores': 65,
                'Tutoring_Sessions': 2,
                'Gender': 'Male',
                'Learning_Disabilities': 'No',
                'Parental_Involvement': 'Medium',
                'Access_to_Resources': 'Medium',
                'Extracurricular_Activities': 'Yes',
                'Sleep_Hours': 7,
                'Motivation_Level': 'Medium',
                'Internet_Access': 'Yes',
                'Family_Income': 'Medium',
                'Teacher_Quality': 'Medium',
                'School_Type': 'Public',
                'Peer_Influence': 'Neutral',
                'Physical_Activity': 3,
                'Parental_Education_Level': 'College',
                'Distance_from_Home': 'Moderate'
            }
        },
        {
            'name': 'Struggling Student',
            'data': {
                'Hours_Studied': 5,
                'Attendance': 60,
                'Previous_Scores': 45,
                'Tutoring_Sessions': 0,
                'Gender': 'Male',
                'Learning_Disabilities': 'Yes',
                'Parental_Involvement': 'Low',
                'Access_to_Resources': 'Low',
                'Extracurricular_Activities': 'No',
                'Sleep_Hours': 5,
                'Motivation_Level': 'Low',
                'Internet_Access': 'No',
                'Family_Income': 'Low',
                'Teacher_Quality': 'Low',
                'School_Type': 'Public',
                'Peer_Influence': 'Negative',
                'Physical_Activity': 1,
                'Parental_Education_Level': 'High School',
                'Distance_from_Home': 'Far'
            }
        }
    ]
    
    # Test each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nTest {i}: {scenario['name']}")
        print("-" * 70)
        
        data = scenario['data']
        print(f"  Hours Studied: {data['Hours_Studied']}")
        print(f"  Attendance: {data['Attendance']}%")
        print(f"  Previous Scores: {data['Previous_Scores']}")
        print(f"  Learning Disabilities: {data['Learning_Disabilities']}")
        print(f"  Parental Involvement: {data['Parental_Involvement']}")
        
        prediction, confidence = loader.predict(data)
        
        print(f"\n  Predicted Score: {prediction:.2f}")
        print(f"  Confidence: {confidence:.4f}")
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    test_multiple_scenarios()



