
class JsonToBookMapper:
    def __init__(self, json_data):
        self.json_data = json_data

    def map(self):
        mapped_books = []
        for item in self.json_data.get("works", []):
            book = {
                "work_key": item.get("key"),
                "title": item.get("title"),
                "first_publish_year": item.get("first_publish_year"),
                "authors": "; ".join([author.get("name") for author in item.get("authors", []) if author.get("name")]),
                "genre": self.json_data.get("name"),
                "subjects": "; ".join(item.get("subject", [])),
                "img_cover_url" : item.get("cover_id")
            }
            mapped_books.append(book)
        return mapped_books