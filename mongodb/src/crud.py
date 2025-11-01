from datetime import datetime, timezone
from bson.objectid import ObjectId
from .mongodb_client import get_collection

def create_student(doc: dict):
    col = get_collection()
    doc = {**doc, "created_at": datetime.now(timezone.utc)}
    res = col.insert_one(doc)
    print(f"Created _id: {res.inserted_id}")
    return res.inserted_id

def read_latest(limit: int = 5):
    col = get_collection()
    docs = list(col.find({}).sort("created_at", -1).limit(limit))
    print(f"Latest {len(docs)} docs:")
    for d in docs:
        print({k: d[k] for k in d if k not in ["_id"]} | {"_id": str(d["_id"])})
    return docs

def update_one_by_id(_id: str, updates: dict):
    col = get_collection()
    res = col.update_one({"_id": ObjectId(_id)}, {"$set": updates})
    print(f"Matched: {res.matched_count}, modified: {res.modified_count}")
    return res.modified_count

def delete_one_by_id(_id: str):
    col = get_collection()
    res = col.delete_one({"_id": ObjectId(_id)})
    print(f"Deleted: {res.deleted_count}")
    return res.deleted_count

def main():
    # CREATE
    new_id = create_student({
        "gender": "male",
        "race": "group A",
        "parent_education": "associate degree",
        "lunch": "free/reduced",
        "test_prep_course": "completed",
        "math_score": 67,
        "reading_score": 72,
        "writing_score": 70
    })

    # READ
    read_latest(limit=3)

    # UPDATE
    update_one_by_id(str(new_id), {"math_score": 75})

    # DELETE (optional demo)
    # delete_one_by_id(str(new_id))

if __name__ == "__main__":
    main()



