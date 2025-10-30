# MySQL Database Setup Scripts

Created by: Raissa  
Role: MySQL Database Implementation

This folder contains automated scripts for setting up and populating the MySQL database for the Student Performance Prediction system.

## Scripts Overview

### 1. `create_database.py`
**Purpose:** Initialize the MySQL database

**Features:**
- Creates `student_performance_db` database if it doesn't exist
- Idempotent operation (safe to run multiple times)
- Uses environment variables for credentials
- Proper error handling

**Usage:**
```python
python scripts/create_database.py
```

---

### 2. `execute_schema.py`
**Purpose:** Execute SQL schema to create all database objects

**Creates:**
- 5 Tables:
  - `students` - Student demographic information
  - `academic_records` - Academic performance data
  - `environmental_factors` - Environmental and social factors
  - `predictions` - ML prediction results
  - `audit_log` - Change tracking for audit trail

- 2 Stored Procedures:
  - `GetStudentPerformanceSummary(student_id)` - Comprehensive student data retrieval
  - `InsertCompleteStudentRecord(...)` - Atomic multi-table insertion

- 2 Triggers:
  - `audit_academic_records_update` - Logs all changes to academic records
  - `validate_exam_score_insert` - Validates exam scores before insertion

**Usage:**
```python
python scripts/execute_schema.py
```

---

### 3. `populate_mysql.py`
**Purpose:** Insert normalized student performance data into MySQL

**Features:**
- `MySQLDataPopulator` class for structured data insertion
- Inserts data into 3 tables from pandas DataFrames:
  - Students: 6,607 records
  - Academic Records: 6,607 records  
  - Environmental Factors: 6,607 records
- Progress tracking (updates every 1000 records)
- Error handling and detailed logging
- Summary statistics after completion

**Usage:**
```python
from scripts.populate_mysql import MySQLDataPopulator

# Assuming you have normalized DataFrames
populator = MySQLDataPopulator()
results = populator.populate_all(students_df, academic_df, environmental_df)
```

---

### 4. `verify_mysql.py`
**Purpose:** Verify database integrity and data quality

**Checks:**
- ✓ Table record counts
- ✓ Referential integrity (all foreign keys valid)
- ✓ Data quality (NULL values, valid ranges)
- ✓ Sample data retrieval

**Usage:**
```python
python scripts/verify_mysql.py
```

**Expected Output:**
```
DATABASE VERIFICATION
============================================================
TABLE RECORD COUNTS
✓ students                    :  6,607 records
✓ academic_records            :  6,607 records
✓ environmental_factors       :  6,607 records
✓ predictions                 :      0 records (empty - will be populated by ML script)
✓ audit_log                   :      0 records

REFERENTIAL INTEGRITY CHECK
✓ academic_records.student_id - All references valid
✓ environmental_factors.student_id - All references valid
✓ predictions.student_id - All references valid

DATA QUALITY CHECKS
✓ No NULL values in students.gender
✓ All exam scores within valid range (0-110)
✓ All attendance values within valid range (0-100)

✓ Database verification completed successfully!
```

---

## Complete Setup Workflow

### Step 1: Configure Environment
Create a `.env` file in the project root:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=student_performance_db
```

### Step 2: Run Setup Scripts
```bash
# 1. Create database
python scripts/create_database.py

# 2. Execute schema (creates tables, procedures, triggers)
python scripts/execute_schema.py

# 3. Populate with data (run from Jupyter notebook)
# See Untitled8.ipynb for data population

# 4. Verify everything worked
python scripts/verify_mysql.py
```

---

## Database Schema (3NF Normalized)

### Entity Relationships
```
students (1) ──→ (Many) academic_records
students (1) ──→ (Many) environmental_factors
students (1) ──→ (Many) predictions
```

### Normalization Rules Applied
- **1NF:** All columns contain atomic values, each row is unique
- **2NF:** No partial dependencies (all non-key attributes depend on entire primary key)
- **3NF:** No transitive dependencies (non-key attributes don't depend on other non-key attributes)

---

## Data Statistics

- **Total Students:** 6,607
- **Total Records:** 19,821 (across 3 main tables)
- **Features per Student:** 20 attributes
- **Dataset Source:** Kaggle - Student Performance Factors

---

## Testing Stored Procedures

### Test GetStudentPerformanceSummary
```sql
CALL GetStudentPerformanceSummary(1);
```

### Test InsertCompleteStudentRecord
```sql
CALL InsertCompleteStudentRecord(
    'Male',              -- gender
    'No',                -- learning_disabilities
    'Near',              -- distance_from_home
    20,                  -- hours_studied
    85,                  -- attendance
    75,                  -- previous_scores
    70,                  -- exam_score
    'Medium',            -- parental_involvement
    'High',              -- access_to_resources
    7,                   -- sleep_hours
    'Public',            -- school_type
    @new_student_id      -- OUT parameter
);

SELECT @new_student_id;  -- View the newly created student ID
```

---

## Troubleshooting

### Connection Issues
- Verify MySQL is running: `mysql -u root -p`
- Check `.env` file has correct credentials
- Ensure database user has CREATE, INSERT, SELECT privileges

### Import Errors
```bash
pip install mysql-connector-python python-dotenv pandas tabulate
```

### Schema Already Exists
- The scripts are idempotent - safe to rerun
- To start fresh: Drop database manually first

```sql
DROP DATABASE IF EXISTS student_performance_db;
```

---

## Integration with Team

This MySQL implementation integrates with:

1. **MongoDB (Team Member):** NoSQL mirror of relational data
2. **FastAPI (Team Member):** CRUD endpoints will query this database
3. **ML Prediction (Team Member):** Results will be saved to `predictions` table

---

## Contribution Notes

**Branch:** `feature/raissa-mysql-population`

**Commits:**
1. Database creation script
2. Schema execution script
3. Data population module
4. Verification script
5. Documentation

**Files:**
- `scripts/create_database.py` - 62 lines
- `scripts/execute_schema.py` - 114 lines
- `scripts/populate_mysql.py` - 267 lines
- `scripts/verify_mysql.py` - 292 lines
- `scripts/README.md` - This file

**Total Lines of Code:** ~735 lines (excluding comments and documentation)

---

## Next Steps

- [ ] Create ERD diagram
- [ ] Test stored procedures with sample data
- [ ] Verify triggers work correctly
- [ ] Document API endpoints for team integration
- [ ] Performance testing with 6607 records

---

**Last Updated:** October 28, 2025  
**Status:** MySQL database implementation complete ✓
