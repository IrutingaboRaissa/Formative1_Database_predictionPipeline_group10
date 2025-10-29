# MySQL Database Implementation - OOP Architecture

## 🎯 Quick Start

**Run the entire MySQL setup with one command:**

```bash
python main.py
```

That's it! This single command will:
1. ✅ Download the dataset from Kaggle
2. ✅ Create the MySQL database
3. ✅ Execute the schema (tables, procedures, triggers)
4. ✅ Transform data to normalized structure
5. ✅ Populate all tables in batches
6. ✅ Verify data integrity

---

## 📁 Project Structure (OOP Design)

```
Formative1_Database_predictionPipeline_group10/
│
├── main.py                          # 🚀 ENTRY POINT - Run this!
├── .env                             # Database credentials
├── student_performance_db_schema.sql # SQL schema file
│
├── src/                             # Source code (OOP architecture)
│   ├── __init__.py
│   │
│   ├── database/                    # Database management classes
│   │   ├── __init__.py
│   │   ├── mysql_manager.py         # MySQLDatabaseManager class
│   │   ├── data_populator.py        # MySQLDataPopulator class
│   │   └── data_verifier.py         # MySQLDataVerifier class
│   │
│   └── utils/                       # Utility classes
│       ├── __init__.py
│       └── data_transformer.py      # DataTransformer class
│
└── scripts/                         # Legacy standalone scripts
    ├── create_database.py
    ├── execute_schema.py
    ├── populate_mysql.py
    ├── verify_mysql.py
    └── test_stored_procedures.py
```

---

## 🏗️ Class Architecture

### 1. **MySQLDatabaseManager**
**File:** `src/database/mysql_manager.py`

**Purpose:** Manages database creation, schema execution, and connections

**Key Methods:**
- `__init__(config_path)` - Load database configuration from .env
- `create_database()` - Create database if not exists
- `execute_schema(schema_file)` - Execute SQL schema file
- `get_connection(include_db)` - Get database connection
- `test_connection()` - Test database connectivity
- `drop_database()` - Drop database (use with caution!)

**Example Usage:**
```python
from database.mysql_manager import MySQLDatabaseManager

db_manager = MySQLDatabaseManager()
db_manager.create_database()
db_manager.execute_schema('student_performance_db_schema.sql')
db_manager.test_connection()
```

---

### 2. **MySQLDataPopulator**
**File:** `src/database/data_populator.py`

**Purpose:** Handles batch insertion of normalized data into MySQL

**Key Methods:**
- `__init__(db_manager)` - Initialize with database manager
- `connect()` - Establish database connection
- `insert_students_batch(df, batch_size)` - Insert students in batches
- `insert_academic_records_batch(df, batch_size)` - Insert academic records
- `insert_environmental_factors_batch(df, batch_size)` - Insert environmental data
- `populate_all(students_df, academic_df, env_df, batch_size)` - Populate all tables
- `disconnect()` - Close connection

**Example Usage:**
```python
from database.data_populator import MySQLDataPopulator

populator = MySQLDataPopulator(db_manager)
results = populator.populate_all(
    students_df, 
    academic_df, 
    environmental_df, 
    batch_size=100
)
print(f"Inserted {results['total']} records")
```

---

### 3. **MySQLDataVerifier**
**File:** `src/database/data_verifier.py`

**Purpose:** Validates database integrity and data quality

**Key Methods:**
- `__init__(db_manager)` - Initialize with database manager
- `get_table_counts()` - Get record counts for all tables
- `verify_referential_integrity()` - Check foreign key relationships
- `get_sample_data(limit)` - Retrieve sample joined data
- `verify_all(expected_count)` - Run complete verification

**Example Usage:**
```python
from database.data_verifier import MySQLDataVerifier

verifier = MySQLDataVerifier(db_manager)
results = verifier.verify_all(expected_count=6607)
print(f"Status: {results['status']}")
```

---

### 4. **DataTransformer**
**File:** `src/utils/data_transformer.py`

**Purpose:** Transforms flat dataset into 3NF normalized structure

**Key Methods:**
- `__init__(df)` - Initialize with raw DataFrame
- `transform_to_normalized()` - Convert to normalized DataFrames
- `get_summary()` - Display transformation summary

**Example Usage:**
```python
from utils.data_transformer import DataTransformer

transformer = DataTransformer(df)
students_df, academic_df, env_df = transformer.transform_to_normalized()
transformer.get_summary()
```

---

## 🔧 Configuration

**`.env` file:**
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=student_performance_db
```

---

## 🎯 Usage Examples

### Option 1: Run Everything (Recommended)
```bash
python main.py
```

### Option 2: Use Classes Individually
```python
import pandas as pd
from database.mysql_manager import MySQLDatabaseManager
from database.data_populator import MySQLDataPopulator
from utils.data_transformer import DataTransformer

# 1. Setup database
db_manager = MySQLDatabaseManager()
db_manager.create_database()
db_manager.execute_schema()

# 2. Transform data
transformer = DataTransformer(your_dataframe)
students_df, academic_df, env_df = transformer.transform_to_normalized()

# 3. Populate database
populator = MySQLDataPopulator(db_manager)
populator.populate_all(students_df, academic_df, env_df)
```

### Option 3: Use Legacy Scripts
```bash
cd scripts
python create_database.py
python execute_schema.py
python populate_mysql.py
python verify_mysql.py
```

---

## ✅ Advantages of OOP Architecture

1. **Single Entry Point** - Run entire setup with `python main.py`
2. **Reusable Classes** - Import and use in other scripts
3. **Clean Separation** - Database, population, verification are separate
4. **Easy Testing** - Each class can be tested independently
5. **Maintainable** - Changes in one class don't affect others
6. **Professional** - Industry-standard design pattern
7. **Scalable** - Easy to add new features/classes

---

## 📊 What Gets Created

### Database Tables:
1. **students** (6,607 records)
2. **academic_records** (6,607 records)
3. **environmental_factors** (6,607 records)
4. **predictions** (empty - for ML results)
5. **audit_log** (for trigger logging)

### Stored Procedures:
1. `GetStudentPerformanceSummary(student_id)`
2. `InsertCompleteStudentRecord(...)`

### Triggers:
1. `audit_academic_records_update` - Logs all updates
2. `validate_exam_score_insert` - Validates before insert

---

## 🚀 Benefits for Your Assignment

✅ **Demonstrates OOP knowledge**  
✅ **Shows software engineering best practices**  
✅ **Clean, maintainable code**  
✅ **Easy to demo to instructor**  
✅ **Professional project structure**  
✅ **Single command execution**  
✅ **Better than scattered scripts**  

---

## 👤 Author

**Raissa Irutingabo**  
MySQL Database Implementation  
Formative 1 - Database & Prediction Pipeline
