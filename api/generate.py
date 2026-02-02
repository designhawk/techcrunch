import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import json
from datetime import datetime

def load_config():
    with open('../config.yaml', 'r') as f:
        return yaml.safe_load(f)

def generate_digest():
    from rss_parser import RSSParser
    from openrouter_insights import OpenRouterInsightsGenerator
    from storage import StorageManager, DailyDigest

    config = load_config()
    rss_url = config.get('rss_url', 'https://techcrunch.com/feed/')
    openrouter_key = config.get('openrouter_api_key', '')

    parser = RSSParser(rss_url)
    articles = parser.parse_articles(limit=15)
    feed_info = parser.get_feed_info()

    articles_data = [a.to_dict() for a in articles]

    insights_data = []
    if openrouter_key and not openrouter_key.startswith('YOUR_'):
        try:
            generator = OpenRouterInsightsGenerator(openrouter_key)
            insights_data = [
                {
                    'title': ins.title,
                    'key_takeaways': ins.key_takeaways,
                    'impact_analysis': ins.impact_analysis,
                    'related_tech': ins.related_tech,
                    'sentiment': ins.sentiment,
                    'read_time_estimate': ins.read_time_estimate
                }
                for ins in generator.generate_batch_insights(articles_data)
            ]
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            insights_data = [{'title': a.get('title', ''), 'key_takeaways': ['AI insights unavailable']} for a in articles_data]
    else:
        insights_data = [{'title': a.get('title', ''), 'key_takeaways': ['Add OpenRouter API key for AI insights']} for a in articles_data]

    today = datetime.now().strftime('%Y-%m-%d')
    digest = DailyDigest(
        date=today,
        articles=articles_data,
        insights=insights_data,
        generated_at=datetime.now().isoformat(),
        feed_info=feed_info
    )

    storage = StorageManager(config.get('data_dir', 'data'))
    storage.save_digest(digest)
    return digest

def main():
    try:
        digest = generate_digest()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": True, "date": digest.date})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)})
        }
