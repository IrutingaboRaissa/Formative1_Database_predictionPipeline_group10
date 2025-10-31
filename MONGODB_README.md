# MongoDB Setup Guide

## Quick Start

1. Make sure MongoDB is installed and running on your machine
2. Update your `.env` file with MongoDB credentials
3. Run the setup script:
   ```bash
   python mongodb_setup.py
   ```

## What This Does

The script will:
- Connect to MongoDB
- Create 4 collections: students, academic_records, environmental_factors, predictions
- Insert all 6607 student records from the Kaggle dataset
- Create indexes for faster queries
- Verify all data was inserted correctly

## Collections Structure

### students
- student_id (unique)
- gender
- learning_disabilities
- distance_from_home

### academic_records
- student_id
- hours_studied
- attendance
- previous_scores
- tutoring_sessions
- exam_score

### environmental_factors
- student_id
- parental_involvement
- access_to_resources
- extracurricular_activities
- sleep_hours
- motivation_level
- internet_access
- family_income
- teacher_quality
- school_type
- peer_influence
- physical_activity
- parental_education_level

### predictions
- student_id
- predicted_score
- actual_score
- confidence_score
- prediction_date

## Verification

After running the script, you should see:
- 6607 students
- 6607 academic records
- 6607 environmental factors
- A sample query showing top students by exam score
