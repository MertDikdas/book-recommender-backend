## Book Recommender – Backend
Backend service of a Book Recommender System built with FastAPI and SQLAlchemy.
This API provides book management, rating, comment handling, and user-book relationship tracking.

## System Requirements

- Python 3.9+
- Git
- bash (if your os is Windows you can use git bash)
- pip

## Installation
## Clone repository
```bash
git clone https://github.com/MertDikdas/book-recommender-backend.git
cd book-recommender-backend
```
## Create virtual environment (optional but recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
```
```bash
python -m venv .venv
source .venv/Scripts/Activate # Windows
```
## Install dependencies
```bash
pip install -r requirements.txt
```
## Pull books from open library
```bash
python -m src.database.create_db #Database creation
python -m src.api.open_library_api.seed_from_api #Pull book from open lib. to database
```
## Run the server
```bash
uvicorn src.api.api:app --reload
```
Server runs at:
http://127.0.0.1:8000
Swagger documentation:
http://127.0.0.1:8000/docs
## Tech Stack
FastAPI – REST API framework
SQLAlchemy – ORM
Pydantic – Data validation
SQLite – Database
OpenLibrary API – External data source
## Features
Book listing & filtering
User rating system
Comment system
User-book relationship tracking
Add/remove books from user list
Book cover URL storage & retrieval
RESTful API design
Modular service/repository architecture
Architecture
## The backend follows a layered structure:
src/
 ├── api/            # Route definitions and book api
 ├── services/       # Business logic
 ├── repositories/   # Database operations
 ├── models/         # SQLAlchemy models
 ├── schemas/        # Pydantic schemas
 └── database.py     # DB configuration
Separation of concerns is applied to ensure scalability and maintainability.
## Database Schema
Main entities:
Users
Books
Ratings
Comments
## Author
Mert Dikdaş
Computer Engineering Student
Ege University


