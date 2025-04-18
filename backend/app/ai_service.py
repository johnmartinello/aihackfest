import os
import google.generativeai as genai
import google.generativeai.types as genai_types # Import types
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)


generation_config = genai_types.GenerationConfig(
    response_mime_type="application/json",
    temperature=1.2,
)

async def get_book_recommendations(query: str, max_results: int = 12, exclude_titles: list = None) -> list:
    """
    Get book recommendations from Google Generative AI based on query
    
    Args:
        query: Search query for book recommendations
        max_results: Maximum number of books to return
        exclude_titles: List of book titles to exclude from recommendations
    """
    
    model = genai.GenerativeModel(
        'gemini-2.0-flash', 
        generation_config=generation_config,
    )
    
    exclusion_text = ""
    if exclude_titles and len(exclude_titles) > 0:
        exclusion_text = f"""
        IMPORTANT EXCLUSION: Do NOT include any of the following books in your recommendations:
        {', '.join(exclude_titles)}
        """

    prompt = f"""
    You are an expert book recommendation/finder system. Based on the query, suggest books.
    focus mostly on recommending books that are similar plot-wise, theme-wise, or stylistically.
    For each recommendation, include: Title of the book, genre, and a short paragraph explaining why it was chosen, detailing aspects of its plot, themes, and mood that match the query.
    Take into account: if the query is a book title, suggest similar books in the same genre or style. If the query is a general description, suggest books that fit that description. If the user is looking for a specific genre, suggest only books in that genre.

    {exclusion_text}

    IMPORTANT:
    Respond ONLY with a valid JSON array containing exactly {max_results} recommendations (or fewer if not enough relevant books are found). Order it by relevance.
    If the user is trying to find a specific book, and If you know the book being describred, you should add to the response.
    If the user is trying to find books that are similar to specific author(s), you should not recommend books by the same author(s) (unless told otherwise).
    DO NOT RECOMMEND ANYTHING THAT IS NOT A BOOK.
    The JSON array should follow this structure for each element:
    {{
      "title": "Book Title",
      "genre": "Genre of the book",
      "reason": "A detailed explanation connecting the book's stylistic elements with the provided description."
    }}

    Query: {query}
    """

    try:
        response = await model.generate_content_async(prompt) # Use async version if needed

        text_response = response.text

        books = json.loads(text_response)
        return books

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from AI response: {e}")
        print(f"--- Failed Response Text ---\n{text_response}\n--------------------------")
        return [
            {"title": "Fallback: The Great Gatsby", "genre": "Classic", "reason": "A classic novel."},
            {"title": "Fallback: To Kill a Mockingbird", "genre": "Classic", "reason": "A powerful story."}
        ]
    except Exception as e:
        # Catch other potential errors (API errors, etc.)
        print(f"Error in AI recommendation: {e}")
        if 'response' in locals() and response:
             print(f"--- Full Response Object on Error ---\n{response}\n---------------------------------")
        return [
            {"title": "Fallback: The Great Gatsby", "genre": "Classic", "reason": "A classic novel."},
            {"title": "Fallback: To Kill a Mockingbird", "genre": "Classic", "reason": "A powerful story."}
        ]

async def generate_user_profile(queries: list) -> str:
    """
    Generate a funny user profile based on their search history
    
    Args:
        queries: List of search queries the user has made
    
    Returns:
        A streaming response for the generated profile
    """
    # For streaming, we'll use a different configuration
    stream_generation_config = genai_types.GenerationConfig(
        temperature=1.2,
    )
    
    model = genai.GenerativeModel(
        'gemini-2.0-flash',
        generation_config=stream_generation_config,
    )
    
    # Join the queries into a single string for context
    search_history = "\n- ".join(queries)
    
    prompt = f"""
    Based on this person's book search history, create a funny, light-hearted profile of them. 
    Be creative and humorous but remain tasteful. Imagine what kind of person they might be based on their literary interests.
    Include things like:
    - What their personality might be like
    - What they might do for fun
    - A funny quirk they might have
    - Their ideal weekend
    - Be playful and witty!
    
    Here are their search queries:
    - {search_history}
    
    Create a profile that's around 150-200 words, with a touch of humor.
    """
    
    try:
        # Return the streaming response directly
        return await model.generate_content_async(prompt, stream=True)
    except Exception as e:
        # For errors, we'll return a non-streaming response with an error message
        print(f"Error generating user profile: {e}")
        return "Sorry, I couldn't create your profile at the moment. Maybe your book choices were too complex for me to analyze!"

