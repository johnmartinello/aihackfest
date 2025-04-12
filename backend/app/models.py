from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Define the SQLite database
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookSearch(Base):
    __tablename__ = "book_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    llm_response = Column(Text)

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    cover_url = Column(String(255))
    first_publish_year = Column(Integer)
    edition_count = Column(Integer)
    has_fulltext = Column(Integer)
    genre = Column(String(255))  
    reason = Column(Text)  
    open_library_data = Column(Text)
    
def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()