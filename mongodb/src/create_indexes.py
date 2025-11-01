from pymongo import ASCENDING, DESCENDING
from .mongodb_client import get_collection

def main():
    col = get_collection()
    print(f"Creating indexes on '{col.name}'...")

    col.create_index([("gender", ASCENDING)], name="idx_gender")
    col.create_index([("race", ASCENDING)], name="idx_race")
    col.create_index([("math_score", DESCENDING)], name="idx_math_score_desc")
    col.create_index([("created_at", DESCENDING)], name="idx_created_at_desc")
    # Example compound index if you often filter by gender + course (if exists)
    # col.create_index([("gender", ASCENDING), ("course", ASCENDING)], name="idx_gender_course")

    print("✅ Indexes created.")

if __name__ == "__main__":
    main()
