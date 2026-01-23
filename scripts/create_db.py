from scripts.database import Base, engine
import scripts.models  #importing all models

Base.metadata.create_all(bind=engine)

print("Tables created.")