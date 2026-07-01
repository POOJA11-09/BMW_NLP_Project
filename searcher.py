import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# FIXED PATHS (ABSOLUTE SAFE)
# -----------------------------

BASE_DIR = os.path.dirname(__file__)

INDEX_FILE = os.path.join(BASE_DIR, "faiss.index")
MAPPING_FILE = os.path.join(BASE_DIR, "id_map.json")

model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=5):

    # load FAISS index safely
    index = faiss.read_index(INDEX_FILE)

    # load mapping safely
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # encode query
    query_vec = model.encode([query]).astype("float32")

    # search
    D, I = index.search(query_vec, top_k)

    results = []

    for idx in I[0]:
        if str(idx) in mapping:
            results.append(mapping[str(idx)])

    return results