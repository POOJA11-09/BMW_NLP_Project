import os
import json
import re
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
DATA_DIR = "data/raw"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    """
    Remove HTML, extra spaces and newlines.
    """

    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# CHUNK DOCUMENT
# -----------------------------
def chunk_text(text, chunk_size=250):
    """
    Split long text into chunks of approximately
    250 words.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])

        if len(chunk.strip()) > 20:
            chunks.append(chunk)

    return chunks


# -----------------------------
# LOAD + CLEAN + DEDUP + CHUNK
# -----------------------------
def preprocess_documents():

    processed_docs = []

    seen_urls = set()

    seen_texts = set()

    total_chunks = 0

    for root, _, files in os.walk(DATA_DIR):

        for file in files:

            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:

                data = json.load(f)

            title = data.get("title", "")
            content = data.get("content", "")
            url = data.get("url", "")

            # -----------------------
            # REMOVE DUPLICATE URL
            # -----------------------
            if url in seen_urls:
                continue

            seen_urls.add(url)

            # -----------------------
            # CLEAN
            # -----------------------
            content = clean_text(content)

            # Remove duplicate content
            if content in seen_texts:
                continue

            seen_texts.add(content)

            # -----------------------
            # COMBINE TITLE + CONTENT
            # -----------------------
            full_text = title + ". " + content

            # -----------------------
            # CHUNKING
            # -----------------------
            chunks = chunk_text(full_text)

            for chunk_id, chunk in enumerate(chunks):

                processed_docs.append({

                    "text": chunk,

                    "meta": {

                        "id": data.get("id"),

                        "title": title,

                        "source": data.get("source"),

                        "url": url,

                        "published_date": data.get("published_date"),

                        "chunk_id": chunk_id

                    }

                })

                total_chunks += 1

    print("=" * 50)
    print("PREPROCESSING COMPLETE")
    print("=" * 50)
    print("Unique Documents :", len(seen_urls))
    print("Total Chunks      :", total_chunks)
    print("=" * 50)

    return processed_docs


# -----------------------------
# GENERATE EMBEDDINGS
# -----------------------------
def generate_embeddings(processed_docs):

    texts = [doc["text"] for doc in processed_docs]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":

    docs = preprocess_documents()

    embeddings = generate_embeddings(docs)

    print("\nEmbeddings shape:", embeddings.shape)