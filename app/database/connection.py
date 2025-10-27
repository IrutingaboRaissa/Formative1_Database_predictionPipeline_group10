# DATABASE CONNECTION CONFIGURATION

import os
import mysql.connector
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MYSQL DATABASE CONNECTION

class MySQLDatabase:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "student_performance_db")
        
        # SQLAlchemy setup
        self.DATABASE_URL = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(
            self.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        
    def get_db(self):
        """Dependency for FastAPI to get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    def create_database_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect without database specified
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            connection.close()
            logging.info(f"Database '{self.database}' created or already exists")
        except Exception as e:
            logging.error(f"Error creating database: {e}")
            raise
            
    def execute_sql_file(self, sql_file_path: str):
        """Execute SQL file for database schema creation"""
        try:
            with open(sql_file_path, 'r') as file:
                sql_content = file.read()
            
            # Split by delimiter for stored procedures
            sql_statements = sql_content.split(';')
            
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = connection.cursor()
            for statement in sql_statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    cursor.execute(statement)
            
            connection.commit()
            cursor.close()
            connection.close()
            logging.info(f"SQL file '{sql_file_path}' executed successfully")
            
        except Exception as e:
            logging.error(f"Error executing SQL file: {e}")
            raise

# MONGODB CONNECTION

class MongoDatabase:
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGODB_DATABASE", "student_performance_nosql")
        self.client = None
        self.database = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            logging.info(f"Connected to MongoDB: {self.database_name}")
            return self.database
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise
            
    def get_collection(self, collection_name: str):
        """Get a specific collection"""
        if not self.database:
            self.connect()
        return self.database[collection_name]
        
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed")

# GLOBAL DATABASE INSTANCES

# Initialize database connections
mysql_db = MySQLDatabase()
mongo_db = MongoDatabase()

# Database dependency for FastAPI
def get_mysql_db():
    return mysql_db.get_db()

def get_mongo_db():
    return mongo_db.get_collection

# DATABASE INITIALIZATION FUNCTION

def initialize_databases():
    """Initialize both MySQL and MongoDB databases"""
    try:
        # Initialize MySQL
        mysql_db.create_database_if_not_exists()
        
        # Execute schema if SQL file exists
        sql_file = "student_performance_db_schema.sql"
        if os.path.exists(sql_file):
            mysql_db.execute_sql_file(sql_file)
        
        # Initialize MongoDB
        mongo_db.connect()
        
        # Create indexes for MongoDB collections
        students_collection = mongo_db.get_collection("students")
        students_collection.create_index("student_id", unique=True)
        
        academic_collection = mongo_db.get_collection("academic_records")
        academic_collection.create_index("student_id")
        
        env_collection = mongo_db.get_collection("environmental_factors")
        env_collection.create_index("student_id")
        
        predictions_collection = mongo_db.get_collection("predictions")
        predictions_collection.create_index([("student_id", 1), ("prediction_date", -1)])
        
        logging.info("All databases initialized successfully")
        
    except Exception as e:
        logging.error(f"Error initializing databases: {e}")
        raise

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize databases
    initialize_databases()
    print("✅ Database initialization completed!")