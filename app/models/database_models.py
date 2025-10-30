"""
SQLAlchemy Database Models

ORM models for database tables
"""

from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, Enum as SQLEnum, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(SQLEnum('Male', 'Female', name='gender_enum'), nullable=False)
    learning_disabilities = Column(SQLEnum('Yes', 'No', name='yesno_enum'), nullable=False, default='No')
    distance_from_home = Column(SQLEnum('Near', 'Moderate', 'Far', name='distance_enum'), default='Moderate')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    academic_records = relationship("AcademicRecord", back_populates="student", cascade="all, delete-orphan")
    environmental_factors = relationship("EnvironmentalFactors", back_populates="student", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete-orphan")


class AcademicRecord(Base):
    __tablename__ = 'academic_records'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    hours_studied = Column(Integer)
    attendance = Column(Integer)
    previous_scores = Column(Integer)
    tutoring_sessions = Column(Integer, default=0)
    exam_score = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    student = relationship("Student", back_populates="academic_records")


class EnvironmentalFactors(Base):
    __tablename__ = 'environmental_factors'
    
    env_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    parental_involvement = Column(SQLEnum('Low', 'Medium', 'High', name='level_enum'), default='Medium')
    access_to_resources = Column(SQLEnum('Low', 'Medium', 'High', name='level_enum2'), default='Medium')
    extracurricular_activities = Column(SQLEnum('Yes', 'No', name='yesno_enum2'), default='No')
    sleep_hours = Column(Integer)
    motivation_level = Column(SQLEnum('Low', 'Medium', 'High', name='level_enum3'), default='Medium')
    internet_access = Column(SQLEnum('Yes', 'No', name='yesno_enum3'), default='Yes')
    family_income = Column(SQLEnum('Low', 'Medium', 'High', name='level_enum4'), default='Medium')
    teacher_quality = Column(SQLEnum('Low', 'Medium', 'High', name='level_enum5'), default='Medium')
    school_type = Column(SQLEnum('Public', 'Private', name='school_type_enum'), default='Public')
    peer_influence = Column(SQLEnum('Positive', 'Neutral', 'Negative', name='peer_influence_enum'), default='Neutral')
    physical_activity = Column(Integer)
    parental_education_level = Column(SQLEnum('High School', 'College', 'Postgraduate', name='education_enum'), default='High School')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    student = relationship("Student", back_populates="environmental_factors")


class Prediction(Base):
    __tablename__ = 'predictions'
    
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    predicted_score = Column(DECIMAL(5, 2))
    actual_score = Column(Integer, nullable=True)
    confidence_score = Column(DECIMAL(5, 4))
    prediction_date = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    student = relationship("Student", back_populates="predictions")
