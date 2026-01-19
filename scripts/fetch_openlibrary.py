
import requests

#URL for fantasy books in Open Library
url = "https://openlibrary.org/subjects/fantasy.json"
#limit to 5 results for testing
params = {"limit":10}

#makee the request
r = requests.get(url,params=params,timeout= 30)
print(r.status_code)
print(r.url)

#parse the json response
data = r.json()
print(type(data))
print(list(data.keys())[:20])
#get the list of works
works = data['works']
print("works type: ", type(works))
print("number of works: ", len(works))

#print each work's title, first publish year, and authors
for i, w in enumerate(works, start=1):
    title = w.get("title")
    year = w.get("first_publish_year")

    authors = [
        a.get("name")
        for a in w.get("authors", [])
        if a.get("name")
    ]

    print(f"{i}) {title} ({year}) - {', '.join(authors)}")

#save the data to a CSV file
import csv
from pathlib import Path
Path("data/raw").mkdir(parents=True, exist_ok=True)
csv_path = Path("data/raw/fantasy_books.csv") 
#define the CSV field names
fieldnames = ["title", "first_publish_year", "authors"]

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for w in works:
        title = w.get("title")
        year = w.get("first_publish_year")
        authors = []
        for a in w.get("authors", []):
            name = a.get("name")
            if name:
                authors.append(name)
        row = {"title": title, "first_publish_year": year, "authors": "; ".join(authors)}
        writer.writerow(row)
