# DATABASE MODELS (Pydantic for FastAPI)

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

# ENUMS FOR VALIDATION

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class YesNo(str, Enum):
    YES = "Yes"
    NO = "No"

class Level(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Distance(str, Enum):
    NEAR = "Near"
    MODERATE = "Moderate" 
    FAR = "Far"

class SchoolType(str, Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"

class PeerInfluence(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"

class Education(str, Enum):
    HIGH_SCHOOL = "High School"
    COLLEGE = "College"
    POSTGRADUATE = "Postgraduate"

# REQUEST MODELS (For Creating Records)

class StudentCreate(BaseModel):
    gender: Gender
    learning_disabilities: YesNo = YesNo.NO
    distance_from_home: Optional[Distance] = Distance.MODERATE

class AcademicRecordCreate(BaseModel):
    student_id: int
    hours_studied: int = Field(ge=0, le=50, description="Hours studied per week")
    attendance: int = Field(ge=0, le=100, description="Attendance percentage")
    previous_scores: int = Field(ge=0, le=100, description="Previous exam scores")
    tutoring_sessions: int = Field(ge=0, description="Number of tutoring sessions")
    exam_score: int = Field(ge=0, le=110, description="Current exam score")

class EnvironmentalFactorsCreate(BaseModel):
    student_id: int
    parental_involvement: Level = Level.MEDIUM
    access_to_resources: Level = Level.MEDIUM
    extracurricular_activities: YesNo = YesNo.NO
    sleep_hours: int = Field(ge=4, le=12, description="Hours of sleep per day")
    motivation_level: Level = Level.MEDIUM
    internet_access: YesNo = YesNo.YES
    family_income: Level = Level.MEDIUM
    teacher_quality: Optional[Level] = Level.MEDIUM
    school_type: SchoolType = SchoolType.PUBLIC
    peer_influence: PeerInfluence = PeerInfluence.NEUTRAL
    physical_activity: int = Field(ge=0, le=10, description="Physical activity level")
    parental_education_level: Optional[Education] = Education.HIGH_SCHOOL

class PredictionCreate(BaseModel):
    student_id: int
    predicted_score: float = Field(ge=0, le=110, description="ML predicted exam score")
    actual_score: Optional[int] = Field(None, ge=0, le=110, description="Actual exam score")
    model_version: str = "v1.0"
    confidence_score: float = Field(ge=0, le=1, description="Prediction confidence")

# =============================================================================
# RESPONSE MODELS (For API Responses)
# =============================================================================

class StudentResponse(BaseModel):
    student_id: int
    gender: Gender
    learning_disabilities: YesNo
    distance_from_home: Optional[Distance]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AcademicRecordResponse(BaseModel):
    record_id: int
    student_id: int
    hours_studied: int
    attendance: int
    previous_scores: int
    tutoring_sessions: int
    exam_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnvironmentalFactorsResponse(BaseModel):
    env_id: int
    student_id: int
    parental_involvement: Level
    access_to_resources: Level
    extracurricular_activities: YesNo
    sleep_hours: int
    motivation_level: Level
    internet_access: YesNo
    family_income: Level
    teacher_quality: Optional[Level]
    school_type: SchoolType
    peer_influence: PeerInfluence
    physical_activity: int
    parental_education_level: Optional[Education]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    prediction_id: int
    student_id: int
    predicted_score: float
    actual_score: Optional[int]
    model_version: str
    confidence_score: float
    prediction_date: datetime
    
    class Config:
        from_attributes = True

# COMPREHENSIVE MODELS (For Complete Operations)

class CompleteStudentCreate(BaseModel):
    """Model for creating a complete student record with all related data"""
    # Student info
    gender: Gender
    learning_disabilities: YesNo = YesNo.NO
    distance_from_home: Optional[Distance] = Distance.MODERATE
    
    # Academic info
    hours_studied: int = Field(ge=0, le=50)
    attendance: int = Field(ge=0, le=100) 
    previous_scores: int = Field(ge=0, le=100)
    tutoring_sessions: int = Field(ge=0)
    exam_score: int = Field(ge=0, le=110)
    
    # Environmental info
    parental_involvement: Level = Level.MEDIUM
    access_to_resources: Level = Level.MEDIUM
    extracurricular_activities: YesNo = YesNo.NO
    sleep_hours: int = Field(ge=4, le=12)
    motivation_level: Level = Level.MEDIUM
    internet_access: YesNo = YesNo.YES
    family_income: Level = Level.MEDIUM
    teacher_quality: Optional[Level] = Level.MEDIUM
    school_type: SchoolType = SchoolType.PUBLIC
    peer_influence: PeerInfluence = PeerInfluence.NEUTRAL
    physical_activity: int = Field(ge=0, le=10)
    parental_education_level: Optional[Education] = Education.HIGH_SCHOOL

class CompleteStudentResponse(BaseModel):
    """Complete student information with all related data"""
    student: StudentResponse
    academic_record: Optional[AcademicRecordResponse]
    environmental_factors: Optional[EnvironmentalFactorsResponse]
    predictions: list[PredictionResponse] = []

# UPDATE MODELS

class StudentUpdate(BaseModel):
    gender: Optional[Gender] = None
    learning_disabilities: Optional[YesNo] = None
    distance_from_home: Optional[Distance] = None

class AcademicRecordUpdate(BaseModel):
    hours_studied: Optional[int] = Field(None, ge=0, le=50)
    attendance: Optional[int] = Field(None, ge=0, le=100)
    previous_scores: Optional[int] = Field(None, ge=0, le=100)
    tutoring_sessions: Optional[int] = Field(None, ge=0)
    exam_score: Optional[int] = Field(None, ge=0, le=110)

class EnvironmentalFactorsUpdate(BaseModel):
    parental_involvement: Optional[Level] = None
    access_to_resources: Optional[Level] = None
    extracurricular_activities: Optional[YesNo] = None
    sleep_hours: Optional[int] = Field(None, ge=4, le=12)
    motivation_level: Optional[Level] = None
    internet_access: Optional[YesNo] = None
    family_income: Optional[Level] = None
    teacher_quality: Optional[Level] = None
    school_type: Optional[SchoolType] = None
    peer_influence: Optional[PeerInfluence] = None
    physical_activity: Optional[int] = Field(None, ge=0, le=10)
    parental_education_level: Optional[Education] = None