import sqlite3
import pandas as pd

df = pd.read_csv("data/processed/books.csv")
df = pd.read_csv("data/ratings.csv")

conn = sqlite3.connect("data/books.db")



def create_books_table(conn: sqlite3.Connection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    author      TEXT,
    genre       TEXT,
    description TEXT
    );
    """)
    conn.commit()

def insert_books(conn: sqlite3.Connection, df: pd.DataFrame):
    for _, row in df.iterrows():
        conn.execute(
        "INSERT INTO books (title, author, genre, description) VALUES (?, ?, ?, ?)",
        (row["title"], row.get("author"), row.get("genre"), row.get("description"))
        )
    conn.commit()

create_books_table(conn)
insert_books(conn, df)