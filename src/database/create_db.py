from src.database.database import Base, engine 
from src.domains.orm import BookORM, UserORM, RatingORM

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    create_tables()