# Prediction Module

**Author:** Mitali  
**Purpose:** Fetch student data from API and make ML predictions

## 📋 Overview

This module implements Task 3 of the assignment: Create a script to fetch data for prediction.

### Features:
1. ✅ Fetches latest student entry from database via API
2. ✅ Handles missing data and edge cases
3. ✅ Loads pre-trained ML model
4. ✅ Preprocesses data for prediction
5. ✅ Makes predictions using the model
6. ✅ Logs prediction results

## 📁 Files

```
prediction/
├── __init__.py              # Main prediction pipeline
├── fetch_and_predict.py     # API data fetching and logging
├── model_loader.py          # ML model loading and preprocessing
└── README.md               # This file
```

## 🚀 Usage

### Prerequisites

1. **API must be running:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Database must be populated with student data**

3. **ML model file** (optional - will use dummy model for testing)
   - Place your trained model in `models/student_performance_model.pkl`
   - Or `.joblib` format

### Run Prediction Pipeline

#### Option 1: Predict for latest student
```bash
python -m prediction
```

#### Option 2: Predict for specific student ID
```bash
python -m prediction 123
```

#### Option 3: Test individual components

**Test data fetching:**
```bash
python prediction/fetch_and_predict.py
```

**Test model loading:**
```bash
python prediction/model_loader.py
```

## 🔧 Configuration

Edit `.env` file:
```env
API_BASE_URL=http://localhost:8000/api
```

## 📊 How It Works

### 1. Data Fetching (`fetch_and_predict.py`)

```python
fetcher = StudentDataFetcher()
student_data = fetcher.get_latest_student()
```

**API Endpoints Used:**
- `GET /api/students/` - Get all students
- `GET /api/students/{id}/complete/` - Get complete student data

### 2. Data Preprocessing (`model_loader.py`)

```python
preprocessor = DataPreprocessor()
df = preprocessor.prepare_features(student_data)
df = preprocessor.handle_missing_values(df)
df = preprocessor.encode_categorical_features(df)
```

**Features prepared:**
- Demographics: Gender, Learning Disabilities, Distance from Home
- Academic: Hours Studied, Attendance, Previous Scores, Tutoring Sessions
- Environmental: 13 factors (sleep, motivation, resources, etc.)

### 3. Model Prediction

```python
loader = ModelLoader()
loader.load_model()
predicted_score, confidence = loader.predict(student_data)
```

### 4. Logging Results

```python
logger = PredictionLogger()
logger.log_prediction(student_id, predicted_score, actual_score, confidence)
```

## 🧪 Testing

### Test with Dummy Model

If you don't have a trained model yet:

```bash
python prediction/model_loader.py
```

This creates a simple RandomForest model for testing.

### Test API Connection

```bash
python prediction/fetch_and_predict.py
```

## 📝 Adding Your ML Model

### From Intro to ML Course

1. **Export your trained model:**
   ```python
   import joblib
   joblib.dump(model, 'models/student_performance_model.pkl')
   ```

2. **Or use pickle:**
   ```python
   import pickle
   with open('models/student_performance_model.pkl', 'wb') as f:
       pickle.dump(model, f)
   ```

3. **Model requirements:**
   - Must accept 19 features
   - Should predict exam scores (0-110)
   - Can be any scikit-learn model (RandomForest, LinearRegression, etc.)

### Features Expected by Model

The model should expect these 19 features in order:
1. Gender (encoded)
2. Learning_Disabilities (encoded)
3. Distance_from_Home (encoded)
4. Hours_Studied
5. Attendance
6. Previous_Scores
7. Tutoring_Sessions
8. Parental_Involvement (encoded)
9. Access_to_Resources (encoded)
10. Extracurricular_Activities (encoded)
11. Sleep_Hours
12. Motivation_Level (encoded)
13. Internet_Access (encoded)
14. Family_Income (encoded)
15. Teacher_Quality (encoded)
16. School_Type (encoded)
17. Peer_Influence (encoded)
18. Physical_Activity
19. Parental_Education_Level (encoded)

## 🐛 Error Handling

The pipeline handles:
- ✅ API connection failures
- ✅ Missing student data
- ✅ Model loading errors
- ✅ Missing feature values
- ✅ Invalid predictions
- ✅ Database logging failures

## 📈 Expected Output

```
======================================================================
STUDENT PERFORMANCE PREDICTION PIPELINE
======================================================================

[1/5] Checking API connection...
✓ API is running and accessible

[2/5] Fetching student data...
✓ Found latest student: ID 123
✓ Fetched complete data for student 123
✓ Fetched data for Student ID: 123

[3/5] Loading ML model...
✓ Model loaded successfully from models/student_performance_model.pkl

[4/5] Making prediction...
✓ Prediction completed successfully

[5/5] Logging prediction to database...

📊 Prediction Result:
   Student ID: 123
   Predicted Score: 78.45
   Confidence: 0.8734
   Actual Score: 80

======================================================================
✅ PREDICTION PIPELINE COMPLETED SUCCESSFULLY
======================================================================
```

## 🎯 Assignment Requirements Met

- ✅ Fetch latest entry from database via API
- ✅ Load pre-trained ML model
- ✅ Preprocess data for prediction
- ✅ Make prediction using model
- ✅ Log prediction result back to database
- ✅ Handle missing data and edge cases

## 📚 Dependencies

All dependencies are in `requirements.txt`:
```
requests==2.31.0
pandas==2.1.4
numpy==1.25.2
scikit-learn==1.3.2
joblib==1.3.2
python-dotenv==1.0.0
```

## 🔗 Related Files

- API Routes: `app/api/routes.py`
- Database Schema: `schema_ddl_only.sql`
- Requirements: `requirements.txt`

## 👥 Team Member

**Mitali** - Prediction Script Implementation

---

**Questions?** Check the main project README or ask in the group chat!
