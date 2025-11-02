"""
Database connection management
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# MySQL connection
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "student_performance_db")

MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create engine
mysql_engine = create_engine(MYSQL_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

Base = declarative_base()

def get_mysql_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_databases():
    """Initialize database connections on startup"""
    print("Initializing database connections...")
    try:
        # Test MySQL connection
        with mysql_engine.connect() as conn:
            print("MySQL connection successful")
    except Exception as e:
        print(f"MySQL connection failed: {e}")



