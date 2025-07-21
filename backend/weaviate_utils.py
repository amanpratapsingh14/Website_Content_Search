import os
from sentence_transformers import SentenceTransformer

try:
    import weaviate
except ImportError:
    weaviate = None

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
weaviate_client = None
WEAVIATE_AVAILABLE = False
if weaviate is not None:
    try:
        weaviate_client = weaviate.Client(WEAVIATE_URL)
        WEAVIATE_AVAILABLE = weaviate_client.is_ready()
    except Exception:
        weaviate_client = None
        WEAVIATE_AVAILABLE = False

def index_chunks_in_weaviate(chunks, url):
    if not weaviate_client:
        return
    class_name = "HtmlChunk"
    if not weaviate_client.schema.exists(class_name):
        schema = {
            "class": class_name,
            "vectorizer": "none",
            "properties": [
                {"name": "id", "dataType": ["text"]},
                {"name": "text", "dataType": ["text"]},
                {"name": "html", "dataType": ["text"]},
                {"name": "url", "dataType": ["text"]},
            ],
        }
        weaviate_client.schema.create_class(schema)
    for idx, chunk in enumerate(chunks):
        embedding = EMBED_MODEL.encode(chunk["text"]).tolist()
        obj = {
            "id": chunk["id"],
            "text": chunk["text"],
            "html": chunk["html"],
            "url": url,
        }
        weaviate_client.data_object.create(
            obj,
            class_name=class_name,
            vector=embedding
        )

def search_chunks_in_weaviate(query, url, top_k=10):
    from .models import SearchResult
    if not weaviate_client:
        return []
    class_name = "HtmlChunk"
    embedding = EMBED_MODEL.encode(query).tolist()
    result = weaviate_client.query.get(class_name, ["id", "text", "html", "url"]) \
        .with_near_vector({"vector": embedding}) \
        .with_where({"path": ["url"], "operator": "Equal", "valueText": url}) \
        .with_limit(top_k * 3) \
        .with_additional(["certainty"]) \
        .do()
    matches = result["data"]["Get"].get(class_name, [])
    seen_ids = set()
    unique_results = []
    for hit in matches:
        chunk_id = hit["id"]
        if chunk_id not in seen_ids:
            unique_results.append(SearchResult(
                id=chunk_id,
                chunk=hit["text"],
                html=hit["html"],
                path=url,
                score=hit["_additional"]["certainty"]
            ))
            seen_ids.add(chunk_id)
        if len(unique_results) == top_k:
            break
    return unique_results 