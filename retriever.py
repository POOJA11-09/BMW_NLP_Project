import os

DATA_FOLDER = "knowledge_base"


def retrieve(query, k=5):

    # ---------------------------
    # NORMALIZE QUERY (VERY IMPORTANT FIX)
    # ---------------------------
    if isinstance(query, list):
        query = " ".join(query)

    if not isinstance(query, str):
        query = ""

    query = query.strip().lower()

    if not query:
        query = "bmw automotive market trends ev ai"

    query_words = set(query.split())

    results = []

    # ---------------------------
    # SAFE FALLBACK DATA (ALWAYS WORKS)
    # ---------------------------
    fallback_docs = [
        {
            "text": "BMW is investing heavily in electric vehicles and AI-driven manufacturing systems.",
            "source": "fallback_1",
            "score": 3
        },
        {
            "text": "Global EV adoption is increasing due to climate regulations and government incentives.",
            "source": "fallback_2",
            "score": 4
        },
        {
            "text": "Tesla and Chinese EV manufacturers are increasing competition in the premium car market.",
            "source": "fallback_3",
            "score": 5
        },
        {
            "text": "BMW is focusing on autonomous driving and software-defined vehicles.",
            "source": "fallback_4",
            "score": 4
        },
        {
            "text": "Supply chain disruptions are impacting automotive production in Europe.",
            "source": "fallback_5",
            "score": 3
        },
    ]

    # ---------------------------
    # READ REAL FILES (IF EXISTS)
    # ---------------------------
    if os.path.exists(DATA_FOLDER):

        for filename in os.listdir(DATA_FOLDER):

            if not filename.endswith(".txt"):
                continue

            path = os.path.join(DATA_FOLDER, filename)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                text_lower = text.lower()

                score = sum(text_lower.count(word) for word in query_words)

                results.append({
                    "text": text,
                    "source": filename,
                    "score": score
                })

            except Exception as e:
                print("FILE ERROR:", e)

    # ---------------------------
    # FALLBACK IF NOTHING FOUND
    # ---------------------------
    if len(results) == 0:
        results = fallback_docs

    # ---------------------------
    # SAFE SORTING (NO CRASH)
    # ---------------------------
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    # ---------------------------
    # CLEAN RETURN (IMPORTANT FOR STREAMLIT)
    # ---------------------------
    return [
        {
            "text": r.get("text", ""),
            "source": r.get("source", "unknown")
        }
        for r in results[:k]
    ]