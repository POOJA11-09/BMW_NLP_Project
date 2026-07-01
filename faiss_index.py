import numpy as np
import faiss
import json
import os

from sentence_transformers import SentenceTransformer
from preprocess import preprocess_documents, generate_embeddings


# -----------------------------
# CONFIG
# -----------------------------
INDEX_FILE = "faiss.index"
MAPPING_FILE = "chunk_mapping.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# BUILD FAISS INDEX
# -----------------------------
def build_faiss_index():

    print("\n🚀 Starting FAISS indexing...")

    # STEP 1: Get processed chunks
    docs = preprocess_documents()

    print(f"Total chunks: {len(docs)}")

    # STEP 2: Generate embeddings (you already have function)
    embeddings = generate_embeddings(docs)

    embeddings = np.array(embeddings).astype("float32")

    # STEP 3: Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    # STEP 4: Save FAISS index
    faiss.write_index(index, INDEX_FILE)

    # STEP 5: Create mapping (IMPORTANT FOR AGENT)
    mapping = {}

    for i, doc in enumerate(docs):
        mapping[i] = {
            "text": doc["text"],
            "title": doc["meta"].get("title"),
            "url": doc["meta"].get("url"),
            "source": doc["meta"].get("source"),
            "published_date": doc["meta"].get("published_date"),
            "chunk_id": doc["meta"].get("chunk_id")
        }

    # STEP 6: Save mapping JSON
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)

    print("\n✅ FAISS INDEX CREATED SUCCESSFULLY")
    print("📦 Index file:", INDEX_FILE)
    print("📦 Mapping file:", MAPPING_FILE)
    print("📊 Total vectors indexed:", len(docs))


# -----------------------------
# SEARCH FUNCTION (FOR AGENT)
# -----------------------------
def search(query, top_k=5):

    index = faiss.read_index(INDEX_FILE)

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    query_vec = model.encode([query]).astype("float32")

    distances, indices = index.search(query_vec, top_k)

    results = []

    for idx in indices[0]:
        if str(idx) in mapping:
            results.append(mapping[str(idx)])

    return results


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    build_faiss_index()

    print("\n🔎 TEST SEARCH:")
    results = search("BMW electric vehicle future")

    for r in results:
        print("\n---")
        print(r["title"])
        print(r["url"])