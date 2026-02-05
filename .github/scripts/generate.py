"""Generate TechCrunch digest and save to GitHub Gist"""

import feedparser
import requests
import json
import os
import re
from datetime import datetime
from openrouter_insights import OpenRouterInsightsGenerator

GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_article_image(entry):
    """Extract featured image from article entry"""
    if hasattr(entry, "media_content"):
        for media in entry.media_content:
            if "url" in media:
                return media["url"]
    if hasattr(entry, "links"):
        for link in entry.links:
            if link.type.startswith("image/"):
                return link.href
    if hasattr(entry, "summary"):
        img_match = re.search(r'<img[^>]+src="([^"]+)"', entry.summary)
        if img_match:
            return img_match.group(1)
    return None


def generate():
    print(f"[INFO] Starting digest generation at {datetime.now().isoformat()}")

    print("[INFO] Fetching RSS feed...")
    feed = feedparser.parse("https://techcrunch.com/feed/")
    feed_info = {
        "title": feed.feed.get("title", "TechCrunch"),
        "subtitle": feed.feed.get("subtitle", ""),
        "link": feed.feed.get("link", "https://techcrunch.com"),
    }
    print(f"[INFO] Found {len(feed.entries)} articles")

    articles = []
    for entry in feed.entries[:15]:
        article = {
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "author": entry.get("author", ""),
            "categories": [tag.get("term", "") for tag in entry.get("tags", [])],
            "image": get_article_image(entry),
        }
        articles.append(article)
        print(f"[INFO] Parsed: {article['title'][:50]}...")

    insights = []
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    if openrouter_key:
        print("[INFO] Generating AI insights...")
        generator = OpenRouterInsightsGenerator(openrouter_key)
        for article in articles:
            insight = generator.generate_insight(article)
            insights.append(
                {
                    "title": insight.title,
                    "key_takeaways": insight.key_takeaways,
                    "impact_analysis": insight.impact_analysis,
                    "related_tech": insight.related_tech,
                    "sentiment": insight.sentiment,
                    "read_time_estimate": insight.read_time_estimate,
                }
            )
            print(f"[INFO] Generated insight for: {article['title'][:30]}...")
    else:
        print("[WARN] No OPENROUTER_API_KEY, using fallback insights")
        for article in articles:
            categories = article.get("categories", [])
            summary = article.get("summary", "")
            insights.append(
                {
                    "title": article["title"],
                    "key_takeaways": [
                        f"Category: {categories[0] if categories else 'Tech'}",
                        summary.split(".")[0] + "." if summary else "See full article",
                        "Click to read more",
                    ],
                    "impact_analysis": "This article covers recent tech industry news",
                    "related_tech": categories[:3],
                    "sentiment": "neutral",
                    "read_time_estimate": "medium",
                }
            )

    digest = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now().isoformat(),
        "articles": articles,
        "insights": insights,
        "feed_info": feed_info,
    }

    if GIST_ID and GITHUB_TOKEN:
        print(f"[INFO] Saving to Gist {GIST_ID}...")
        gist_url = f"https://api.github.com/gists/{GIST_ID}"
        response = requests.patch(
            gist_url,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={
                "files": {"techcrunch.json": {"content": json.dumps(digest, indent=2)}}
            },
        )
        if response.status_code in (200, 201):
            print("[INFO] Successfully saved digest to Gist")
        else:
            print(f"[ERROR] Failed to save Gist: {response.status_code}")
            print(response.text)
    else:
        print("[WARN] GIST_ID or GITHUB_TOKEN not set, saving locally")
        os.makedirs("data", exist_ok=True)
        with open("data/digest.json", "w") as f:
            json.dump(digest, f, indent=2)

    print(f"[INFO] Digest generation complete at {datetime.now().isoformat()}")
    return digest


if __name__ == "__main__":
    generate()
