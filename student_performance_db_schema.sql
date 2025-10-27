
-- STUDENT PERFORMANCE DATABASE SCHEMA

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
    model_version VARCHAR(50) DEFAULT 'v1.0',
    confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student_predictions (student_id),
    INDEX idx_prediction_date (prediction_date),
    INDEX idx_model_version (model_version)
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


-- STORED PROCEDURE: Get Student Performance Summary
DELIMITER //

CREATE PROCEDURE GetStudentPerformanceSummary(IN student_id_param INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    SELECT 
        s.student_id,
        s.gender,
        s.learning_disabilities,
        s.distance_from_home,
        ar.hours_studied,
        ar.attendance,
        ar.previous_scores,
        ar.exam_score,
        ef.parental_involvement,
        ef.school_type,
        ef.motivation_level,
        COUNT(p.prediction_id) as total_predictions,
        AVG(p.predicted_score) as avg_predicted_score,
        AVG(p.confidence_score) as avg_confidence
    FROM students s
    LEFT JOIN academic_records ar ON s.student_id = ar.student_id
    LEFT JOIN environmental_factors ef ON s.student_id = ef.student_id  
    LEFT JOIN predictions p ON s.student_id = p.student_id
    WHERE s.student_id = student_id_param
    GROUP BY s.student_id, s.gender, s.learning_disabilities, s.distance_from_home,
             ar.hours_studied, ar.attendance, ar.previous_scores, ar.exam_score,
             ef.parental_involvement, ef.school_type, ef.motivation_level;
END //

-- STORED PROCEDURE: Insert Complete Student Record
CREATE PROCEDURE InsertCompleteStudentRecord(
    IN p_gender ENUM('Male', 'Female'),
    IN p_learning_disabilities ENUM('Yes', 'No'),
    IN p_distance_from_home ENUM('Near', 'Moderate', 'Far'),
    IN p_hours_studied INT,
    IN p_attendance INT,
    IN p_previous_scores INT,
    IN p_exam_score INT,
    IN p_parental_involvement ENUM('Low', 'Medium', 'High'),
    IN p_access_to_resources ENUM('Low', 'Medium', 'High'),
    IN p_sleep_hours INT,
    IN p_school_type ENUM('Public', 'Private'),
    OUT p_student_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Insert student
    INSERT INTO students (gender, learning_disabilities, distance_from_home)
    VALUES (p_gender, p_learning_disabilities, p_distance_from_home);

    SET p_student_id = LAST_INSERT_ID();

    -- Insert academic record
    INSERT INTO academic_records (student_id, hours_studied, attendance, previous_scores, exam_score)
    VALUES (p_student_id, p_hours_studied, p_attendance, p_previous_scores, p_exam_score);

    -- Insert environmental factors
    INSERT INTO environmental_factors (student_id, parental_involvement, access_to_resources, sleep_hours, school_type)
    VALUES (p_student_id, p_parental_involvement, p_access_to_resources, p_sleep_hours, p_school_type);

    COMMIT;
END //

DELIMITER ;

-- TRIGGER: Audit Academic Records Changes
DELIMITER //

CREATE TRIGGER audit_academic_records_update
    AFTER UPDATE ON academic_records
    FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name, 
        operation, 
        record_id, 
        old_values, 
        new_values,
        changed_by
    ) VALUES (
        'academic_records',
        'UPDATE',
        NEW.record_id,
        JSON_OBJECT(
            'hours_studied', OLD.hours_studied,
            'attendance', OLD.attendance, 
            'previous_scores', OLD.previous_scores,
            'exam_score', OLD.exam_score
        ),
        JSON_OBJECT(
            'hours_studied', NEW.hours_studied,
            'attendance', NEW.attendance,
            'previous_scores', NEW.previous_scores, 
            'exam_score', NEW.exam_score
        ),
        USER()
    );
END //

-- TRIGGER: Validate Exam Score Range
CREATE TRIGGER validate_exam_score_insert
    BEFORE INSERT ON academic_records
    FOR EACH ROW
BEGIN
    IF NEW.exam_score < 0 OR NEW.exam_score > 110 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Exam score must be between 0 and 110';
    END IF;

    IF NEW.attendance < 60 AND NEW.exam_score > 90 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Attendance below 60% with score above 90 seems suspicious';
    END IF;
END //

DELIMITER ;
