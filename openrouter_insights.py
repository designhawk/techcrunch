"""AI Insights Generator using OpenRouter API"""
import os
import requests
from typing import List
from dataclasses import dataclass
import json
import time


@dataclass
class ArticleInsight:
    title: str
    key_takeaways: List[str]
    impact_analysis: str
    related_tech: List[str]
    sentiment: str
    read_time_estimate: str


class OpenRouterInsightsGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.environ.get("HTTP_REFERER", "http://localhost:5000"),
            "X-Title": "TechCrunch Digest"
        }

    def generate_insight(self, article: dict) -> ArticleInsight:
        """Generate AI insight for a single article"""
        title = article.get('title', '')
        summary = article.get('summary', '')[:400]
        categories = article.get('categories', [])

        prompt = f"""
Analyze this TechCrunch article and provide insights. Respond ONLY with valid JSON.

Article: {title}
Summary: {summary}
Categories: {', '.join(categories)}

Output JSON with:
{{
  "key_takeaways": ["3 main points from this article"],
  "impact_analysis": "1-2 sentences on why this matters",
  "related_tech": ["technologies/companies mentioned"],
  "sentiment": "positive/neutral/negative",
  "read_time_estimate": "short/medium/long"
}}
"""

        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json={
                    "model": "tngtech/deepseek-r1t2-chimera:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"OpenRouter response for: {title[:30]}...")
            return self._parse_response(content, title)
        except Exception as e:
            print(f"OpenRouter error: {e}")
            return self._create_fallback_insight(article)

    def generate_batch_insights(self, articles: List[dict]) -> List[ArticleInsight]:
        """Generate insights for multiple articles"""
        insights = []
        for article in articles:
            insight = self.generate_insight(article)
            insights.append(insight)
            time.sleep(0.5)
        return insights

    def _parse_response(self, response_text: str, title: str) -> ArticleInsight:
        """Parse AI response JSON"""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            data = json.loads(json_str)
            return ArticleInsight(
                title=title,
                key_takeaways=data.get('key_takeaways', []),
                impact_analysis=data.get('impact_analysis', ''),
                related_tech=data.get('related_tech', []),
                sentiment=data.get('sentiment', 'neutral'),
                read_time_estimate=data.get('read_time_estimate', 'medium')
            )
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parse error: {e}")
            return self._create_fallback_insight({'title': title})

    def _create_fallback_insight(self, article: dict) -> ArticleInsight:
        """Create fallback when API fails"""
        title = article.get('title', '')
        summary = article.get('summary', '')[:200]
        categories = article.get('categories', [])

        return ArticleInsight(
            title=title,
            key_takeaways=[
                f"Category: {categories[0] if categories else 'Tech'}",
                summary.split('.')[0] + '.' if summary else 'See full article',
                "Click to read more details"
            ],
            impact_analysis="This article covers recent tech industry news",
            related_tech=categories[:3],
            sentiment="neutral",
            read_time_estimate="medium"
        )
