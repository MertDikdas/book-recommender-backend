from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
import math


#Pydantic models
#Create
class UserCreate(BaseModel):
    username: str

class BookCreate(BaseModel):
    title: str
    work_key: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    img_cover_url : Optional[str] = None

class CommentCreate(BaseModel):
    book_id:int
    username: str
    comment_text:str = Field(min_length=1, max_length=2000)

class RatingCreate(BaseModel):
    username: str
    book_id: int
    rating: int


#Response
class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)
    

class BookOut(BaseModel):
    id: int
    work_key: str
    title: str
    author: str
    genre: Optional[str] = None
    description: Optional[str] = None
    img_cover_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("img_cover_url", mode="before")
    @classmethod
    def convert_nan_to_none(cls, v):
        if v is None:
            return None

        # pandas / numpy nan kontrolü
        try:
            import pandas as pd
            if pd.isna(v):
                return None
        except Exception:
            pass

        # float nan kontrolü
        if isinstance(v, float) and math.isnan(v):
            return None

        return str(v)
    
class CommentOut(BaseModel):
    id: int
    user_id: int
    username: Optional[str] = None
    book_id: int
    comment_text: str
    model_config = ConfigDict(from_attributes=True)


class RatingOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True)



