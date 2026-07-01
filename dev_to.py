import feedparser
from utils.save_json import save_json
import requests
from bs4 import BeautifulSoup
import os


TAGS = [
    "bmw",
    "electricvehicles",
    "automotive",
    "tesla",
    "ev"
]


def extract_full_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return ""

        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")
        return " ".join(p.get_text(strip=True) for p in paragraphs)

    except Exception as e:
        print("Article error:", e)
        return ""


def scrape_devto(limit=25):

    print("\n🔎 DEV.TO SCRAPER STARTED\n")

    os.makedirs("data/raw/devto", exist_ok=True)

    count = 0

    for tag in TAGS:

        url = f"https://dev.to/feed/tag/{tag}"
        feed = feedparser.parse(url)

        print(f"\nTag: {tag}")
        print("Feed status:", feed.bozo)
        print("Entries found:", len(feed.entries))

        # 🔴 IMPORTANT DEBUG CHECK
        if len(feed.entries) == 0:
            print(f"❌ No data for tag: {tag}")
            continue

        for entry in feed.entries:

            if count >= limit:
                break

            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            print("Scraping:", title[:60])

            content = extract_full_text(link)

            if not content:
                content = title

            data = {
                "id": f"DEVTO_{count}",
                "title": title,
                "url": link,
                "published_date": published,
                "source": "Dev.to",
                "content": content
            }

            save_json(
                "data/raw/devto",
                f"DEVTO_{count}.json",
                data
            )

            count += 1

    print("\n====================")
    print("DEV.TO DONE:", count)
    print("====================")

    return count
if __name__ == "__main__":
    scrape_devto()