
class JsonToBookMapper:
    def __init__(self, json_data):
        self.json_data = json_data

    def map(self, works:str):
        mapped_books = []
        for item in self.json_data.get(works, []):

            if item.get("cover_id"):
                img_cover_url = f"https://covers.openlibrary.org/b/id/{item.get("cover_id")}-L.jpg"
            elif item.get("edition_key"):
                img_cover_url = f"https://covers.openlibrary.org/b/olid/{item.get("cover_edition_key")}-L.jpg"
            else:
                img_cover_url = None
            book = {
                "work_key": item.get("key"),
                "title": item.get("title"),
                "first_publish_year": item.get("first_publish_year"),
                "authors": "; ".join([author.get("name") for author in item.get("authors", []) if author.get("name")]),
                "genre": self.json_data.get("name"), 
                "description": "; ".join(item.get("subject", [])),
                "img_cover_url" : img_cover_url
            }
            mapped_books.append(book)
        return mapped_books
