# Student Performance Prediction System

A database project that predicts student exam scores using MySQL, machine learning, and an API.

## What This Does

Takes student data (study hours, attendance, family background, etc.) and predicts their exam scores using a trained machine learning model. All the data is stored in a MySQL database and accessible through an API.

## Team members

- Raissa - MySQL database
- Mitali - Machine learning model
- Innocente - MongoDB
- Alliance - FastAPI

## Tech Stack

- MySQL - main database
- MongoDB - document storage (for comparison)
- Python - everything else
- FastAPI - API endpoints
- Random Forest - ML model

## Quick Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database:
```bash
python scripts/setup_and_populate.py
```

Note: This automatically creates tables, stored procedures, and triggers.

3. Train the model:
```bash
python train_model.py
```

4. Start the API:
```bash
uvicorn app.main:app --reload
```

API will be at: http://localhost:8000/docs

## Database Structure

5 tables (3NF normalized):
- students - basic info
- academic_records - grades and study habits
- environmental_factors - home life, resources
- predictions - ML model predictions
- audit_log - tracks changes

Everything connects through student_id.

## Stored Procedures & Triggers

**Stored Procedures:**
- `GetStudentPerformanceSummary` - Retrieves complete student data
- `InsertCompleteStudentRecord` - Atomic insert for complete student record

**Triggers:**
- `audit_academic_records_update` - Logs all academic record changes
- `audit_predictions_insert` - Logs all ML predictions

See `STORED_PROCEDURES_AND_TRIGGERS_GUIDE.md` for details.

## Making Predictions

```bash
python make_predictions.py 10
```

This runs predictions for 10 students and saves results to the database.

## Model Performance

- Accuracy: 76% (R² = 0.7630)
- Best predictors: previous scores, study hours, attendance

## Notes

- MongoDB is there for learning/comparison but not required
- MySQL does the heavy lifting
- Model trained on synthetic data so predictions aren't perfect
- **Assignment Completion:** See `ASSIGNMENT_COMPLETION_SUMMARY.md` for full report details

## Testing

```bash
# Test stored procedures and triggers
python scripts/test_stored_procedures.py

# Test predictions
python test_prediction.py

# View predictions and audit logs
python view_predictions.py
python view_audit_log.py
```

## Common Issues

**Database connection fails?**
Check .env file has correct MySQL credentials

**API won't start?**
Make sure MySQL is running and database is populated

**Model not found?**
Run train_model.py first

## Requirements

- Python 3.11+
- MySQL 8.0+
- MongoDB 6.0+ (optional)


