import requests
from bs4 import BeautifulSoup
from utils.save_json import save_json
import time

BASE_URL = "https://www.press.bmwgroup.com/global"


# -----------------------------
# EXTRACT ARTICLE
# -----------------------------
def extract_article(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return "", None

        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text(strip=True) for p in paragraphs])

        date_tag = soup.find("time")
        published_date = None

        if date_tag and date_tag.has_attr("datetime"):
            published_date = date_tag["datetime"].split("T")[0]

        return content, published_date

    except Exception as e:
        print(f"Failed article: {url} | {e}")
        return "", None


# -----------------------------
# MAIN SCRAPER
# -----------------------------
def scrape_bmw_press(limit=50):

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(BASE_URL, headers=headers)

    print("Homepage status:", res.status_code)

    soup = BeautifulSoup(res.text, "html.parser")

    # -----------------------------
    # FIX: FILTER ONLY ARTICLE LINKS
    # -----------------------------
    articles = soup.find_all("a", href=True)

    count = 0
    seen = set()

    for a in articles:

        if count >= limit:
            break

        title = a.get_text(strip=True)
        link = a["href"]

        # -----------------------------
        # FILTER INVALID LINKS
        # -----------------------------
        if not title or len(title) < 10:
            continue

        if "press.bmwgroup.com" not in link:
            if link.startswith("/"):
                link = "https://www.press.bmwgroup.com" + link
            else:
                continue

        # remove duplicates
        if link in seen:
            continue

        seen.add(link)

        print(f"Scraping: {title}")

        content, published_date = extract_article(link)

        print("Content length:", len(content))

        # skip empty pages
        if len(content) < 50:
            continue

        data = {
            "id": f"BMW_PRESS_{count}",
            "title": title,
            "content": content,
            "url": link,
            "published_date": published_date,
            "source": "BMW Press"
        }

        save_json(
            "data/raw/bmw_press",
            f"BMW_PRESS_{count}.json",
            data
        )

        count += 1
        time.sleep(1)

    print(f"BMW Press done: {count} articles collected")
    return count