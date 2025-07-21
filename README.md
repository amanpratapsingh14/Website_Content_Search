# Website Content Search

## Objective
Develop a single-page application (SPA) that allows users to input a website URL and a search query. The application returns the top 10 most relevant HTML DOM content chunks (with tags) from the target website, based on the search query. The results are deduplicated and can be viewed as both text and raw HTML.

---

## Codebase Structure

```
website_content_search/
├── backend/
│   ├── main.py            # FastAPI app, API endpoint, and orchestration
│   ├── models.py          # Pydantic models for request/response
│   ├── html_utils.py      # HTML parsing and chunking logic
│   ├── weaviate_utils.py  # Weaviate and embedding logic
│   └── requirements.txt   # Backend dependencies
├── frontend/
│   ├── public/            # Static assets (favicon, index.html, etc.)
│   ├── src/
│   │   ├── App.js         # Main React component (UI, API calls, results)
│   │   ├── App.css        # App-specific styles
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # Frontend dependencies
│   └── README.md          # Frontend usage notes
├── weaviate/
│   └── docker-compose.yml # Weaviate vector database setup
└── README.md              # (This file)
```

---

## Codebase Flow

1. **Frontend (React):**
    - User enters a website URL and a search query in the form.
    - On submit, a POST request is sent to the backend `/search` endpoint.
    - Results are displayed as cards, showing a text summary and a toggle to view the raw HTML DOM chunk.

2. **Backend (FastAPI):**
    - Receives the URL and query.
    - Fetches the HTML content of the target website.
    - Parses and chunks the HTML into block-level elements (e.g., `div`, `section`, etc.), further splitting large blocks by token count.
    - Deduplicates chunks by exact text match.
    - If Weaviate is available:
        - Chunks are embedded and indexed in Weaviate.
        - Semantic search is performed using the query embedding.
        - Top results are deduplicated and returned.
    - If Weaviate is not available:
        - Fallback to keyword-based search and ranking.
        - Top results are deduplicated and returned.

---

## Implementation Details

### Backend
- **Framework:** FastAPI (Python)
- **HTML Parsing:** BeautifulSoup
- **Chunking:** Block-level tags, max 500 tokens per chunk
- **Deduplication:** Strict (case-insensitive, whitespace-normalized text match)
- **Semantic Search:** SentenceTransformers (MiniLM-L6-v2) + Weaviate (if available)
- **Fallback Search:** Keyword count ranking
- **API:** `/search` (POST)

### Frontend
- **Framework:** React
- **UI:** Modern, clean, responsive form and results cards
- **Features:**
    - Input for URL and query
    - Results with text and HTML toggle
    - Loading and error handling

### Vector Database
- **Weaviate:**
    - Dockerized, local instance
    - Stores chunk embeddings and metadata
    - Used for semantic search and ranking

---

## Techniques Used
- **HTML DOM chunking** for context-preserving search
- **Token-based splitting** for large blocks
- **Semantic embedding** for meaning-based search
- **Keyword fallback** for robustness
- **Strict deduplication** to avoid repeated content
- **Modern React UI** for usability

---

## Tools Used
- **Backend:** FastAPI, BeautifulSoup, SentenceTransformers, Weaviate, Requests
- **Frontend:** React, JavaScript, CSS
- **Vector DB:** Weaviate (Docker)

---

## Solution Summary
This project enables precise, context-aware search over any website's HTML content. By combining block-level HTML parsing, semantic embeddings, and a modern UI, users can quickly find the most relevant DOM sections for their queries. The solution is robust to repeated content and works with or without a vector database backend.

---

## Setup & Usage

### Prerequisites
- Python 3.8+
- Node.js & npm
- Docker (for Weaviate)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Weaviate (optional, for semantic search)
```bash
cd weaviate
sudo docker-compose up
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## License
MIT 

---

## Slide Deck

You can view the project presentation slide deck here:
[Google Slides: Website Content Search Presentation](https://docs.google.com/presentation/d/1zhYHtqTI4tTAJc8IK_jeijgU3tfa7WXUFqtD2t6gvIQ/edit?usp=sharing)

---

## Demo Screenshot

---