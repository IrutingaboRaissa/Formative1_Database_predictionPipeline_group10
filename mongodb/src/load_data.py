import re
from datetime import datetime, timezone
import pandas as pd
from .config import DATA_CSV_PATH
from .mongodb_client import get_collection

def to_snake(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("/", " ").replace("-", " ")
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s

def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    # Try to convert any column with "score", "age", "id" to numeric if possible
    for c in df.columns:
        if any(k in c for k in ["score", "age", "id", "math", "reading", "writing"]):
            df[c] = pd.to_numeric(df[c], errors="ignore")
    return df

def main():
    print(f"Loading CSV from: {DATA_CSV_PATH}")
    df = pd.read_csv(DATA_CSV_PATH)

    # Standardize columns
    df.columns = [to_snake(c) for c in df.columns]
    df = coerce_numeric(df)

    # Add audit fields
    df["created_at"] = datetime.now(timezone.utc)

    records = df.to_dict(orient="records")

    col = get_collection()
    # Optional: Clear existing if you want a clean import each run
    # col.delete_many({})

    if not records:
        print("No records found in CSV.")
        return

    res = col.insert_many(records)
    print(f"✅ Inserted {len(res.inserted_ids)} documents into '{col.name}'")

if __name__ == "__main__":
    main()
