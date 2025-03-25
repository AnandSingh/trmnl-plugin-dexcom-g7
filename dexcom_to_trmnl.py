import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from pydexcom import Dexcom

load_dotenv()

TRMNL_API_KEY = os.getenv("TRMNL_API_KEY")
TRMNL_PLUGIN_ID = os.getenv("TRMNL_PLUGIN_ID")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"

def is_mock_mode():
    """Returns True only if USE_MOCK_DATA is explicitly true/yes/1; otherwise defaults to live."""
    val = os.getenv("USE_MOCK_DATA", "").strip().lower()
    return val in ("1", "true", "yes")


def generate_mock_data():
    value = 80 + int(os.urandom(1)[0] % 100)
    chart_blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    chart_values = [80 + (os.urandom(1)[0] % 100) for _ in range(24)]
    min_val = min(chart_values)
    max_val = max(chart_values)
    range_val = max_val - min_val or 1
    chart = ''.join([chart_blocks[int((v - min_val) / range_val * (len(chart_blocks) - 1))] for v in chart_values])
    trend = "⚠️ Low" if value < 70 else "🔴 High" if value > 180 else "🟢 Normal"
    return {
        "glucose": value,
        "trend": trend,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chart": chart
    }


def get_live_glucose_data():
    dexcom = Dexcom(
        username=os.getenv("DEXCOM_USERNAME"),
        password=os.getenv("DEXCOM_PASSWORD"),
        region=os.getenv("DEXCOM_SERVER", "us").lower()
    )
    reading = dexcom.get_current_glucose_reading()
    
    if not reading:
        print("⚠️ No glucose reading returned from Dexcom!")
        raise Exception("No glucose data available. Try again later.")
    
    print(reading)
    return {
        "glucose": reading.value,
        "trend": reading.trend_description + " " + reading.trend_arrow,
        "time": reading.datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "chart": "▁▂▃▄▅▆▇█"[(reading.value - 40) // 20] * 24
    }

def send_data():
    if not TRMNL_API_KEY or not TRMNL_PLUGIN_ID:
        print("❌ Missing TRMNL_API_KEY or TRMNL_PLUGIN_ID")
        return

    if is_mock_mode():
        data = generate_mock_data()
        print("🧪 Mock mode enabled")
    else:
        data = get_live_glucose_data()
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
