import httpx
import json
import urllib.parse

async def search_book_by_title(title: str) -> dict:
    """
    Search for a book on Open Library by title
    """
    if not isinstance(title, str):
        title = title.decode("utf-8") if isinstance(title, bytes) else str(title)

    encoded_title = urllib.parse.quote(title)
    url = f"https://openlibrary.org/search.json?q={encoded_title}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  
            return response.json()
        except httpx.RequestError as e:
            print(f"Error searching for book '{title}': {e}")
            return {"error": str(e), "docs": []}
        except json.JSONDecodeError:
            print(f"Invalid JSON response for book '{title}'")
            return {"error": "Invalid JSON response", "docs": []}

def extract_book_info(open_library_data: dict) -> dict:
    """
    Extract relevant book information from Open Library API response
    """
    if not open_library_data or "docs" not in open_library_data or not open_library_data["docs"]:
        return None
    
    book_data = open_library_data["docs"][0]
    
    cover_url = None
    if "cover_i" in book_data:
        cover_id = book_data["cover_i"]
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    
    author = None
    if "author_name" in book_data and book_data["author_name"]:
        author = book_data["author_name"][0]
    
    return {
        "title": book_data.get("title", "Unknown"),
        "author": author,
        "cover_url": cover_url,
        "first_publish_year": book_data.get("first_publish_year"),
        "edition_count": book_data.get("edition_count"),
        "has_fulltext": bool(book_data.get("has_fulltext", False)),
        "open_library_data": json.dumps(book_data)
    }