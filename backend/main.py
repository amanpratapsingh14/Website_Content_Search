from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
import hashlib

from models import SearchRequest, SearchResult
from html_utils import chunk_html_blocks
from weaviate_utils import (
    index_chunks_in_weaviate,
    search_chunks_in_weaviate,
    WEAVIATE_AVAILABLE,
    weaviate_client
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def jaccard_similarity(a, b):
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)

def is_exact_duplicate(a, b):
    return a.strip().lower() == b.strip().lower()

@app.post("/search", response_model=List[SearchResult])
def search_website_content(request: SearchRequest):
    # 1. Fetch HTML
    try:
        resp = requests.get(request.url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")
    # 2. Chunk HTML into blocks
    chunks = chunk_html_blocks(resp.text, max_tokens=500)
    if not chunks:
        raise HTTPException(status_code=404, detail="No content found on page.")
    # Deduplicate chunks by text_id before indexing/searching
    unique_chunks = []
    seen_text_ids = set()
    for chunk in chunks:
        if chunk["text_id"] not in seen_text_ids:
            unique_chunks.append(chunk)
            seen_text_ids.add(chunk["text_id"])
    # 3. If Weaviate available, index and search
    if WEAVIATE_AVAILABLE and weaviate_client:
        index_chunks_in_weaviate(unique_chunks, request.url)
        results = search_chunks_in_weaviate(request.query, request.url, top_k=20)
        # Strict deduplication: only skip if text is exactly the same
        deduped_results = []
        for r in results:
            if not any(is_exact_duplicate(r.chunk, c.chunk) for c in deduped_results):
                deduped_results.append(r)
            if len(deduped_results) == 10:
                break
        return deduped_results
    # 4. If Weaviate not available, do a simple keyword search as fallback
    scored = []
    q = request.query.lower()
    for chunk in unique_chunks:
        score = chunk["text"].lower().count(q)
        if score > 0:
            scored.append((chunk, score))
    scored.sort(key=lambda x: -x[1])
    # Strict deduplication for fallback
    deduped_results = []
    for c, s in scored:
        if not any(is_exact_duplicate(c["text"], d.chunk) for d in deduped_results):
            deduped_results.append(SearchResult(id=c["id"], chunk=c["text"], html=c["html"], path=request.url, score=s/10.0))
        if len(deduped_results) == 10:
            break
    return deduped_results 