# Student Performance Prediction System

A database project that predicts student exam scores using MySQL, machine learning, and an API.

## What This Does

Takes student data (study hours, attendance, family background, etc.) and predicts their exam scores using a trained machine learning model. All the data is stored in a MySQL database and accessible through an API.

## Team

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

5 tables:
- students - basic info
- academic_records - grades and study habits
- environmental_factors - home life, resources
- predictions - ML model predictions
- audit_log - tracks changes

Everything connects through student_id.

## Making Predictions

```bash
python make_predictions.py 10
```

This runs predictions for 10 students and saves results to the database.

## Project Structure

```
├── src/              - database classes
├── app/              - FastAPI code
├── mongodb/          - MongoDB stuff
├── prediction/       - ML pipeline
├── scripts/          - setup and test scripts
├── models/           - trained model file
└── schema_ddl_only.sql - database schema
```

## Model Performance

- Accuracy: 76% (R² = 0.7630)
- Best predictors: previous scores, study hours, attendance

## Notes

- MongoDB is there for learning/comparison but not required
- MySQL does the heavy lifting
- Model trained on synthetic data so predictions aren't perfect
- Check PROJECT_REPORT.md for full details

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

---

Made for Database Systems course - Fall 2024
