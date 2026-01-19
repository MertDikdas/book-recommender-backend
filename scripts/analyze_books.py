import csv
from pathlib import Path

csv_path = Path("data/raw/books_raw.csv")

with csv_path.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total = len(rows)
missing_year = 0

for row in rows:
    year = row["first_publish_year"]
    if year == "" or year is None:
        missing_year += 1

ratio = missing_year / total if total > 0 else 0
print(f"missing_year: {missing_year}/{total} ({ratio:.2%})")
