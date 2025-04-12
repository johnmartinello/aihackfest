from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class BookSearchRequest(BaseModel):
    query: str

class MoreBooksRequest(BaseModel):
    search_id: int
    count: int = 8

class BookResponse(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    cover_url: Optional[str] = None
    first_publish_year: Optional[int] = None
    edition_count: Optional[int] = None
    has_fulltext: Optional[bool] = None
    genre: Optional[str] = None  # Added genre field
    reason: Optional[str] = None
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class BookSearchResponse(BaseModel):
    id: int
    query: str
    created_at: datetime
    books: List[BookResponse]
    
    class Config:
        from_attributes = True  # Updated from orm_mode