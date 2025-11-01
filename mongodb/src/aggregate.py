from .mongodb_client import get_collection

def avg_scores_by_gender():
    col = get_collection()
    pipeline = [
        {"$group": {
            "_id": "$gender",
            "avg_math": {"$avg": "$math_score"},
            "avg_reading": {"$avg": "$reading_score"},
            "avg_writing": {"$avg": "$writing_score"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(col.aggregate(pipeline))

def top_n_by_math(n=5):
    col = get_collection()
    pipeline = [
        {"$sort": {"math_score": -1}},
        {"$limit": n},
        {"$project": {"gender": 1, "race": 1, "math_score": 1, "_id": 0}}
    ]
    return list(col.aggregate(pipeline))

def score_distribution(bucket=10):
    """Bucket math_score into ranges of width `bucket` (e.g., 0-9, 10-19, ...)."""
    col = get_collection()
    pipeline = [
        {"$match": {"math_score": {"$type": "number"}}},
        {"$project": {"bucket": {"$multiply": [{"$floor": {"$divide": ["$math_score", bucket]}}, bucket]}}},
        {"$group": {"_id": "$bucket", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(col.aggregate(pipeline))

def main():
    print("Avg scores by gender:")
    for row in avg_scores_by_gender():
        print(row)

    print("\nTop 5 by math score:")
    for row in top_n_by_math(5):
        print(row)

    print("\nMath score distribution (bucket=10):")
    for row in score_distribution(10):
        print(row)

if __name__ == "__main__":
    main()
