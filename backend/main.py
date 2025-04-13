from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

from app.models import get_db, create_tables, BookSearch, Book
from app.schemas import BookSearchRequest, BookSearchResponse, BookResponse, MoreBooksRequest
from app.ai_service import get_book_recommendations, generate_user_profile
from app.library_service import search_book_by_title, extract_book_info

# New schema for profile generation
class UserProfileRequest(BaseModel):
    queries: List[str]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Book Recommendation API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "Book Recommendation API is running"}

@app.post("/api/generate-profile")
async def create_user_profile(request: UserProfileRequest):
    """
    Generate a funny user profile based on search history
    """
    if len(request.queries) < 2:
        raise HTTPException(status_code=400, detail="At least 2 search queries are required to generate a profile")
    
    # Get the streaming response from the AI service
    stream_response = await generate_user_profile(request.queries)
    
    # Create an async generator that yields chunks of the response
    async def profile_stream_generator():
        try:
            async for chunk in stream_response:
                if hasattr(chunk, "text"):
                    yield chunk.text
        except Exception as e:
            yield f"Error generating profile: {str(e)}"
    
    # Return a StreamingResponse that will stream the content to the client
    return StreamingResponse(
        profile_stream_generator(),
        media_type="text/plain"
    )

@app.post("/api/search", response_model=BookSearchResponse)
async def search_books(request: BookSearchRequest, db: Session = Depends(get_db)):
    """
    Search for book recommendations based on user query
    """
    books = await get_book_recommendations(request.query)
    
    if not isinstance(books, list):
        try:
            if isinstance(books, str):
                books = json.loads(books)
            if not isinstance(books, list):
                books = [books]
        except Exception as e:
            print(f"Error parsing book recommendations: {e}")
            books = []
    
    # 2. Save search query to database
    book_search = BookSearch(
        query=request.query,
        llm_response=json.dumps(books)
    )
    db.add(book_search)
    db.commit()
    db.refresh(book_search)
    
    # 3. For each recommended book, fetch details from Open Library
    books_data = []
    for book in books:
        if not isinstance(book, dict) or "title" not in book:
            continue
            
        # Search Open Library for book info
        library_data = await search_book_by_title(book["title"])
        
        if library_data and "docs" in library_data and library_data["docs"]:
            book_info = extract_book_info(library_data)
            
            if book_info:
                db_book = Book(
                    search_id=book_search.id,
                    title=book_info["title"],
                    author=book_info["author"],
                    cover_url=book_info["cover_url"],
                    first_publish_year=book_info["first_publish_year"],
                    edition_count=book_info["edition_count"],
                    has_fulltext=book_info["has_fulltext"],
                    genre=book.get("genre", "Unknown"),  
                    reason=book.get("reason", ""),  
                    open_library_data=book_info["open_library_data"]
                )
                db.add(db_book)
                db.commit()
                db.refresh(db_book)
                books_data.append(db_book)
    
    response = {
        "id": book_search.id,
        "query": book_search.query,
        "created_at": book_search.created_at,
        "books": books_data
    }
    
    return response

@app.post("/api/more-books", response_model=BookSearchResponse)
async def load_more_books(request: MoreBooksRequest, db: Session = Depends(get_db)):
    """
    Load more book recommendations for an existing search
    """
    # 1. Get the original search query
    search = db.query(BookSearch).filter(BookSearch.id == request.search_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # 2. Get existing books to exclude from new recommendations
    existing_books = db.query(Book).filter(Book.search_id == request.search_id).all()
    exclude_titles = [book.title for book in existing_books]
    
    # 3. Get new recommendations excluding existing books
    books = await get_book_recommendations(
        query=search.query, 
        max_results=request.count, 
        exclude_titles=exclude_titles
    )
    
    if not isinstance(books, list):
        try:
            if isinstance(books, str):
                books = json.loads(books)
            if not isinstance(books, list):
                books = [books]
        except Exception as e:
            print(f"Error parsing book recommendations: {e}")
            books = []
    
    # 4. For each recommended book, fetch details from Open Library
    books_data = []
    for book in books:
        if not isinstance(book, dict) or "title" not in book:
            continue
            
        # Search Open Library for book info
        library_data = await search_book_by_title(book["title"])
        
        if library_data and "docs" in library_data and library_data["docs"]:
            book_info = extract_book_info(library_data)
            
            if book_info:
                db_book = Book(
                    search_id=search.id,
                    title=book_info["title"],
                    author=book_info["author"],
                    cover_url=book_info["cover_url"],
                    first_publish_year=book_info["first_publish_year"],
                    edition_count=book_info["edition_count"],
                    has_fulltext=book_info["has_fulltext"],
                    genre=book.get("genre", "Unknown"),
                    reason=book.get("reason", ""),
                    open_library_data=book_info["open_library_data"]
                )
                db.add(db_book)
                db.commit()
                db.refresh(db_book)
                books_data.append(db_book)
    
    # 5. Get all books for this search, including the newly added ones
    all_books = db.query(Book).filter(Book.search_id == request.search_id).all()
    
    response = {
        "id": search.id,
        "query": search.query,
        "created_at": search.created_at,
        "books": all_books
    }
    
    return response

@app.get("/api/history", response_model=list[BookSearchResponse])
async def get_search_history(db: Session = Depends(get_db)):
    """
    Get all previous book searches with their results
    """
    searches = db.query(BookSearch).all()
    
    results = []
    for search in searches:
        books = db.query(Book).filter(Book.search_id == search.id).all()
        
        search_response = {
            "id": search.id,
            "query": search.query,
            "created_at": search.created_at,
            "books": books
        }
        
        results.append(search_response)
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed port from 8000 to 8001