from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.database.pull_books_from_db import pull_books_from_db
from src.database.database import SessionLocal
from src.domains.entities.book_entity import BookEntity
import pandas as pd
import numpy as np

# Load processed data
db = SessionLocal()
df = pull_books_from_db(db)

# Create a weighted text field with more emphasis on source_subject
df["text_weighted"] = (
    df["title"].fillna("") + " " +
    df["author"].fillna("") + " " +
    (df["genre"].fillna("") + " ") * 3 +
    (df["description"].fillna(" ") + " ") * 3
)

# Vectorize the text data
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
)

# Vectorize the weighted text data for improved recommendations
X_w = vectorizer.fit_transform(df["text_weighted"])

work_key_to_pos = {
    str(wk): i
    for i, wk in enumerate(df["work_key"].tolist())
}


# Recommendation function for a user based on their ratings
# min_k and max_k are used for pagination of recommendations
def recommend_for_user(user_ratings, user_books, min_k,max_k=20) -> list[BookEntity] | None:
    # If user has no ratings, return random books
    if len(user_ratings) == 0:
        return [BookEntity(id = df.iloc[i]["id"], work_key=df.iloc[i]["work_key"], title=df.iloc[i]["title"], author=df.iloc[i]["author"], genre=df.iloc[i]["genre"], description=df.iloc[i]["description"]) for i in df.sample(max_k).index]
    item_vectors = []
    weights = []
    # Build user profile
    for row in user_ratings:
        if row.book_id not in user_books:
            continue
        rating = row.rating
        wk = user_books[row.book_id].work_key
        pos = work_key_to_pos.get(wk)
        if pos is None:
            continue
        v = X_w[pos].toarray()[0]
        item_vectors.append(v)
        weights.append(rating)
    if not item_vectors:
        return [
            BookEntity(
                id=df.iloc[i]["id"],
                work_key=df.iloc[i]["work_key"],
                title=df.iloc[i]["title"],
                author=df.iloc[i]["author"],
                genre=df.iloc[i]["genre"],
                description=df.iloc[i]["description"],
            )
            for i in df.sample(max_k).index
        ]
    # Create user profile as weighted average of item vectors    
    item_matrix = np.vstack(item_vectors)
    weights = np.array(weights)  # Center ratings around 0 (assuming ratings are from 1 to 5)
    user_profile = np.average(item_matrix, axis=0, weights=weights)
    # Compute similarity scores
    similarity_scores = cosine_similarity(user_profile.reshape(1, -1), X_w).ravel()
    # Exclude already rated books
    # Get top-k recommendations
    rated_idx = {
        work_key_to_pos.get(user_books[row.book_id].work_key)
        for row in user_ratings
        if work_key_to_pos.get(user_books[row.book_id].work_key) is not None
    }
    idx_scores = list(enumerate(similarity_scores))
    idx_scores = [
        (i, s) for i, s in idx_scores
        if i not in rated_idx 
    ] 
    # Sort by score and get top-k 
    top_idx = sorted(idx_scores, key=lambda x: x[1], reverse=True)
    # Get only indices
    top_idx = [i for i, s in top_idx[min_k:max_k]]
    return [BookEntity(id = df.iloc[i]["id"],work_key=df.iloc[i]["work_key"], title=df.iloc[i]["title"], author=df.iloc[i]["author"], genre=df.iloc[i]["genre"], description=df.iloc[i]["description"]) for i in top_idx]