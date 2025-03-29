import os
import random
from datetime import datetime, timedelta, timezone
import requests
import json

def generate_mock_data(entries=10):
    """Generate mock glucose data for testing."""
    data = []
    current_time = datetime.now(timezone.utc)  # Use timezone-aware UTC datetime

    for i in range(entries):
        reading_time = current_time - timedelta(minutes=i * 5)
        glucose_value = random.randint(80, 180)
        direction = random.choice([
            "DoubleUp", "SingleUp", "FortyFiveUp", "Flat", 
            "FortyFiveDown", "SingleDown", "DoubleDown", "NONE"
        ])
        
        entry = {
            "sgv": glucose_value,
            "direction": direction,
            "dateString": reading_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        data.append(entry)

    return data[::-1]  # Reverse to make oldest first

def get_trend_arrow(direction: str) -> str:
    arrows = {
        "DoubleUp": "⏫ Double Up",
        "SingleUp": "🔼 Rising",
        "FortyFiveUp": "↗️ Slight Rise",
        "Flat": "➡️ Flat",
        "FortyFiveDown": "↘️ Slight Drop",
        "SingleDown": "🔽 Falling",
        "DoubleDown": "⏬ Rapid Drop",
        "NONE": "⚪ No Trend",
    }
    return arrows.get(direction, f"❓ {direction}")

def prepare_data_for_trmnl(mock_data):
    """Prepare data to be sent to TRMNL."""
    latest_entry = mock_data[-1]  # Use the most recent reading
    labels = [entry["dateString"][11:16] for entry in mock_data]  # Extract only the HH:MM part
    glucose_values = [entry["sgv"] for entry in mock_data]

    trmnl_data = {
        "glucose": latest_entry["sgv"],
        "trend": get_trend_arrow(latest_entry["direction"]),
        "time": latest_entry["dateString"],
        "chart_labels": labels,
        "chart_data": glucose_values
    }
    return trmnl_data

def send_to_trmnl(trmnl_data):
    TRMNL_API_KEY = os.getenv("TRMNL_API_KEY")
    TRMNL_PLUGIN_ID = os.getenv("TRMNL_PLUGIN_ID")

    if not TRMNL_API_KEY or not TRMNL_PLUGIN_ID:
        print("❌ Missing TRMNL_API_KEY or TRMNL_PLUGIN_ID")
        return

    url = f"https://usetrmnl.com/api/custom_plugins/{TRMNL_PLUGIN_ID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"merge_variables": trmnl_data}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Sent to TRMNL ({response.status_code}):", response.text)
        else:
            print(f"❌ Error sending data to TRMNL ({response.status_code}):", response.text)
    except Exception as e:
        print("❌ Error sending data to TRMNL:", e)

def test():
    # Generate sample mock data
    mock_data = generate_mock_data(entries=10)
    trmnl_data = prepare_data_for_trmnl(mock_data)
    
    # Display data locally for testing
    print(json.dumps(trmnl_data, indent=4))
    
    # Uncomment below to send to TRMNL
    # send_to_trmnl(trmnl_data)

