"""RSS Feed Parser for TechCrunch"""
import feedparser
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
import time
import re
import requests


@dataclass
class Article:
    title: str
    link: str
    description: str
    author: str
    published_date: str
    categories: List[str]
    image_url: str = ""
    summary: str = ""

    def to_dict(self):
        return asdict(self)


def extract_image_from_content(content: str) -> str:
    """Extract image URL from HTML content"""
    if not content:
        return ""
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    return match.group(1) if match else ""


def fetch_og_image(url: str) -> str:
    """Fetch OpenGraph image from article page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        text = response.text

        # Try og:image
        og_patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        ]
        for pattern in og_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        # Try Twitter image
        twitter_match = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', text)
        if twitter_match:
            return twitter_match.group(1)

        return ""
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""


class RSSParser:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_feed(self) -> dict:
        """Fetch and parse the RSS feed"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                feed = feedparser.parse(self.feed_url)
                if feed.bozo:
                    raise ValueError(f"Failed to parse feed: {feed.bozo_exception}")
                return feed
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise e

    def parse_articles(self, limit: int = 20) -> List[Article]:
        """Parse articles from the feed"""
        feed = self.fetch_feed()
        articles = []

        for entry in feed.entries[:limit]:
            categories = [tag.term for tag in entry.get('tags', [])]

            description = entry.get('description', '')
            summary = entry.get('summary', '')

            image_url = ""
            if hasattr(entry, 'links'):
                for link in entry.links:
                    if hasattr(link, 'type') and link.type.startswith('image/'):
                        image_url = link.href
                        break

            published_date = entry.get('published', '')
            if hasattr(entry, 'published_parsed'):
                published_date = datetime(*entry.published_parsed[:6]).isoformat()

            article = Article(
                title=entry.get('title', 'No Title'),
                link=entry.get('link', ''),
                description=description[:500] if description else '',
                author=entry.get('author', 'Unknown'),
                published_date=published_date,
                categories=categories,
                image_url=image_url,
                summary=summary[:300] if summary else description[:300]
            )
            articles.append(article)

        # Fetch images from article pages
        print(f"[INFO] Fetching images for {len(articles)} articles...")
        for i, article in enumerate(articles):
            if not article.image_url:
                article.image_url = fetch_og_image(article.link)
                print(f"[{i+1}/{len(articles)}] {article.title[:40]}... | {'FOUND' if article.image_url else 'NO IMAGE'}")

        return articles

    def get_feed_info(self) -> dict:
        """Get basic feed information"""
        feed = self.fetch_feed()
        return {
            'title': feed.feed.get('title', 'Unknown'),
            'description': feed.feed.get('description', ''),
            'link': feed.feed.get('link', ''),
            'last_build_date': feed.feed.get('lastBuildDate', ''),
        }
