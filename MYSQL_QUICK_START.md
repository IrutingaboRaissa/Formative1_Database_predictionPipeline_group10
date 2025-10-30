# MySQL Setup & Execution Guide
## Raissa's MySQL Implementation - Quick Start

### Step 1: Install Required Packages
Run this in your notebook:
```python
!pip install mysql-connector-python python-dotenv
```

### Step 2: Create .env File
Create a file named `.env` in the project root with your MySQL credentials:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_ACTUAL_PASSWORD
MYSQL_DATABASE=student_performance_db
```

### Step 3: Run Notebook Cells in Order

**Cell 1:** Import all libraries
**Cell 2:** Install kagglehub
**Cell 3:** Download dataset
**Cell 4:** Load CSV data
**Cell 5:** Explore dataset
**Cell 7:** Design 3NF schema
**Cell 8:** Generate MySQL DDL
**Cell 9:** Create stored procedures & triggers
**Cell 10:** Normalize data into DataFrames
**Cell 11:** Create database & execute schema
**Cell 12:** Insert data in batches (100 records at a time)
**Cell 13:** Verify database population

### Step 4: Verify Your Work

After running all cells, check your MySQL database:

```sql
USE student_performance_db;

-- Check table counts
SELECT COUNT(*) FROM students;           -- Should be 6607
SELECT COUNT(*) FROM academic_records;   -- Should be 6607
SELECT COUNT(*) FROM environmental_factors; -- Should be 6607

-- Test stored procedure
CALL GetStudentPerformanceSummary(1);

-- Test trigger (update a record and check audit_log)
UPDATE academic_records SET exam_score = 75 WHERE record_id = 1;
SELECT * FROM audit_log;
```

### What You've Accomplished (MySQL ONLY)

✅ **Database Design:**
- 4 tables in 3NF normalization
- Primary and foreign keys
- Check constraints for data validation
- Indexes for performance

✅ **Stored Procedures (2):**
- GetStudentPerformanceSummary(student_id)
- InsertCompleteStudentRecord(...)

✅ **Triggers (2):**
- audit_academic_records_update
- validate_exam_score_insert

✅ **Data Population:**
- 6,607 students
- 6,607 academic records
- 6,607 environmental factors
- **Total: 19,821 records**

✅ **Automation Scripts:**
- create_database.py
- execute_schema.py
- populate_mysql.py
- verify_mysql.py
- test_stored_procedures.py

✅ **Documentation:**
- scripts/README.md
- MYSQL_CONTRIBUTION_SUMMARY.md

### Your Commits (9 total)

1. feat: Implement MySQL database creation script
2. feat: Add SQL schema execution script with validation
3. feat: Implement MySQL data population module
4. feat: Add comprehensive MySQL database verification script
5. docs: Add comprehensive documentation for MySQL setup scripts
6. chore: Add tabulate package to requirements
7. test: Add comprehensive stored procedures and triggers testing
8. docs: Add comprehensive MySQL contribution summary
9. feat: Add batch processing for MySQL data insertion

### NOT Your Responsibility

❌ MongoDB implementation (teammate's job)
❌ FastAPI CRUD endpoints (teammate's job)  
❌ ML model training (teammate's job)
❌ Prediction script (teammate's job)

### Next Step: Create ERD Diagram

1. Go to https://dbdiagram.io
2. Paste this code:

```dbml
Table students {
  student_id int [pk, increment]
  gender varchar [not null]
  learning_disabilities varchar [not null, default: 'No']
  distance_from_home varchar [default: 'Moderate']
  created_at timestamp
  updated_at timestamp
}

Table academic_records {
  record_id int [pk, increment]
  student_id int [not null, ref: > students.student_id]
  hours_studied int
  attendance int
  previous_scores int
  tutoring_sessions int
  exam_score int
  created_at timestamp
}

Table environmental_factors {
  env_id int [pk, increment]
  student_id int [not null, ref: > students.student_id]
  parental_involvement varchar
  access_to_resources varchar
  extracurricular_activities varchar
  sleep_hours int
  motivation_level varchar
  internet_access varchar
  family_income varchar
  teacher_quality varchar
  school_type varchar
  peer_influence varchar
  physical_activity int
  parental_education_level varchar
  created_at timestamp
}

Table predictions {
  prediction_id int [pk, increment]
  student_id int [not null, ref: > students.student_id]
  predicted_score decimal
  actual_score int
  model_version varchar
  confidence_score decimal
  prediction_date timestamp
}

Table audit_log {
  log_id int [pk, increment]
  table_name varchar [not null]
  operation varchar [not null]
  record_id int [not null]
  old_values json
  new_values json
  changed_by varchar
  change_timestamp timestamp
}
```

3. Export as PNG and add to your report

### Troubleshooting

**Error: "No module named 'mysql'"**
Solution: Run `!pip install mysql-connector-python` in a notebook cell

**Error: "Access denied for user 'root'"**
Solution: Check your `.env` file has the correct password

**Error: "Database already exists"**
Solution: That's fine! The scripts handle this. Or drop it first: `DROP DATABASE student_performance_db;`

**Error: "Table already exists"**
Solution: The schema file includes `DROP TABLE IF EXISTS`. Re-run the schema execution cell.

---

**Your GitHub Branch:** `feature/raissa-mysql-population`

**Total Contribution:**
- 9 meaningful commits
- 1,656+ lines of code
- Complete MySQL database implementation
- All assignment requirements met ✓
