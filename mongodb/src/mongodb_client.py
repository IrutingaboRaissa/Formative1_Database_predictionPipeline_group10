from pymongo import MongoClient
from .config import MONGODB_URI, DB_NAME, COLLECTION_NAME

def get_db():
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI is not set. Check your .env.")
    client = MongoClient(MONGODB_URI)
    return client[DB_NAME]

def get_collection():
    db = get_db()
    return db[COLLECTION_NAME]
