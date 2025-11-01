import pandas as pd
from .mongodb_client import get_collection

def main():
    col = get_collection()
    docs = list(col.find({}, {"_id": 0}).limit(20))
    if not docs:
        print("No documents to export. Did you run load_data.py?")
        return
    df = pd.DataFrame(docs)
    out_path = "sample_export.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")

if __name__ == "__main__":
    main()
