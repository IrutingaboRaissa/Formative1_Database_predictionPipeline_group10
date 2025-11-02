-- ============================================================================
-- STORED PROCEDURES AND TRIGGERS
-- Student Performance Database
-- ============================================================================
-- This file contains stored procedures and triggers required for the
-- Student Performance Prediction System
-- 
-- Execute this file AFTER running schema_ddl_only.sql
-- ============================================================================

USE student_performance_db;

-- ============================================================================
-- STORED PROCEDURE 1: GetStudentPerformanceSummary
-- ============================================================================
-- Purpose: Retrieves a comprehensive summary of student performance data
-- Parameters: student_id (INT)
-- Returns: Complete student information including academic, environmental,
--          and prediction data
-- ============================================================================

DROP PROCEDURE IF EXISTS GetStudentPerformanceSummary;

DELIMITER //

CREATE PROCEDURE GetStudentPerformanceSummary(IN p_student_id INT)
BEGIN
    SELECT 
        s.student_id,
        s.gender,
        s.learning_disabilities,
        s.distance_from_home,
        a.hours_studied,
        a.attendance,
        a.previous_scores,
        a.exam_score,
        a.tutoring_sessions,
        e.school_type,
        e.parental_involvement,
        COUNT(p.prediction_id) AS total_predictions,
        AVG(p.predicted_score) AS avg_predicted_score,
        e.motivation_level,
        e.access_to_resources,
        e.family_income,
        e.internet_access,
        e.parental_education_level,
        s.created_at AS student_created_at
    FROM students s
    LEFT JOIN academic_records a ON s.student_id = a.student_id
    LEFT JOIN environmental_factors e ON s.student_id = e.student_id
    LEFT JOIN predictions p ON s.student_id = p.student_id
    WHERE s.student_id = p_student_id
    GROUP BY s.student_id, s.gender, s.learning_disabilities, s.distance_from_home,
             a.hours_studied, a.attendance, a.previous_scores, a.exam_score, 
             a.tutoring_sessions, e.school_type, e.parental_involvement,
             e.motivation_level, e.access_to_resources, e.family_income,
             e.internet_access, e.parental_education_level, s.created_at;
END //

DELIMITER ;


-- ============================================================================
-- STORED PROCEDURE 2: InsertCompleteStudentRecord
-- ============================================================================
-- Purpose: Inserts a complete student record with academic and environmental
--          data in a single transaction
-- Parameters: All student, academic, and environmental attributes
-- Returns: student_id of the newly created student
-- Benefits: Ensures data integrity, reduces API calls, atomic operation
-- ============================================================================

DROP PROCEDURE IF EXISTS InsertCompleteStudentRecord;

DELIMITER //

CREATE PROCEDURE InsertCompleteStudentRecord(
    -- Student table parameters
    IN p_gender ENUM('Male', 'Female'),
    IN p_learning_disabilities ENUM('Yes', 'No'),
    IN p_distance_from_home ENUM('Near', 'Moderate', 'Far'),
    
    -- Academic records parameters
    IN p_hours_studied INT,
    IN p_attendance INT,
    IN p_previous_scores INT,
    IN p_tutoring_sessions INT,
    IN p_exam_score INT,
    
    -- Environmental factors parameters
    IN p_parental_involvement ENUM('Low', 'Medium', 'High'),
    IN p_access_to_resources ENUM('Low', 'Medium', 'High'),
    IN p_extracurricular_activities ENUM('Yes', 'No'),
    IN p_sleep_hours INT,
    IN p_motivation_level ENUM('Low', 'Medium', 'High'),
    IN p_internet_access ENUM('Yes', 'No'),
    IN p_family_income ENUM('Low', 'Medium', 'High'),
    IN p_teacher_quality ENUM('Low', 'Medium', 'High'),
    IN p_school_type ENUM('Public', 'Private'),
    IN p_peer_influence ENUM('Positive', 'Neutral', 'Negative'),
    IN p_physical_activity INT,
    IN p_parental_education_level ENUM('High School', 'College', 'Postgraduate'),
    
    -- Output parameter
    OUT p_new_student_id INT
)
BEGIN
    -- Declare variables for error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction on error
        ROLLBACK;
        SET p_new_student_id = -1;
    END;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Insert into students table
    INSERT INTO students (gender, learning_disabilities, distance_from_home)
    VALUES (p_gender, p_learning_disabilities, p_distance_from_home);
    
    -- Get the newly created student_id
    SET p_new_student_id = LAST_INSERT_ID();
    
    -- Insert into academic_records table
    INSERT INTO academic_records (
        student_id, hours_studied, attendance, previous_scores, 
        tutoring_sessions, exam_score
    )
    VALUES (
        p_new_student_id, p_hours_studied, p_attendance, p_previous_scores,
        p_tutoring_sessions, p_exam_score
    );
    
    -- Insert into environmental_factors table
    INSERT INTO environmental_factors (
        student_id, parental_involvement, access_to_resources,
        extracurricular_activities, sleep_hours, motivation_level,
        internet_access, family_income, teacher_quality, school_type,
        peer_influence, physical_activity, parental_education_level
    )
    VALUES (
        p_new_student_id, p_parental_involvement, p_access_to_resources,
        p_extracurricular_activities, p_sleep_hours, p_motivation_level,
        p_internet_access, p_family_income, p_teacher_quality, p_school_type,
        p_peer_influence, p_physical_activity, p_parental_education_level
    );
    
    -- Commit the transaction
    COMMIT;
    
    -- Return success message
    SELECT p_new_student_id AS new_student_id, 'Student record created successfully' AS message;
