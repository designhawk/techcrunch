"""Storage Manager for Daily Digests"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class DailyDigest:
    date: str
    articles: List[Dict]
    insights: List[Dict]
    generated_at: str
    feed_info: Dict


class StorageManager:
    def __init__(self, data_dir: str = None):
        if data_dir is None or data_dir == "data":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Check if data dir exists relative to script, otherwise use cwd
            script_data = os.path.join(script_dir, 'data')
            if os.path.exists(script_data):
                data_dir = script_data
            else:
                data_dir = os.path.join(os.getcwd(), 'data')
        elif not os.path.isabs(data_dir):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, data_dir)
        self.data_dir = data_dir
        self._ensure_data_dir()
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_digest_path(self, date: str) -> str:
        return os.path.join(self.data_dir, f"digest_{date}.json")

    def save_digest(self, digest: DailyDigest) -> str:
        """Save a daily digest to file"""
        path = self._get_digest_path(digest.date)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(digest), f, indent=2, ensure_ascii=False)
        return path

    def load_digest(self, date: str) -> Optional[DailyDigest]:
        """Load a daily digest by date"""
        path = self._get_digest_path(date)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return DailyDigest(**data)
        return None

    def list_digests(self) -> List[str]:
        """List all available digest dates"""
        if not os.path.exists(self.data_dir):
            return []
        files = [f.replace('digest_', '').replace('.json', '')
                 for f in os.listdir(self.data_dir)
                 if f.startswith('digest_') and f.endswith('.json')]
        return sorted(files, reverse=True)

    def get_latest_digest(self) -> Optional[DailyDigest]:
        """Get the most recent digest"""
        dates = self.list_digests()
        if dates:
            return self.load_digest(dates[0])
        return None

    def delete_digest(self, date: str) -> bool:
        """Delete a digest by date"""
        path = self._get_digest_path(date)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def get_stats(self) -> Dict:
        """Get storage statistics"""
        digests = self.list_digests()
        return {
            "total_digests": len(digests),
            "latest_date": digests[0] if digests else None,
            "storage_path": os.path.abspath(self.data_dir)
        }
