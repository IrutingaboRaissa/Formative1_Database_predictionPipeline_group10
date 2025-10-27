# Task Breakdown - Group 10

**Team Members:** Mitali, Raissa, Alliance, Innocente

## Current Status (Done by Raissa)
✅ Database schema designed (3NF normalized)  
✅ MySQL DDL script created with stored procedures & triggers  
✅ Dataset loaded and explored (Student Performance - 6,607 records)  
✅ Project structure created  
✅ Pydantic models defined  
✅ Database connection classes created  

---

## Remaining Tasks

### **TASK 1: Database Implementation** (20% Complete)

#### 1.1 MongoDB Implementation
**Assigned to:** `Innocente`  
**Estimated Time:** 3-4 hours  
**Deliverables:**
- [ ] Create MongoDB collections mirroring the SQL tables
- [ ] Write script to populate MongoDB with data from CSV
- [ ] Test MongoDB queries and aggregations
- [ ] Document MongoDB schema structure

**Files to create:**
- `database/mongodb_setup.py`
- `database/populate_mongodb.py`

---

#### 1.2 ERD Diagram Creation
**Assigned to:** `Mitali`  
**Estimated Time:** 1-2 hours  
**Deliverables:**
- [ ] Create professional ERD using draw.io, Lucidchart, or dbdiagram.io
- [ ] Show all tables, relationships, primary/foreign keys
- [ ] Export as high-quality PNG/PDF
- [ ] Add to `docs/` folder

