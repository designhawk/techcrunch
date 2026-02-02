"""AI Insights Generator using OpenRouter API with Mistral fallback"""
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
        self.mistral_key = os.environ.get('MISTRAL_API_KEY', '')
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.mistral_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.environ.get("HTTP_REFERER", "http://localhost:5000"),
            "X-Title": "TechCrunch Digest"
        }
        self.mistral_headers = {
            "Authorization": f"Bearer {self.mistral_key}",
            "Content-Type": "application/json"
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

        # Try OpenRouter first
        try:
            print(f"[DEBUG] Calling OpenRouter for: {title[:50]}...")
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
            print(f"[DEBUG] Response status: {response.status_code}")
            
            if response.status_code == 429:
                print(f"[WARN] OpenRouter rate limited, trying Mistral...")
                return self._call_mistral(prompt, title, article)
            
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"OpenRouter response for: {title[:30]}...")
            return self._parse_response(content, title)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"[WARN] OpenRouter rate limited, trying Mistral...")
                return self._call_mistral(prompt, title, article)
            print(f"[ERROR] HTTP error: {e.response.status_code} - {e.response.text}")
            return self._create_fallback_insight(article)
        except Exception as e:
            print(f"[ERROR] OpenRouter error: {type(e).__name__}: {e}")
            return self._create_fallback_insight(article)

    def _call_mistral(self, prompt: str, title: str, article: dict) -> ArticleInsight:
        """Call Mistral API as fallback"""
        if not self.mistral_key:
            print(f"[WARN] No MISTRAL_API_KEY set, using fallback")
            return self._create_fallback_insight(article)
        
        try:
            print(f"[DEBUG] Calling Mistral for: {title[:50]}...")
            response = requests.post(
                self.mistral_url,
                headers=self.mistral_headers,
                json={
                    "model": "mistral-small-latest",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                },
                timeout=60
            )
            print(f"[DEBUG] Mistral response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"Mistral response for: {title[:30]}...")
            return self._parse_response(content, title)
        except Exception as e:
            print(f"[ERROR] Mistral error: {type(e).__name__}: {e}")
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
