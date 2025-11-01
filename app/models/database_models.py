from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.connection import MySQLDatabase

Base = MySQLDatabase().Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(10), nullable=False)
    learning_disabilities = Column(String(3), nullable=False, default="No")
    distance_from_home = Column(String(10), default="Moderate")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    academic_records = relationship("AcademicRecord", back_populates="student", cascade="all, delete")
    environmental_factors = relationship("EnvironmentalFactors", back_populates="student", cascade="all, delete")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete")

class AcademicRecord(Base):
    __tablename__ = "academic_records"

    record_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    hours_studied = Column(Integer)
    attendance = Column(Integer)
    previous_scores = Column(Integer)
    tutoring_sessions = Column(Integer, default=0)
    exam_score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="academic_records")

class EnvironmentalFactors(Base):
    __tablename__ = "environmental_factors"

    env_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    parental_involvement = Column(String(10), default="Medium")
    access_to_resources = Column(String(10), default="Medium")
    extracurricular_activities = Column(String(3), default="No")
    sleep_hours = Column(Integer)
    motivation_level = Column(String(10), default="Medium")
    internet_access = Column(String(3), default="Yes")
    family_income = Column(String(10), default="Medium")
    teacher_quality = Column(String(10), default="Medium")
    school_type = Column(String(10), default="Public")
    peer_influence = Column(String(10), default="Neutral")
    physical_activity = Column(Integer)
    parental_education_level = Column(String(20), default="High School")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="environmental_factors")

class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    predicted_score = Column(Float)
    actual_score = Column(Integer, nullable=True)
    model_version = Column(String(50), default="v1.0")
    confidence_score = Column(Float)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="predictions")