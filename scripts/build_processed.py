import csv
from pathlib import Path

RAW_PATH = Path("data/raw/books_raw.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUT_PATH = PROCESSED_DIR / "books.csv"

def load_raw_data():
    if RAW_PATH.exists() is False:
        raise FileNotFoundError(f"Raw data file not found: {RAW_PATH}")
    
    with RAW_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Loaded {len(rows)} rows from {RAW_PATH}")
    return rows

def dedup_by_work_key(rows):
    seen_work_keys = set()
    unique_rows = []
    missing_work_key_count = 0
    duplicate_count = 0

    for row in rows:
        work_key = row.get("work_key")
        if not work_key:
            missing_work_key_count += 1
            continue
        if work_key in seen_work_keys:
            duplicate_count += 1
            continue
        seen_work_keys.add(work_key)
        unique_rows.append(row)
    print(f"Rows with missing work_key: {missing_work_key_count}")
    print(f"Duplicate rows skipped: {duplicate_count}")
    print(f"Unique rows kept: {len(unique_rows)}")
    return unique_rows

def save_processed_data(rows):
    if not rows:
        print("No data to save.")
        return
    fieldnames = rows[0].keys()
    with OUT_PATH.open("w",encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Processed data saved to {OUT_PATH}")

def main():
    raw_rows = load_raw_data()
    unique_rows = dedup_by_work_key(raw_rows)
    save_processed_data(unique_rows)

    
if __name__ == "__main__":
    main()