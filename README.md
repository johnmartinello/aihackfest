# Book Recommendation System - AI Hackfest Project

## Overview

This project is a Book Recommendation System built for the **AI Hackfest (2025)** event. It demonstrates the use of Generative AI to provide personalized book suggestions based on user queries.

**This application was developed in less than 12 hours.**

## Functionality

* **AI-Powered Recommendations:** Enter a query (e.g., a book title, genre, plot description, or desired mood) and the system uses Google's Generative AI (Gemini 2.0 Flash) to find relevant book recommendations.
* **Detailed Book Information:** For each recommendation, the system fetches additional details like author, cover image, publication year from the Open Library API.
* **"Recommend More" Feature:** If the initial recommendations aren't enough, click the "Recommend More Books" button to get additional suggestions based on your original query.
* **User Search History:** Each user can view their search history, stored locally in their browser. Users can quickly access past searches and their results without needing to search again.
* **Simple Interface:** A clean web interface built with Vue.js allows users to easily input queries and view results.

## Technology Stack

* **Backend:** FastAPI (Python), SQLAlchemy, Google Generative AI API
* **Frontend:** Vue.js, Axios
* **Database:** SQLite
* **External API:** Open Library API
* **Storage:** Browser localStorage for user-specific search history

## Development Context

* **Event:** AI Hackfest (2025)
* **Developer:** João Lucas Martinello
* **Timeframe:** 1 Day

## How it Works

1. The user enters a search query in the frontend.
2. The frontend sends the query to the FastAPI backend.
3. The backend uses the Google Generative AI API to get a list of book recommendations (title, genre, reason) based on the query, excluding previously recommended titles if applicable.
4. For each recommended title, the backend queries the Open Library API to fetch detailed book information (author, cover, etc.).
5. The backend saves the search query and the combined book data (AI recommendation + Open Library details) to the SQLite database.
6. The results are sent back to the frontend and displayed to the user.
7. The "Recommend More Books" button triggers a request to a separate backend endpoint, providing the original search ID to fetch more unique recommendations.
8. Search history is saved to the user's browser localStorage, allowing them to revisit past searches.

## Setup & Running

### 1. Clone the repository 

```bash
git clone https://github.com/yourusername/book-recommendation-system.git
cd book-recommendation-system
```

### 2. Backend Setup

```bash
cd backend
```

#### Create a virtual environment (optional but recommended)
```bash
python -m venv env
```

#### Activate virtual environment (Windows)
```bash
.\env\Scripts\activate
```

#### Install backend dependencies
```bash
pip install -r requirements.txt
```

#### Ensure you have a .env file with your GOOGLE_API_KEY
Create a `.env` file in the backend directory with:
```
GOOGLE_API_KEY=your_api_key_here
```

#### Run database migrations (if needed, e.g., first time setup)
```bash
python migrate.py
```

#### Start the backend server
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup (in a separate terminal)

```bash
cd ../frontend
```

#### Install frontend dependencies
```bash
npm install
```

#### Start the frontend development server
```bash
npm run serve
```

### 4. Access the application

Open your browser and navigate to [http://localhost:8080](http://localhost:8080) (or the port specified by Vue CLI)
