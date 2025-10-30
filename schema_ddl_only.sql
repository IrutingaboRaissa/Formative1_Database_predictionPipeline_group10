-- STUDENT PERFORMANCE DATABASE SCHEMA (DDL ONLY)

DROP DATABASE IF EXISTS student_performance_db;
CREATE DATABASE student_performance_db;
USE student_performance_db;

-- TABLE 1: STUDENTS (Main Entity)
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    gender ENUM('Male', 'Female') NOT NULL,
    learning_disabilities ENUM('Yes', 'No') NOT NULL DEFAULT 'No',
    distance_from_home ENUM('Near', 'Moderate', 'Far') DEFAULT 'Moderate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_gender (gender),
    INDEX idx_learning_disabilities (learning_disabilities)
);

-- TABLE 2: ACADEMIC_RECORDS
CREATE TABLE academic_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    hours_studied INT CHECK (hours_studied >= 0 AND hours_studied <= 50),
    attendance INT CHECK (attendance >= 0 AND attendance <= 100),
    previous_scores INT CHECK (previous_scores >= 0 AND previous_scores <= 100),
    tutoring_sessions INT DEFAULT 0 CHECK (tutoring_sessions >= 0),
    exam_score INT CHECK (exam_score >= 0 AND exam_score <= 110),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student_academic (student_id),
    INDEX idx_exam_score (exam_score),
    INDEX idx_created_at (created_at)
);

-- TABLE 3: ENVIRONMENTAL_FACTORS  
CREATE TABLE environmental_factors (
    env_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    parental_involvement ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    access_to_resources ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    extracurricular_activities ENUM('Yes', 'No') DEFAULT 'No',
    sleep_hours INT CHECK (sleep_hours >= 4 AND sleep_hours <= 12),
    motivation_level ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    internet_access ENUM('Yes', 'No') DEFAULT 'Yes',
    family_income ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    teacher_quality ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    school_type ENUM('Public', 'Private') DEFAULT 'Public',
    peer_influence ENUM('Positive', 'Neutral', 'Negative') DEFAULT 'Neutral',
    physical_activity INT CHECK (physical_activity >= 0 AND physical_activity <= 10),
    parental_education_level ENUM('High School', 'College', 'Postgraduate') DEFAULT 'High School',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student_env (student_id),
    INDEX idx_parental_involvement (parental_involvement),
    INDEX idx_school_type (school_type)
);

-- TABLE 4: PREDICTIONS (ML Results)
CREATE TABLE predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    predicted_score DECIMAL(5,2) CHECK (predicted_score >= 0 AND predicted_score <= 110),
    actual_score INT NULL CHECK (actual_score >= 0 AND actual_score <= 110),
    confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student_predictions (student_id),
    INDEX idx_prediction_date (prediction_date)
);

-- TABLE 5: AUDIT_LOG (For Trigger)
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(50) NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    record_id INT NOT NULL,
    old_values JSON NULL,
    new_values JSON NULL,
    changed_by VARCHAR(100) DEFAULT 'system',
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_table_operation (table_name, operation),
    INDEX idx_change_timestamp (change_timestamp)
);
