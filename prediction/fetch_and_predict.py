"""
Prediction Script - Fetches latest student data and makes ML predictions

This script:
1. Fetches the latest student entry from the API
2. Preprocesses the data for ML model
3. Loads the trained model
4. Makes a prediction
5. Logs the prediction back to the database via API
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


class StudentDataFetcher:
    """Handles fetching student data from the API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def get_latest_student(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the latest student entry from the API
        
        Returns:
            Dictionary with complete student data or None if error
        """
        try:
            # Get all students and select the latest one
            response = requests.get(f"{self.base_url}/students/")
            response.raise_for_status()
            
            students = response.json()
            if not students:
                print("❌ No students found in database")
                return None
            
            # Get the last student (latest entry)
            latest_student = students[-1]
            student_id = latest_student['student_id']
            
            print(f"✓ Found latest student: ID {student_id}")
            
            # Fetch complete student data (with academic and environmental data)
            complete_data = self.get_complete_student_data(student_id)
            return complete_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching student data: {e}")
            return None
    
    def get_complete_student_data(self, student_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch complete student data including academic and environmental factors
        
        Args:
            student_id: Student ID to fetch
            
        Returns:
            Complete student data dictionary
        """
        try:
            response = requests.get(f"{self.base_url}/students/{student_id}/complete/")
            response.raise_for_status()
            
            student_data = response.json()
            print(f"✓ Fetched complete data for student {student_id}")
            return student_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching complete student data: {e}")
            return None
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific student by ID
        
        Args:
            student_id: Student ID to fetch
            
        Returns:
            Complete student data
        """
        return self.get_complete_student_data(student_id)


class PredictionLogger:
    """Handles logging predictions back to the database"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def log_prediction(
        self,
        student_id: int,
        predicted_score: float,
        actual_score: Optional[int] = None,
        confidence_score: float = 0.0
    ) -> bool:
        """
        Log prediction result to the database via API
        
        Args:
            student_id: Student ID
            predicted_score: Predicted exam score
            actual_score: Actual exam score (if known)
            confidence_score: Model confidence (0-1)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                "student_id": student_id,
                "predicted_score": float(predicted_score),
                "confidence_score": float(confidence_score),
                "model_version": "v1.0"
            }
            
            if actual_score is not None:
                payload["actual_score"] = int(actual_score)
            
            # TODO: Update this endpoint when predictions endpoint is added to API
            # For now, we'll print the prediction
            print(f"\nPrediction Result:")
            print(f"   Student ID: {student_id}")
            print(f"   Predicted Score: {predicted_score:.2f}")
            print(f"   Confidence: {confidence_score:.4f}")
            if actual_score:
                print(f"   Actual Score: {actual_score}")
            
            # When API endpoint is ready, uncomment this:
            # response = requests.post(
            #     f"{self.base_url}/predictions/",
            #     json=payload
            # )
            # response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error logging prediction: {e}")
            return False


def test_api_connection():
    """Test if the API is running and accessible"""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/")
        response.raise_for_status()
        print("✓ API is running and accessible")
        return True
    except requests.exceptions.RequestException:
        print("❌ API is not running. Please start the API server first:")
        print("   uvicorn app.main:app --reload")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Student Performance Prediction System")
    print("=" * 60)
    
    # Test API connection
    if not test_api_connection():
        exit(1)
    
    # Fetch latest student data
    fetcher = StudentDataFetcher()
    student_data = fetcher.get_latest_student()
    
    if student_data:
        print(f"\n✓ Successfully fetched student data")
        print(f"Student ID: {student_data.get('student_id')}")
        
        # TODO: Add preprocessing and prediction in model_loader.py
        print("\n⚠️ Next step: Implement model loading and prediction")
        print("   See: prediction/model_loader.py")
    else:
        print("\n❌ Failed to fetch student data")
