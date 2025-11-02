"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Student schemas
class StudentBase(BaseModel):
    gender: str
    learning_disabilities: str
    distance_from_home: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    gender: Optional[str] = None
    learning_disabilities: Optional[str] = None
    distance_from_home: Optional[str] = None

class StudentResponse(StudentBase):
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Academic Record schemas
class AcademicRecordBase(BaseModel):
    hours_studied: int
    attendance: int
    previous_scores: int
    tutoring_sessions: int
    exam_score: Optional[int] = None

class AcademicRecordCreate(AcademicRecordBase):
    student_id: int

class AcademicRecordUpdate(AcademicRecordBase):
    hours_studied: Optional[int] = None
    attendance: Optional[int] = None
    previous_scores: Optional[int] = None
    tutoring_sessions: Optional[int] = None
    exam_score: Optional[int] = None

class AcademicRecordResponse(AcademicRecordBase):
    record_id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Environmental Factors schemas
class EnvironmentalFactorsBase(BaseModel):
    parental_involvement: str
    access_to_resources: str
    extracurricular_activities: str
    sleep_hours: int
    motivation_level: str
    internet_access: str
    family_income: str
    teacher_quality: str
    school_type: str
    peer_influence: str
    physical_activity: int
    parental_education_level: str

class EnvironmentalFactorsCreate(EnvironmentalFactorsBase):
    student_id: int

class EnvironmentalFactorsUpdate(EnvironmentalFactorsBase):
    parental_involvement: Optional[str] = None
    access_to_resources: Optional[str] = None
    extracurricular_activities: Optional[str] = None
    sleep_hours: Optional[int] = None
    motivation_level: Optional[str] = None
    internet_access: Optional[str] = None
    family_income: Optional[str] = None
    teacher_quality: Optional[str] = None
    school_type: Optional[str] = None
    peer_influence: Optional[str] = None
    physical_activity: Optional[int] = None
    parental_education_level: Optional[str] = None

class EnvironmentalFactorsResponse(EnvironmentalFactorsBase):
    env_id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Prediction schemas
class PredictionBase(BaseModel):
    predicted_score: float
    actual_score: Optional[int] = None
    confidence_score: float

class PredictionCreate(PredictionBase):
    student_id: int

class PredictionResponse(PredictionBase):
    prediction_id: int
    student_id: int
    prediction_date: datetime

    class Config:
        from_attributes = True

# Complete student data
class CompleteStudentCreate(BaseModel):
    student: StudentCreate
    academic_record: AcademicRecordBase
    environmental_factors: EnvironmentalFactorsBase

class CompleteStudentResponse(BaseModel):
    student: StudentResponse
    academic_record: Optional[AcademicRecordResponse] = None
    environmental_factors: Optional[EnvironmentalFactorsResponse] = None
    predictions: Optional[list[PredictionResponse]] = []

class CompleteStudentData(BaseModel):
    student: StudentResponse
    academic_record: Optional[AcademicRecordResponse] = None
    environmental_factors: Optional[EnvironmentalFactorsResponse] = None
    predictions: Optional[list[PredictionResponse]] = []



