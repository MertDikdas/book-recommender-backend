import requests
import csv
import numpy as np
import pandas as pd
from pathlib import Path

# Define constants
SUBJECTS = ["fantasy"] #, "science_fiction", "romance", "history","literature","mystery_and_detective_stories", "juvenile_literature",
             #"autobiography","programming","psychology","poetry","short_stories","young_adult_fiction", "biology", "chemistry","mathematics",
             #"business__economics", "finance", "ancient_civilization","archaeology","cooking"]
LIMIT_PER_SUBJECT = 2000
PER_REQUEST_LIMIT = 1000
BASE_URL = "https://openlibrary.org"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
csv_path = RAW_DIR / "books_raw.csv"

fieldnames = ["work_key", "title", "first_publish_year", "authors", "source_subject","subjects"]

#fetch data from OpenLibrary API for a given subject

def fetch_subject(subject: str, limit: int = PER_REQUEST_LIMIT, offset: int = 0) -> dict:
    params = {
        "limit": min(limit, PER_REQUEST_LIMIT),  # tek istekte max 1000
        "offset": offset,
    }
    r = requests.get(f"{BASE_URL}/subjects/{subject}.json", params=params, timeout=15)
    r.raise_for_status()
    return r.json()
"""
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
            subjects = []
            for s in w.get("subject", []):
                subjects.append(s)
            

            row = {
                "work_key": w.get("key"),
                "title": title,
                "first_publish_year": year,
                "authors": "; ".join(authors),
                "subjects": "; ".join(subjects),
                "source_subject": subject,
            }
            writer.writerow(row)
print(f"Saved raw books to {csv_path}")
"""

