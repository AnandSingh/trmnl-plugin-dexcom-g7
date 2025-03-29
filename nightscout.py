import os
import time
import hashlib
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


TRMNL_API_KEY = os.getenv("TRMNL_API_KEY")
TRMNL_PLUGIN_ID = os.getenv("TRMNL_PLUGIN_ID")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
NIGHTSCOUT_URL = os.getenv("NIGHTSCOUT_URL")
NIGHTSCOUT_API_SECRET = os.getenv("NIGHTSCOUT_API_SECRET", "")
USE_HASHED_SECRET = True  # replicate behavior of firmware

def sha1_hash(value: str) -> str:
    return hashlib.sha1(value.encode('utf-8')).hexdigest()

def build_headers():
    headers = {
        "Accept": "application/json"
    }
    if NIGHTSCOUT_API_SECRET:
        secret = sha1_hash(NIGHTSCOUT_API_SECRET) if USE_HASHED_SECRET else NIGHTSCOUT_API_SECRET
        headers["api-secret"] = secret
    return headers

def fetch_sgv_values(params=None):
    if not NIGHTSCOUT_URL:
        raise Exception("❌ NIGHTSCOUT_URL is not set")

    url = f"{NIGHTSCOUT_URL.rstrip('/')}/api/v1/entries/sgv.json"


    response = requests.get(url, headers=build_headers(), allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Nightscout API error {response.status_code}: {response.text}")
    print(response)
    return response.json()


def fetch_entries_in_range(minutes_back=60, count=24):
    if not NIGHTSCOUT_URL:
        raise Exception("❌ NIGHTSCOUT_URL is not set")
    to_epoch = int(time.time() * 1000)
    from_epoch = to_epoch - (minutes_back * 60 * 1000)

    url = (
        f"{NIGHTSCOUT_URL.rstrip('/')}/api/v1/entries"
        f"?find[date][$gt]={from_epoch}"
        f"&find[date][$lte]={to_epoch}"
        f"&count={count}"
    )

    response = requests.get(url, headers=build_headers(), allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Nightscout API error {response.status_code}: {response.text}")
    print(response)
    return response.json()

def print_filtered_glucose_data():
    try:
        readings = fetch_entries_in_range(60, 24)
        if not readings:
            print("⚠️ No glucose data in time range.")
            return
        print(readings)
        latest = readings[0]
        sgv = latest["sgv"]
        direction = latest.get("direction", "Unknown")
        timestamp = latest.get("dateString", datetime.utcnow().isoformat())

        print(f"🩸 BG: {sgv} mg/dL")
        print(f"➡️ Trend: {direction}")
        print(f"🕒 Time: {timestamp}")

        values = [r["sgv"] for r in readings if "sgv" in r][:24]
        chart_blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val or 1
        chart = ''.join([chart_blocks[int((v - min_val) / range_val * (len(chart_blocks) - 1))] for v in values])

        print(f"📈 Chart: {chart}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print_filtered_glucose_data()

def send_data():
    if not TRMNL_API_KEY or not TRMNL_PLUGIN_ID:
        print("❌ Missing TRMNL_API_KEY or TRMNL_PLUGIN_ID")
        return

    if is_mock_mode():
        data = generate_mock_data()
        print("🧪 Mock mode enabled")
    else:
        data = print_filtered_glucose_data()
        print("🌐 Live mode (Dexcom API) enabled")

    payload = {
        "merge_variables": data
    }

    url = f"https://usetrmnl.com/api/custom_plugins/{TRMNL_PLUGIN_ID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"✅ Sent to TRMNL ({response.status_code}):", response.text)
    except Exception as e:
        print("❌ Error sending data to TRMNL:", e)

if __name__ == "__main__":
    send_data()