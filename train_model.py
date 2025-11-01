"""
Train ML Model for Student Performance Prediction

This script trains a machine learning model using the student performance dataset
and saves it for use in the prediction pipeline.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os


def load_and_prepare_data():
    """
    Load the student performance dataset
    For now, we'll create sample data. Replace this with actual CSV loading.
    """
    print("Loading dataset...")
    
    # TODO: Replace with actual dataset loading
    # df = pd.read_csv('Student_performance_data.csv')
    
    # For now, create sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Learning_Disabilities': np.random.choice(['Yes', 'No'], n_samples, p=[0.2, 0.8]),
        'Distance_from_Home': np.random.choice(['Near', 'Moderate', 'Far'], n_samples),
        'Hours_Studied': np.random.randint(1, 45, n_samples),
        'Attendance': np.random.randint(60, 100, n_samples),
        'Previous_Scores': np.random.randint(40, 100, n_samples),
        'Tutoring_Sessions': np.random.randint(0, 8, n_samples),
        'Parental_Involvement': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'Access_to_Resources': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'Extracurricular_Activities': np.random.choice(['Yes', 'No'], n_samples),
        'Sleep_Hours': np.random.randint(4, 10, n_samples),
        'Motivation_Level': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'Internet_Access': np.random.choice(['Yes', 'No'], n_samples, p=[0.8, 0.2]),
        'Family_Income': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'Teacher_Quality': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'School_Type': np.random.choice(['Public', 'Private'], n_samples, p=[0.7, 0.3]),
        'Peer_Influence': np.random.choice(['Positive', 'Neutral', 'Negative'], n_samples),
        'Physical_Activity': np.random.randint(0, 6, n_samples),
        'Parental_Education_Level': np.random.choice(['High School', 'College', 'Postgraduate'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate target (exam score) based on features with some logic
    df['Exam_Score'] = (
        df['Hours_Studied'] * 0.5 +
        df['Attendance'] * 0.3 +
        df['Previous_Scores'] * 0.4 +
        df['Tutoring_Sessions'] * 2 +
        df['Sleep_Hours'] * 1.5 +
        np.random.randn(n_samples) * 5  # Add some noise
    ).clip(0, 100)
    
    print(f"✓ Loaded {len(df)} records")
    return df


def encode_features(df):
    """Encode categorical features"""
    print("🔧 Encoding categorical features...")
    
    df_encoded = df.copy()
    label_encoders = {}
    
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    for col in categorical_columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    print(f"✓ Encoded {len(categorical_columns)} categorical features")
    return df_encoded, label_encoders


def train_model(X_train, y_train):
    """Train Random Forest Regressor"""
    print("\n🤖 Training Random Forest model...")
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    print("✓ Model training completed!")
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("\n📈 Evaluating model...")
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"   R² Score: {r2:.4f}")
    print(f"   RMSE: {rmse:.2f}")
    print(f"   MAE: {mae:.2f}")
    print(f"   MSE: {mse:.2f}")
    
    return {
        'r2': r2,
        'rmse': rmse,
        'mae': mae,
        'mse': mse
    }


def save_model(model, filename='models/student_performance_model.pkl'):
    """Save trained model to file"""
    print(f"\n💾 Saving model to {filename}...")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save model
    joblib.dump(model, filename)
    
    print(f"✓ Model saved successfully!")
    print(f"   File size: {os.path.getsize(filename) / 1024:.2f} KB")


def main():
    """Main training pipeline"""
    print("=" * 70)
    print("STUDENT PERFORMANCE MODEL TRAINING")
    print("=" * 70)
    
    # Load data
    df = load_and_prepare_data()
    
    # Separate features and target
    X = df.drop('Exam_Score', axis=1)
    y = df['Exam_Score']
    
    # Encode features
    X_encoded, label_encoders = encode_features(X)
    
    # Split data
    print("\n✂️  Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Testing set: {len(X_test)} samples")
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model)
    
    # Feature importance
    print("\n🔍 Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")
    
    print("\nMODEL TRAINING COMPLETED SUCCESSFULLY!")
    print(f"\nModel saved to: models/student_performance_model.pkl")
    print(f"You can now use this model in the prediction pipeline!")


if __name__ == "__main__":
    main()
