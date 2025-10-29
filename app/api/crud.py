from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional

from ..models.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    AcademicRecordCreate, AcademicRecordUpdate, AcademicRecordResponse,
    EnvironmentalFactorsCreate, EnvironmentalFactorsUpdate, EnvironmentalFactorsResponse,
    CompleteStudentCreate, CompleteStudentResponse
)
from ..models.database_models import Student, AcademicRecord, EnvironmentalFactors

# Student CRUD operations
def create_student(db: Session, student: StudentCreate) -> Student:
    try:
        db_student = Student(
            gender=student.gender,
            learning_disabilities=student.learning_disabilities,
            distance_from_home=student.distance_from_home
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_student(db: Session, student_id: int) -> Student:
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    return db.query(Student).offset(skip).limit(limit).all()

def update_student(db: Session, student_id: int, student: StudentUpdate) -> Student:
    db_student = get_student(db, student_id)
    update_data = student.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_student(db: Session, student_id: int) -> bool:
    student = get_student(db, student_id)
    try:
        db.delete(student)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Academic Record CRUD operations
def create_academic_record(db: Session, record: AcademicRecordCreate) -> AcademicRecord:
    try:
        # Verify student exists
        get_student(db, record.student_id)
        
        db_record = AcademicRecord(**record.dict())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_academic_record(db: Session, student_id: int) -> AcademicRecord:
    record = db.query(AcademicRecord).filter(AcademicRecord.student_id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Academic record not found")
    return record

def update_academic_record(db: Session, student_id: int, record: AcademicRecordUpdate) -> AcademicRecord:
    db_record = get_academic_record(db, student_id)
    update_data = record.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    try:
        db.commit()
        db.refresh(db_record)
        return db_record
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Environmental Factors CRUD operations
def create_environmental_factors(db: Session, factors: EnvironmentalFactorsCreate) -> EnvironmentalFactors:
    try:
        # Verify student exists
        get_student(db, factors.student_id)
        
        db_factors = EnvironmentalFactors(**factors.dict())
        db.add(db_factors)
        db.commit()
        db.refresh(db_factors)
        return db_factors
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_environmental_factors(db: Session, student_id: int) -> EnvironmentalFactors:
    factors = db.query(EnvironmentalFactors).filter(EnvironmentalFactors.student_id == student_id).first()
    if not factors:
        raise HTTPException(status_code=404, detail="Environmental factors not found")
    return factors

def update_environmental_factors(db: Session, student_id: int, factors: EnvironmentalFactorsUpdate) -> EnvironmentalFactors:
    db_factors = get_environmental_factors(db, student_id)
    update_data = factors.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_factors, field, value)
    
    try:
        db.commit()
        db.refresh(db_factors)
        return db_factors
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Complete Student operations
def create_complete_student(db: Session, student_data: CompleteStudentCreate) -> CompleteStudentResponse:
    try:
        # Create student
        student = create_student(
            db,
            StudentCreate(
                gender=student_data.gender,
                learning_disabilities=student_data.learning_disabilities,
                distance_from_home=student_data.distance_from_home
            )
        )

        # Create academic record
        academic_record = create_academic_record(
            db,
            AcademicRecordCreate(
                student_id=student.student_id,
                hours_studied=student_data.hours_studied,
                attendance=student_data.attendance,
                previous_scores=student_data.previous_scores,
                tutoring_sessions=student_data.tutoring_sessions,
                exam_score=student_data.exam_score
            )
        )

        # Create environmental factors
        env_factors = create_environmental_factors(
            db,
            EnvironmentalFactorsCreate(
                student_id=student.student_id,
                parental_involvement=student_data.parental_involvement,
                access_to_resources=student_data.access_to_resources,
                extracurricular_activities=student_data.extracurricular_activities,
                sleep_hours=student_data.sleep_hours,
                motivation_level=student_data.motivation_level,
                internet_access=student_data.internet_access,
                family_income=student_data.family_income,
                teacher_quality=student_data.teacher_quality,
                school_type=student_data.school_type,
                peer_influence=student_data.peer_influence,
                physical_activity=student_data.physical_activity,
                parental_education_level=student_data.parental_education_level
            )
        )

        return CompleteStudentResponse(
            student=student,
            academic_record=academic_record,
            environmental_factors=env_factors,
            predictions=[]
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_complete_student(db: Session, student_id: int) -> CompleteStudentResponse:
    student = get_student(db, student_id)
    academic_record = get_academic_record(db, student_id)
    env_factors = get_environmental_factors(db, student_id)
    
    return CompleteStudentResponse(
        student=student,
        academic_record=academic_record,
        environmental_factors=env_factors,
        predictions=[]  # Predictions will be added when prediction functionality is implemented
    )