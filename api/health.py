import json
from datetime import datetime

def main():
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        })
    }
