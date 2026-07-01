from agent.planner import call_llm


def analyze_sentiment(docs):

    text = " ".join(d.get("text", "").lower() for d in docs)

    positive_words = ["growth", "opportunity", "innovation", "strong", "increase"]
    negative_words = ["risk", "loss", "decline", "pressure", "competition"]

    pos = sum(text.count(w) for w in positive_words)
    neg = sum(text.count(w) for w in negative_words)
    neu = max(0, 5 - (pos + neg))

    return {
        "Positive": pos,
        "Negative": neg,
        "Neutral": neu
    }