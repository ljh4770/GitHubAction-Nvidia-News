import os
import requests
from datetime import datetime

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
if not GITHUB_ACTIONS:
    from dotenv import load_dotenv
    load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"
README_PATH = "README.md"

params = {
    "q": "nvidia",            # 검색어 (오타 방지: nvidia)
    "language": "en",         # 필요 시 'ko' 등으로 변경
    "sortBy": "publishedAt",  # 최신순 정렬
    "pageSize": 10,           # 10개만 가져오기
    "apiKey": API_KEY,
}

def get_news():
    """Fetch 10 latest news articles from News API"""
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        results = []

        for art in articles:
            published = art["publishedAt"][:10]
            title = art["title"]
            url = art["url"]
            results.append((published, title, url))
        return results[:10]
    
    print(f"Error fetching news: {response.status_code} - {response.text}")
    return None

def update_readme():
    """Update README.md file"""
    
    # Update timestamp & Default contents
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Latest NVIDIA News (top 10)\n",
        f"_Last updated: **{now}**_\n\n",
    ]

    news_infos = get_news() # Fetch news articles
    if news_infos is None: # Failed to fetch
        lines.append("Failed to fetch news articles.\n")
    else: # Successfully fetched
        for news in news_infos:
            published, title, url = news
            lines.append(f"- [{title}]({url}) (Published: {published})\n")

    # Write to README.md
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    update_readme()