# ingest.py
"""
Run this script to index the files inside ./data directory.
It reads .txt and .md files and stores them as documents.
"""
import os
import json
from retriever import Retriever

DATA_DIR = "./data"
CHUNK_SIZE = 800   # approx characters per chunk
OVERLAP = 100

def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def load_files(data_dir=DATA_DIR):
    docs = []
    doc_id = 0
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if not os.path.isfile(path):
            continue
        if not (fname.lower().endswith(".txt") or fname.lower().endswith(".md")):
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": doc_id,
                "text": chunk,
                "meta": {"source": fname, "chunk": i}
            })
            doc_id += 1
    return docs

if __name__ == "__main__":
    retriever = Retriever()
    docs = load_files()
    if not docs:
        print("No docs found in ./data. Add some .txt or .md files then run this script.")
    else:
        print(f"Indexing {len(docs)} chunks ...")
        retriever.build_index(docs)
        print("Index built and saved.")
