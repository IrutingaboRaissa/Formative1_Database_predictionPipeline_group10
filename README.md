# Formative 1: Database & Prediction Pipeline

Student Performance Prediction System with 3NF Normalized Database, FastAPI, and Machine Learning

## Project Overview

This project implements a comprehensive database system for analyzing and predicting student performance using:
- **MySQL Database** with 3NF normalized schema
- **MongoDB** for NoSQL storage
- **FastAPI** REST API for CRUD operations
- **Machine Learning** prediction pipeline using scikit-learn
- **Student Performance Factors** dataset from Kaggle

## Database Schema

### MySQL Tables (3NF Normalized)
1. **students** - Student demographic information
2. **academic_records** - Academic performance data
3. **environmental_factors** - Environmental and social factors
4. **predictions** - ML prediction results
5. **audit_log** - Change tracking

### Stored Procedures
- `GetStudentPerformanceSummary(student_id)` - Retrieves comprehensive student data
- `InsertCompleteStudentRecord(...)` - Atomic multi-table insertion

### Triggers
- `audit_academic_records_update` - Logs all academic record changes
- `validate_exam_score_insert` - Validates exam scores before insertion

## Project Structure

```
Formative1_Database_predictionPipeline_group10/
├── Untitled8.ipynb                        # Main analysis notebook
├── student_performance_db_schema.sql      # Complete MySQL schema
├── requirements.txt                       # Python dependencies
├── .env.example                          # Environment configuration template
├── app/
│   ├── models/
│   │   └── schemas.py                    # Pydantic models for API
│   ├── database/
│   │   └── connection.py                 # Database connections
│   └── api/                              # FastAPI endpoints (in progress)
└── models/                               # ML models storage
```

## Setup Instructions

### 1. Environment Setup

```powershell
# Clone the repository
git clone https://github.com/IrutingaboRaissa/Formative1_Database_predictionPipeline_group10.git
cd Formative1_Database_predictionPipeline_group10

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

Create a `.env` file (copy from `.env.example`):

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=student_performance_db

MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=student_performance_nosql
```

### 3. Initialize MySQL Database

```powershell
# Login to MySQL
mysql -u root -p

# Execute schema
source student_performance_db_schema.sql
```

### 4. Run the Notebook

```powershell
jupyter notebook Untitled8.ipynb
```

## Features Completed

- [x] Dataset loading and exploration (6607 records, 20 features)
- [x] 3NF database schema design
- [x] MySQL DDL with constraints, indexes, stored procedures, and triggers
- [x] Data normalization into 3 related tables
- [x] FastAPI project structure
- [x] Pydantic models for data validation
- [x] Database connection classes (MySQL + MongoDB)

## Next Steps

- [ ] Implement FastAPI CRUD endpoints
- [ ] Populate MySQL database with normalized data
- [ ] Create MongoDB collections
- [ ] Train ML model for prediction
- [ ] Build prediction script
- [ ] Create ERD diagram
- [ ] Write tests and documentation

## Dataset Information

**Source:** Kaggle - Student Performance Factors  
**Records:** 6,607 students  
**Features:** 20 attributes including:
- Academic: Hours Studied, Attendance, Previous Scores, Exam Score
- Environmental: Parental Involvement, School Type, Sleep Hours, etc.
- Demographic: Gender, Distance from Home, Learning Disabilities

## Technologies Used

- **Backend:** FastAPI, Python 3.13
- **Databases:** MySQL 8.0, MongoDB
- **ORM:** SQLAlchemy
- **Data Processing:** pandas, numpy
- **ML:** scikit-learn
- **Validation:** Pydantic
- **Environment:** python-dotenv

## Team

Group 10 - Formative 1 Assignment

## License

Educational project for database and ML coursework
