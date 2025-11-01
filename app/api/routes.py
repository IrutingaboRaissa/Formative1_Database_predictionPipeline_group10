from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database.connection import get_mysql_db
from ..models.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    AcademicRecordCreate, AcademicRecordUpdate, AcademicRecordResponse,
    EnvironmentalFactorsCreate, EnvironmentalFactorsUpdate, EnvironmentalFactorsResponse,
    CompleteStudentCreate, CompleteStudentResponse
)
from . import crud

router = APIRouter()

# Student endpoints
@router.post("/students/", response_model=StudentResponse, tags=["students"])
def create_student(student: StudentCreate, db: Session = Depends(get_mysql_db)):
    """Create a new student record"""
    return crud.create_student(db, student)

@router.get("/students/", response_model=List[StudentResponse], tags=["students"])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_mysql_db)):
    """Get all students with pagination"""
    return crud.get_students(db, skip=skip, limit=limit)

@router.get("/students/{student_id}", response_model=StudentResponse, tags=["students"])
def read_student(student_id: int, db: Session = Depends(get_mysql_db)):
    """Get a specific student by ID"""
    return crud.get_student(db, student_id)

@router.put("/students/{student_id}", response_model=StudentResponse, tags=["students"])
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_mysql_db)):
    """Update a student's information"""
    return crud.update_student(db, student_id, student)

@router.delete("/students/{student_id}", tags=["students"])
def delete_student(student_id: int, db: Session = Depends(get_mysql_db)):
    """Delete a student"""
    crud.delete_student(db, student_id)
    return {"message": "Student deleted successfully"}

# Academic Record endpoints
@router.post("/students/{student_id}/academic", response_model=AcademicRecordResponse, tags=["academic"])
def create_academic_record(
    student_id: int,
    record: AcademicRecordCreate,
    db: Session = Depends(get_mysql_db)
):
    """Create an academic record for a student"""
    record.student_id = student_id
    return crud.create_academic_record(db, record)

@router.get("/students/{student_id}/academic", response_model=AcademicRecordResponse, tags=["academic"])
def read_academic_record(student_id: int, db: Session = Depends(get_mysql_db)):
    """Get a student's academic record"""
    return crud.get_academic_record(db, student_id)

@router.put("/students/{student_id}/academic", response_model=AcademicRecordResponse, tags=["academic"])
def update_academic_record(
    student_id: int,
    record: AcademicRecordUpdate,
    db: Session = Depends(get_mysql_db)
):
    """Update a student's academic record"""
    return crud.update_academic_record(db, student_id, record)

# Environmental Factors endpoints
@router.post("/students/{student_id}/environmental", response_model=EnvironmentalFactorsResponse, tags=["environmental"])
def create_environmental_factors(
    student_id: int,
    factors: EnvironmentalFactorsCreate,
    db: Session = Depends(get_mysql_db)
):
    """Create environmental factors record for a student"""
    factors.student_id = student_id
    return crud.create_environmental_factors(db, factors)

@router.get("/students/{student_id}/environmental", response_model=EnvironmentalFactorsResponse, tags=["environmental"])
def read_environmental_factors(student_id: int, db: Session = Depends(get_mysql_db)):
    """Get a student's environmental factors"""
    return crud.get_environmental_factors(db, student_id)

@router.put("/students/{student_id}/environmental", response_model=EnvironmentalFactorsResponse, tags=["environmental"])
def update_environmental_factors(
    student_id: int,
    factors: EnvironmentalFactorsUpdate,
    db: Session = Depends(get_mysql_db)
):
    """Update a student's environmental factors"""
    return crud.update_environmental_factors(db, student_id, factors)

# Complete Student endpoints
@router.post("/students/complete/", response_model=CompleteStudentResponse, tags=["complete"])
def create_complete_student(student: CompleteStudentCreate, db: Session = Depends(get_mysql_db)):
    """Create a complete student record with academic and environmental data"""
    return crud.create_complete_student(db, student)

@router.get("/students/{student_id}/complete/", response_model=CompleteStudentResponse, tags=["complete"])
def read_complete_student(student_id: int, db: Session = Depends(get_mysql_db)):
    """Get complete student information including academic and environmental data"""
    return crud.get_complete_student(db, student_id)