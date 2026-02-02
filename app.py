"""TechCrunch Daily Digest Web Application"""
import yaml
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for

from rss_parser import RSSParser
from openrouter_insights import OpenRouterInsightsGenerator
from storage import StorageManager, DailyDigest


def load_config(config_path: str = None) -> dict:
    """Load configuration from YAML file"""
    if config_path is None:
        # Check multiple possible locations
        possible_paths = [
            'config.yaml',
            os.path.join(os.getcwd(), 'config.yaml'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml'),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                config_path = path
                break
        else:
            print(f"Warning: config.yaml not found in: {possible_paths}")
            return {}

    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        return {}


def create_daily_digest():
    """Create a new daily digest with articles and AI insights"""
    config = load_config()
    rss_url = config.get('rss_url', 'https://techcrunch.com/feed/')
    # Support both config file and environment variable
    openrouter_key = os.environ.get('OPENROUTER_API_KEY', config.get('openrouter_api_key', ''))

    if not openrouter_key:
        print("[ERROR] No OpenRouter API key found. Set OPENROUTER_API_KEY env var in Render.")

    parser = RSSParser(rss_url)
    articles = parser.parse_articles(limit=15)
    feed_info = parser.get_feed_info()

    articles_data = [a.to_dict() for a in articles]

    insights_data = []
    if openrouter_key and not openrouter_key.startswith('YOUR_'):
        try:
            print(f"[INFO] Using OpenRouter API key: {openrouter_key[:15]}...")
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


app = Flask(__name__)
config = load_config()
storage = StorageManager(config.get('data_dir', 'data'))

# Generation status for progress tracking
generation_status = {
    'running': False,
    'articles': 0,
    'images': 0,
    'insights': 0,
    'complete': False
}


@app.route('/')
def index():
    """Main page - show latest digest"""
    latest = storage.get_latest_digest()
    if latest:
        return render_template('index.html', digest=latest)
    return render_template('no_digest.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Trigger a new digest generation"""
    try:
        # Reset status
        global generation_status
        generation_status = {'running': True, 'articles': 0, 'images': 0, 'insights': 0, 'complete': False}

        digest = create_daily_digest()

        generation_status['complete'] = True
        generation_status['running'] = False

        if request.is_json:
            return jsonify({'success': True, 'date': digest.date})
        return redirect(url_for('index'))
    except Exception as e:
        generation_status['running'] = False
        generation_status['complete'] = True
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return render_template('error.html', error=str(e))


@app.route('/progress')
def progress():
    """Progress page for digest generation"""
    return render_template('progress.html')


@app.route('/api/status')
def api_status():
    """API endpoint for generation status"""
    return jsonify(generation_status)


@app.route('/api/digest/<date>')
def api_digest(date):
    """API endpoint for digest data"""
    digest = storage.load_digest(date)
    if digest:
        return jsonify(asdict(digest))
    return jsonify({'error': 'Digest not found'}), 404


@app.route('/stats')
def stats():
    """Storage statistics"""
    stats = storage.get_stats()
    return jsonify(stats)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


def asdict(digest):
    """Helper to convert dataclass to dict"""
    from dataclasses import asdict as _asdict
    return _asdict(digest)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', config.get('port', 5000)))
    host = config.get('host', '0.0.0.0')
    debug = config.get('debug', False)

    app.run(host=host, port=port, debug=debug)
