import os
import requests
from dotenv import load_dotenv

load_dotenv()

NIGHTSCOUT_URL = os.getenv("NIGHTSCOUT_URL")  # e.g. https://t1d.localghost.org
NIGHTSCOUT_API_SECRET = os.getenv("NIGHTSCOUT_API_SECRET", "")

def fetch_latest_sgv():
    if not NIGHTSCOUT_URL:
        raise Exception("❌ NIGHTSCOUT_URL is not set")

    url = f"{NIGHTSCOUT_URL.rstrip('/')}/api/v1/entries.json?count=1"
    headers = {
        "Accept": "application/json"
    }

    if NIGHTSCOUT_API_SECRET:
        headers["api-secret"] = NIGHTSCOUT_API_SECRET

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"❌ API Error {response.status_code}: {response.text}")

    data = response.json()
    if not data:
        raise Exception("❌ No glucose entries returned")

    entry = data[0]
    return {
        "glucose": entry.get("sgv"),
        "trend": entry.get("direction", "Unknown"),
        "time": entry.get("dateString")
    }

if __name__ == "__main__":
    try:
        result = fetch_latest_sgv()
        print("✅ Latest Nightscout Glucose Reading:")
        print(f"🩸 Glucose: {result['glucose']} mg/dL")
        print(f"➡️ Trend: {result['trend']}")
        print(f"🕒 Time: {result['time']}")
    except Exception as e:
        print("❌ Error:", e)
