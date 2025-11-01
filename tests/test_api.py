"""
Test script for API endpoints
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"

def test_create_student() -> Dict[str, Any]:
    """Test creating a new student"""
    student_data = {
        "gender": "Male",
        "learning_disabilities": "No",
        "distance_from_home": "Near"
    }
    
    response = requests.post(f"{BASE_URL}/students/", json=student_data)
    print("\nCreate Student Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_academic_record(student_id: int) -> Dict[str, Any]:
    """Test creating an academic record"""
    academic_data = {
        "student_id": student_id,
        "hours_studied": 25,
        "attendance": 85,
        "previous_scores": 78,
        "tutoring_sessions": 5,
        "exam_score": 82
    }
    
    response = requests.post(f"{BASE_URL}/students/{student_id}/academic", json=academic_data)
    print("\nCreate Academic Record Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_environmental_factors(student_id: int) -> Dict[str, Any]:
    """Test creating environmental factors"""
    env_data = {
        "student_id": student_id,
        "parental_involvement": "High",
        "access_to_resources": "Medium",
        "extracurricular_activities": "Yes",
        "sleep_hours": 8,
        "motivation_level": "High",
        "internet_access": "Yes",
        "family_income": "Medium",
        "teacher_quality": "High",
        "school_type": "Public",
        "peer_influence": "Positive",
        "physical_activity": 7,
        "parental_education_level": "College"
    }
    
    response = requests.post(f"{BASE_URL}/students/{student_id}/environmental", json=env_data)
    print("\nCreate Environmental Factors Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_get_student(student_id: int):
    """Test getting a student"""
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    print("\nGet Student Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def test_update_student(student_id: int):
    """Test updating a student"""
    update_data = {
        "distance_from_home": "Far"
    }
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=update_data)
    print("\nUpdate Student Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def run_all_tests():
    """Run all API tests"""
    print("Starting API Tests...")
    
    # Create a new student
    student = test_create_student()
    student_id = student["student_id"]
    
    # Create academic record
    test_create_academic_record(student_id)
    
    # Create environmental factors
    test_create_environmental_factors(student_id)
    
    # Get student details
    test_get_student(student_id)
    
    # Update student
    test_update_student(student_id)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()