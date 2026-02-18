import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Define constants
SUBJECTS = ["fantasy", "science_fiction", "romance", "history","literature","mystery_and_detective_stories", "juvenile_literature",
             "autobiography","programming","psychology","poetry","short_stories","young_adult_fiction", "biology", "chemistry","mathematics",
             "business__economics", "finance", "ancient_civilization","archaeology","cooking"]
LIMIT_PER_SUBJECT = 15000
PER_REQUEST_LIMIT = 1000
BASE_URL = "https://openlibrary.org"
BASE_TURKISH = "https://openlibrary.org/search.json"

session = requests.Session()
retries = Retry(
    total=8,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
session.mount("https://", HTTPAdapter(max_retries=retries))

#fetch data from OpenLibrary API for a given subject

def fetch_subject(subject: str, limit: int = PER_REQUEST_LIMIT, offset: int = 0) -> dict:
    params = {"limit": min(limit, PER_REQUEST_LIMIT), "offset": offset}
    headers = {"User-Agent": "BookRecommenderSeeder/1.0 (contact: you@example.com)"}
    r = session.get(f"{BASE_URL}/subjects/{subject}.json", params=params, headers=headers, timeout=30)
    r.raise_for_status()
    print(f"{subject} offset={offset} OK")
    return r.json()




def fetch_tr_books(query="language:tur", page=1, limit=100):
    params = {"q": query, "page": page, "limit": limit}
    headers = {"User-Agent": "BookSeeder/1.0"}
    r = requests.get(BASE_TURKISH, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()
