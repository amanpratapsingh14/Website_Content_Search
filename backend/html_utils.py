import re
import hashlib
from bs4 import BeautifulSoup

BLOCK_TAGS = ["div", "section", "article", "main", "aside", "nav", "header", "footer"]

def chunk_html_blocks(html, max_tokens=500):
    soup = BeautifulSoup(html, "html.parser")
    blocks = []
    for tag in soup.find_all(BLOCK_TAGS):
        raw_html = str(tag)
        text = tag.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        if text:
            chunk_id = hashlib.md5(raw_html.encode()).hexdigest()
            text_id = hashlib.md5(text.lower().strip().encode()).hexdigest()
            blocks.append({"id": chunk_id, "text_id": text_id, "html": raw_html, "text": text})
    if not blocks:
        body = soup.body or soup
        raw_html = str(body)
        text = body.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        chunk_id = hashlib.md5(raw_html.encode()).hexdigest()
        text_id = hashlib.md5(text.lower().strip().encode()).hexdigest()
        blocks = [{"id": chunk_id, "text_id": text_id, "html": raw_html, "text": text}]
    final_chunks = []
    for block in blocks:
        words = block["text"].split()
        if len(words) <= max_tokens:
            final_chunks.append(block)
        else:
            for i in range(0, len(words), max_tokens):
                chunk_text = " ".join(words[i:i+max_tokens])
                sub_html = block["html"]
                sub_id = hashlib.md5((sub_html + chunk_text).encode()).hexdigest()
                text_id = hashlib.md5(chunk_text.lower().strip().encode()).hexdigest()
                final_chunks.append({"id": sub_id, "text_id": text_id, "html": sub_html, "text": chunk_text})
    return final_chunks 