**Tools Recommended:**
- [dbdiagram.io](https://dbdiagram.io) - Code-based ERD
- [draw.io](https://draw.io) - Visual ERD
- [Lucidchart](https://lucidchart.com) - Professional ERD

---

#### 1.3 MySQL Database Population
**Assigned to:** `Raissa`  
**Estimated Time:** 2-3 hours  
**Deliverables:**
- [ ] Create script to load CSV data into MySQL
- [ ] Normalize data into students, academic_records, environmental_factors tables
- [ ] Test stored procedures and triggers
- [ ] Verify data integrity

**Files to create:**
- `database/populate_mysql.py`

---

### **TASK 2: FastAPI CRUD Operations** (10% Complete)

**Assigned to:** `Alliance`  
**Estimated Time:** 6-8 hours  
**Deliverables:**
- [ ] Implement POST endpoint (Create student record)
- [ ] Implement GET endpoints (Read single/all students)
- [ ] Implement PUT endpoint (Update student record)
- [ ] Implement DELETE endpoint (Delete student record)
- [ ] Add error handling and validation
- [ ] Test all endpoints using FastAPI docs or Postman
- [ ] Connect to MySQL database (not MongoDB for CRUD)

**Files to create:**
- `app/api/routes.py`
- `app/api/crud.py`
- `app/main.py`

**CRUD Operations Required:**
```
POST   /students              - Create new student
GET    /students              - Get all students
GET    /students/{id}         - Get student by ID
PUT    /students/{id}         - Update student
DELETE /students/{id}         - Delete student
```

---

### **TASK 3: Prediction Script** (0% Complete)

**Assigned to:** `Mitali`  
**Estimated Time:** 4-5 hours  
**Deliverables:**
- [ ] Fetch latest entry from database via API
- [ ] Load pre-trained ML model (from Intro to ML course)
- [ ] Preprocess data for prediction
- [ ] Make prediction using model
- [ ] Log prediction result back to database
- [ ] Handle missing data and edge cases

**Files to create:**
- `prediction/fetch_and_predict.py`
- `prediction/model_loader.py`
- `models/` - Store ML model file (.pkl or .joblib)

**Steps:**
1. Use `requests` library to call GET endpoint
2. Preprocess features (scaling, encoding)
3. Load model using `joblib` or `pickle`
4. Make prediction
5. POST prediction result back via API

---

## Task Assignment

### **Final Team Assignments:**

| Team Member | Tasks | Total Hours | Files to Create |
|------------|-------|-------------|-----------------|
| **Mitali** | 1. ERD Diagram<br>2. Prediction Script | 5-7 hours | `docs/ERD.png`<br>`prediction/fetch_and_predict.py`<br>`prediction/model_loader.py` |
| **Raissa** | MySQL Database Population | 2-3 hours | `database/populate_mysql.py` |
| **Alliance** | FastAPI CRUD Operations | 6-8 hours | `app/main.py`<br>`app/api/routes.py`<br>`app/api/crud.py` |
| **Innocente** | MongoDB Implementation | 3-4 hours | `database/mongodb_setup.py`<br>`database/populate_mongodb.py` |

### **Why This Distribution?**

- **Mitali**: ERD (quick, visual) + Prediction (needs ML knowledge) = Balanced workload
- **Raissa**: MySQL population (she created the schema, so she knows it best)
- **Alliance**: CRUD API (biggest task, most critical component)
- **Innocente**: MongoDB (complete NoSQL implementation with setup & population)

### **Workflow Order:**

1. **Raissa** → Populate MySQL first (so data is ready for API testing)
2. **Mitali** → Create ERD early (helps everyone visualize structure)
3. **Alliance** → Build API endpoints (needs MySQL data from Raissa)
4. **Innocente** → Set up MongoDB (can work in parallel)
5. **Mitali** → Prediction script (needs Alliance's API to fetch data)

---

## Task Assignment Recommendation

### Option 1: By Task
- **Person 1:** MongoDB Implementation + ERD Diagram
- **Person 2:** MySQL Population + Testing
- **Person 3:** FastAPI CRUD Endpoints
- **Person 4:** Prediction Script + Final Integration

### Option 2: By Component
- **Person 1:** All Database work (MongoDB + MySQL population)
- **Person 2:** FastAPI endpoints (CRUD operations)
- **Person 3:** Prediction script + ML model
- **Person 4:** ERD + Documentation + Testing

---

## Commit Best Practices

**IMPORTANT:** Each person must have **minimum 4 commits** (excluding initial commit and README changes)

### Commit Message Format:
```
[Component] Brief description

Example:
[MongoDB] Add MongoDB connection and setup script
[API] Implement POST endpoint for students
[Prediction] Add data preprocessing and model loading
[ERD] Create database ERD diagram
```

### Good Commits:
✅ `[API] Implement GET endpoint for fetching all students`  
✅ `[Database] Add MongoDB population script with data validation`  
✅ `[Prediction] Integrate model prediction with API fetch`  

### Bad Commits:
❌ `Update files`  
❌ `Fixed stuff`  
❌ `Changes`  

---

## Testing Checklist

- [ ] MySQL stored procedure `GetStudentPerformanceSummary` works
- [ ] MySQL trigger `audit_academic_records_update` logs changes
- [ ] All 5 CRUD endpoints return correct responses
- [ ] Prediction script fetches latest entry successfully
- [ ] Prediction results are logged in database
- [ ] MongoDB collections contain all data

---

## Deliverables Summary

### Code Repository
- [ ] All Python scripts committed with clear messages
- [ ] Each member has 4+ meaningful commits
- [ ] `.env.example` provided (no passwords committed)
- [ ] Requirements.txt is up to date

### PDF Report
- [ ] GitHub repo link included
- [ ] Team member contributions table
- [ ] ERD diagram included
- [ ] Screenshots of API endpoints working
- [ ] Screenshots of database queries
- [ ] Prediction output examples

### Presentation
- [ ] Each member explains their role
- [ ] Camera ON and audible
- [ ] Demonstrate working code
- [ ] Show database operations

---

## Quick Start Commands

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Initialize MySQL
mysql -u root -p < student_performance_db_schema.sql

# 5. Run FastAPI server (once Task 2 is complete)
uvicorn app.main:app --reload

# 6. Run prediction script (once Task 3 is complete)
python prediction/fetch_and_predict.py
```

---

## Questions & Help

If stuck, check:
1. Project README.md
2. Existing code in `app/models/` and `app/database/`
3. FastAPI documentation: https://fastapi.tiangolo.com
4. MongoDB documentation: https://pymongo.readthedocs.io

**Remember:** Everyone must contribute code, not just documentation!
