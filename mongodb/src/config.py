import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "student_performance_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "students")

DATA_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "student_performance_data.csv")
