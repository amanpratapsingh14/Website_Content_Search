from pydantic import BaseModel

class SearchRequest(BaseModel):
    url: str
    query: str

class SearchResult(BaseModel):
    id: str  # unique identifier for the chunk
    chunk: str  # text summary
    html: str   
    path: str
    score: float 