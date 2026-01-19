import requests
import csv
from pathlib import Path

# Define constants
SUBJECTS = ["fantasy", "science_fiction", "romance", "history"]
LIMIT_PER_SUBJECT = 200

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
csv_path = RAW_DIR / "books_raw.csv"

fieldnames = ["work_key", "title", "first_publish_year", "authors", "source_subject"]

#fetch data from OpenLibrary API for a given subject
def fetch_subject(subject: str, limit: int = LIMIT_PER_SUBJECT):
    url = f"https://openlibrary.org/subjects/{subject}.json"
    params = {"limit": limit}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for subject in SUBJECTS:
        print(f"Fetching subject: {subject}")
        data = fetch_subject(subject)
        works = data.get("works", [])

        for w in works:
            title = w.get("title")
            year = w.get("first_publish_year")

            authors = []
            for a in w.get("authors", []):
                name = a.get("name")
                if name:
                    authors.append(name)

            row = {
                "work_key": w.get("key"),
                "title": title,
                "first_publish_year": year,
                "authors": "; ".join(authors),
                "source_subject": subject,
            }
            writer.writerow(row)

print(f"Saved raw books to {csv_path}")
