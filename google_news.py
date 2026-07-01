import feedparser
from utils.save_json import save_json
from datetime import datetime
from urllib.parse import quote


# -----------------------------
# SAFE DATE PARSER
# -----------------------------
def clean_date(date_str):

    if not date_str:
        return ""

    try:
        return datetime.strptime(
            date_str,
            "%a, %d %b %Y %H:%M:%S %Z"
        ).date().isoformat()

    except:
        return ""


# -----------------------------
# SCRAPER
# -----------------------------
def scrape_google_news(query="BMW", limit=30):

    encoded_query = quote(query)

    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)

    count = 0

    for entry in feed.entries:

        if count >= limit:
            break

        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "")

        published_date = clean_date(published)

        summary = entry.get("summary", "")

        # -----------------------------
        # SMART CONTENT BUILDING
        # -----------------------------
        if summary:
            content = f"{title}. {summary}"
        else:
            content = title

        data = {
            "id": f"NEWS_{count}",
            "title": title,
            "source": "Google News",
            "published_date": published_date,
            "url": link,
            "content": content
        }

        save_json(
            "data/raw/google_news",
            f"NEWS_{count}.json",
            data
        )

        count += 1

    print(f"Google News done: {count} articles collected")
    return count