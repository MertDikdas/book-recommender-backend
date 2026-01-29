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
    (df["author"].fillna("") + " "*5) +
    (df["genre"].fillna("") + " ") +
    df["description"].fillna("") 
)

# Vectorize the text data
vectorizer = TfidfVectorizer(
    stop_words="english"
)

# Vectorize the weighted text data for improved recommendations
X_w = vectorizer.fit_transform(df["text_weighted"])



# Recommendation function for a user based on their ratings
def recommend_for_user(user_ratings, top_k=10) -> list[BookEntity]:
    # If user has no ratings, return random books
    if user_ratings.empty:
        return [BookEntity(**row.to_dict()) for _, row in df.sample(top_k).iterrows()]
    item_vectors = []
    weights = []
    # Build user profile
    for row in user_ratings.itertuples(index=False):
        rating = row.rating
        idx = row.id
        v = X_w[idx].toarray()[0]
        item_vectors.append(v)
        weights.append(rating)
    # Create user profile as weighted average of item vectors    
    item_matrix = np.vstack(item_vectors)
    weights = np.array(weights)
    user_profile = np.average(item_matrix, axis=0, weights=weights)
    # Compute similarity scores
    similarity_scores = cosine_similarity(user_profile.reshape(1, -1), X_w).ravel()
    # Exclude already rated books
    rated_idx = {row.id for _, row in user_ratings.iterrows()}
    # Get top-k recommendations
    idx_scores = list(enumerate(similarity_scores))
    idx_scores = [
        (i, s) for i, s in idx_scores
        if i not in rated_idx 
    ] 
    # Sort by score and get top-k 
    top_idx = sorted(idx_scores, key=lambda x: x[1], reverse=True)
    # Get only indices
    top_idx = [i for i, s in top_idx[:top_k]]
    return [BookEntity(**df.iloc[i].to_dict()) for i in top_idx]
