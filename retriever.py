# retriever.py
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index.index")
DOCS_JSON = os.getenv("DOCS_JSON", "./docs_meta.json")

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.docs = []  # list of dicts: {"id": int, "text": "...", "meta": {...}}
        if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_JSON):
            self._load_index()
        else:
            self.index = None  # index not built yet

    def _load_index(self):
        """Load FAISS index and document metadata"""
        with open(DOCS_JSON, "r", encoding="utf-8") as f:
            self.docs = json.load(f)
        self.index = faiss.read_index(INDEX_PATH)
        print(f"✅ FAISS index loaded with {len(self.docs)} documents.")

    def build_index(self, docs):
        """Build FAISS index from docs list"""
        self.docs = docs
        print(f"🔧 Building FAISS index with {len(docs)} documents...")
        embeddings = self.model.encode([d["text"] for d in docs], show_progress_bar=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings).astype("float32"))
        faiss.write_index(index, INDEX_PATH)
        with open(DOCS_JSON, "w", encoding="utf-8") as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)
        self.index = index
        print("✅ Index built and saved successfully.")

    def retrieve(self, query, top_k=4):
        """Retrieve top_k similar chunks for a query"""
        if self.index is None:
            print("⚠️ No FAISS index found. Please run ingest.py first.")
            return []
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb).astype("float32"), top_k)
        results = []
        for idx in I[0]:
            if idx < 0 or idx >= len(self.docs):
                continue
            results.append(self.docs[idx])
        return results
