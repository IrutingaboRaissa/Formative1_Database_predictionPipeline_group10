"""
ML Model Loader and Predictor

This module handles:
1. Loading the trained ML model
2. Preprocessing student data for prediction
3. Making predictions
4. Handling missing data

Author: Mitali
Date: October 30, 2025
"""

import joblib
import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from sklearn.preprocessing import LabelEncoder
import os


class DataPreprocessor:
    """Handles data preprocessing for ML predictions"""
    
    def __init__(self):
        self.label_encoders = {}
        self.feature_columns = None
    
    def prepare_features(self, student_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare student data for model prediction
        
        Args:
            student_data: Complete student data from API
            
        Returns:
            DataFrame with preprocessed features
        """
        # Extract relevant features
        features = {}
        
        # Student demographics
        features['Gender'] = student_data.get('gender', 'Male')
        features['Learning_Disabilities'] = student_data.get('learning_disabilities', 'No')
        features['Distance_from_Home'] = student_data.get('distance_from_home', 'Moderate')
        
        # Academic data
        academic = student_data.get('academic_record', {})
        features['Hours_Studied'] = academic.get('hours_studied', 0)
        features['Attendance'] = academic.get('attendance', 0)
        features['Previous_Scores'] = academic.get('previous_scores', 0)
        features['Tutoring_Sessions'] = academic.get('tutoring_sessions', 0)
        
        # Environmental factors
        env = student_data.get('environmental_factors', {})
        features['Parental_Involvement'] = env.get('parental_involvement', 'Medium')
        features['Access_to_Resources'] = env.get('access_to_resources', 'Medium')
        features['Extracurricular_Activities'] = env.get('extracurricular_activities', 'No')
        features['Sleep_Hours'] = env.get('sleep_hours', 7)
        features['Motivation_Level'] = env.get('motivation_level', 'Medium')
        features['Internet_Access'] = env.get('internet_access', 'Yes')
        features['Family_Income'] = env.get('family_income', 'Medium')
        features['Teacher_Quality'] = env.get('teacher_quality', 'Medium')
        features['School_Type'] = env.get('school_type', 'Public')
        features['Peer_Influence'] = env.get('peer_influence', 'Neutral')
        features['Physical_Activity'] = env.get('physical_activity', 0)
        features['Parental_Education_Level'] = env.get('parental_education_level', 'High School')
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical features using Label Encoding
        
        Args:
            df: DataFrame with features
            
        Returns:
            DataFrame with encoded features
        """
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
            else:
                # Handle unseen labels
                le = self.label_encoders[col]
                df[col] = df[col].apply(
                    lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else -1
                )
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the data
        
        Args:
            df: DataFrame with potential missing values
            
        Returns:
            DataFrame with handled missing values
        """
        # Fill numeric columns with median
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        return df


class ModelLoader:
    """Handles loading and using the trained ML model"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize model loader
        
        Args:
            model_path: Path to the trained model file (.pkl or .joblib)
        """
        self.model_path = model_path or os.path.join('models', 'student_performance_model.pkl')
        self.model = None
        self.preprocessor = DataPreprocessor()
    
    def load_model(self) -> bool:
        """
        Load the trained model from file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.model_path):
                print(f"⚠️  Model file not found: {self.model_path}")
                print("   Please train a model first and save it to this location")
                return False
            
            # Try loading with joblib first, then pickle
            try:
                self.model = joblib.load(self.model_path)
            except:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            
            print(f"✓ Model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def predict(self, student_data: Dict[str, Any]) -> Tuple[float, float]:
        """
        Make a prediction for a student
        
        Args:
            student_data: Complete student data from API
            
        Returns:
            Tuple of (predicted_score, confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Preprocess data
        df = self.preprocessor.prepare_features(student_data)
        df = self.preprocessor.handle_missing_values(df)
        df = self.preprocessor.encode_categorical_features(df)
        
        # Make prediction
        predicted_score = self.model.predict(df)[0]
        
        # Calculate confidence (if model supports predict_proba)
        try:
            probabilities = self.model.predict_proba(df)
            confidence = np.max(probabilities)
        except AttributeError:
            # For regression models, use R² score or set default confidence
            confidence = 0.85  # Default confidence
        
        return float(predicted_score), float(confidence)
    
    def create_dummy_model(self):
        """
        Create a simple dummy model for testing purposes
        This is a placeholder until you add your real model from Intro to ML
        """
        from sklearn.ensemble import RandomForestRegressor
        
        print("⚠️  Creating dummy model for testing...")
        print("   Replace this with your actual trained model!")
        
        # Simple dummy model (replace with your actual model)
        self.model = RandomForestRegressor(n_estimators=10, random_state=42)
        
        # Create dummy training data
        X_dummy = np.random.rand(100, 19)  # 19 features
        y_dummy = np.random.randint(50, 100, 100)  # Exam scores 50-100
        
        self.model.fit(X_dummy, y_dummy)
        print("✓ Dummy model created (for testing only)")


def test_prediction():
    """Test the prediction pipeline with sample data"""
    print("\n" + "=" * 60)
    print("Testing Prediction Pipeline")
    print("=" * 60)
    
    # Sample student data
    sample_student = {
        "student_id": 1,
        "gender": "Male",
        "learning_disabilities": "No",
        "distance_from_home": "Near",
        "academic_record": {
            "hours_studied": 20,
            "attendance": 85,
            "previous_scores": 75,
            "tutoring_sessions": 3
        },
        "environmental_factors": {
            "parental_involvement": "High",
            "access_to_resources": "High",
            "extracurricular_activities": "Yes",
            "sleep_hours": 7,
            "motivation_level": "High",
            "internet_access": "Yes",
            "family_income": "Medium",
            "teacher_quality": "High",
            "school_type": "Private",
            "peer_influence": "Positive",
            "physical_activity": 5,
            "parental_education_level": "College"
        }
    }
    
    # Load model
    loader = ModelLoader()
    
    if not loader.load_model():
        print("\n⚠️  Using dummy model for testing...")
        loader.create_dummy_model()
    
    # Make prediction
    try:
        predicted_score, confidence = loader.predict(sample_student)
        print(f"\n✓ Prediction successful!")
        print(f"   Predicted Exam Score: {predicted_score:.2f}")
        print(f"   Confidence: {confidence:.4f}")
    except Exception as e:
        print(f"\n❌ Prediction failed: {e}")


if __name__ == "__main__":
    test_prediction()
