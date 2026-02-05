import os
import requests


def main(request):
    INNGEST_KEY = os.environ.get("INNGEST_EVENT_KEY")
    INNGEST_URL = "https://api.inngest.com/e"

    try:
        response = requests.post(
            f"{INNGEST_URL}/app/refresh",
            headers={
                "Authorization": f"Bearer {INNGEST_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "data": {
                    "triggered_at": str(
                        __import__("datetime").datetime.now().isoformat()
                    ),
                    "source": "vercel_ui",
                }
            },
            timeout=10,
        )

        if response.status_code in (200, 202):
            return {"status": "triggered", "success": True}
        else:
            return {"status": "error", "error": response.text}, 500

    except Exception as e:
        return {"status": "error", "error": str(e)}, 500