END //

DELIMITER ;


-- ============================================================================
-- TRIGGER 1: audit_academic_records_update
-- ============================================================================
-- Purpose: Automatically logs all UPDATE operations on academic_records table
--          to the audit_log table for tracking changes
-- Fires: AFTER UPDATE on academic_records
-- Logs: old values, new values, timestamp, and operation type
-- Use Case: Data validation, compliance, tracking student performance changes
-- ============================================================================

DROP TRIGGER IF EXISTS audit_academic_records_update;

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
        changed_by,
        change_timestamp
    )
    VALUES (
        'academic_records',
        'UPDATE',
        NEW.record_id,
        JSON_OBJECT(
            'hours_studied', OLD.hours_studied,
            'attendance', OLD.attendance,
            'previous_scores', OLD.previous_scores,
            'tutoring_sessions', OLD.tutoring_sessions,
            'exam_score', OLD.exam_score
        ),
        JSON_OBJECT(
            'hours_studied', NEW.hours_studied,
            'attendance', NEW.attendance,
            'previous_scores', NEW.previous_scores,
            'tutoring_sessions', NEW.tutoring_sessions,
            'exam_score', NEW.exam_score
        ),
        COALESCE(USER(), 'system'),
        CURRENT_TIMESTAMP
    );
END //

DELIMITER ;


-- ============================================================================
-- TRIGGER 2: audit_predictions_insert (BONUS)
-- ============================================================================
-- Purpose: Logs all new predictions to the audit_log table
-- Fires: AFTER INSERT on predictions table
-- Use Case: Track ML model predictions for analysis and compliance
-- ============================================================================

DROP TRIGGER IF EXISTS audit_predictions_insert;

DELIMITER //

CREATE TRIGGER audit_predictions_insert
AFTER INSERT ON predictions
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name,
        operation,
        record_id,
        old_values,
        new_values,
        changed_by,
        change_timestamp
    )
    VALUES (
        'predictions',
        'INSERT',
        NEW.prediction_id,
        NULL,
        JSON_OBJECT(
            'student_id', NEW.student_id,
            'predicted_score', NEW.predicted_score,
            'actual_score', NEW.actual_score,
            'confidence_score', NEW.confidence_score,
            'prediction_date', NEW.prediction_date
        ),
        COALESCE(USER(), 'ML_MODEL'),
        CURRENT_TIMESTAMP
    );
END //

DELIMITER ;


-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Run these queries to verify that procedures and triggers were created

-- Check stored procedures
SELECT 
    ROUTINE_NAME,
    ROUTINE_TYPE,
    CREATED,
    LAST_ALTERED
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = 'student_performance_db'
AND ROUTINE_TYPE = 'PROCEDURE';

-- Check triggers
SELECT 
    TRIGGER_NAME,
    EVENT_MANIPULATION,
    EVENT_OBJECT_TABLE,
    ACTION_TIMING,
    CREATED
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = 'student_performance_db';


-- ============================================================================
-- EXAMPLE USAGE
-- ============================================================================

-- Example 1: Call GetStudentPerformanceSummary
-- CALL GetStudentPerformanceSummary(1);

-- Example 2: Insert a complete student record
-- CALL InsertCompleteStudentRecord(
--     'Male', 'No', 'Near',                           -- Student info
--     25, 85, 75, 5, 80,                              -- Academic info
--     'High', 'High', 'Yes', 7, 'High',               -- Environmental info (part 1)
--     'Yes', 'Medium', 'High', 'Public',              -- Environmental info (part 2)
--     'Positive', 5, 'College',                       -- Environmental info (part 3)
--     @new_id                                         -- Output parameter
-- );
-- SELECT @new_id AS 'Newly Created Student ID';

-- Example 3: Test the trigger by updating an academic record
-- UPDATE academic_records SET exam_score = 95 WHERE student_id = 1;
-- SELECT * FROM audit_log WHERE table_name = 'academic_records' ORDER BY change_timestamp DESC LIMIT 1;

-- ============================================================================
-- END OF FILE
-- ============================================================================
