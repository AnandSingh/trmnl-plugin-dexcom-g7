import os
import time
import hashlib
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import pytz
from mock_data import *

load_dotenv()
print(f"RAW ENV: {os.getenv('USE_MOCK_DATA')}")
print(f"LOWERCASE ENV: {os.getenv('USE_MOCK_DATA').strip().lower()}")

TRMNL_API_KEY = os.getenv("TRMNL_API_KEY")
TRMNL_PLUGIN_ID = os.getenv("TRMNL_PLUGIN_ID")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
NIGHTSCOUT_URL = os.getenv("NIGHTSCOUT_URL")
NIGHTSCOUT_API_SECRET = os.getenv("NIGHTSCOUT_API_SECRET", "")
USE_HASHED_SECRET = True  # replicate behavior of firmware
TIMEZONE = os.getenv("TIMEZONE", "UTC")  # Default to UTC if not specified

def is_mock_mode():
    """Returns True only if USE_MOCK_DATA is explicitly true/yes/1; otherwise defaults to live."""
    val = os.getenv("USE_MOCK_DATA", "").strip().lower()
    return val in ("1", "true", "yes")


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

def format_timestamp(iso_timestamp: str) -> str:
    """Converts an ISO timestamp to a localized, readable format."""
    try:
        # Parse the ISO timestamp
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        
        # Convert to specified timezone
        target_tz = pytz.timezone(TIMEZONE)
        local_dt = dt.astimezone(target_tz)
        
        # Format to 'Month Day, Year - HH:MM AM/PM' format for display
        return local_dt.strftime("%b %d, %Y - %I:%M %p")
    except ValueError:
        return iso_timestamp  # Return original if parsing fails

def get_trend_arrow(direction: str) -> str:
    arrows = {
    "DoubleUp": '<i class="ti ti-arrow-big-up-lines"></i> Double Up',
    "SingleUp": '<i class="ti ti-arrow-big-up"></i> Rising',
    "FortyFiveUp": '<i class="ti ti-arrow-up-right"></i> Slight Rise',
    "Flat": '<i class="ti ti-arrow-right"></i> Flat',
    "FortyFiveDown": '<i class="ti ti-arrow-down-right"></i> Slight Drop',
    "SingleDown": '<i class="ti ti-arrow-big-down"></i> Falling',
    "DoubleDown": '<i class="ti ti-arrow-big-down-lines"></i> Rapid Drop',
    "NONE": '<i class="ti ti-circle"></i> No Trend',
    }
    return arrows.get(direction, f'<i class="ti ti-help"></i> {direction}')


def fetch_sgv_values(params=None):
    if not NIGHTSCOUT_URL:
        raise Exception("Error: NIGHTSCOUT_URL is not set")

    url = f"{NIGHTSCOUT_URL.rstrip('/')}/api/v1/entries/sgv.json"


    response = requests.get(url, headers=build_headers(), allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Error: Nightscout API error {response.status_code}: {response.text}")
    print(response)
    return response.json()


def fetch_entries_in_range(minutes_back=60, count=24):
    if not NIGHTSCOUT_URL:
        raise Exception("Error:: NIGHTSCOUT_URL is not set")
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

def get_live_glucose_data():
    try:
        # Fetch the latest data point (1 entry)
        readings = fetch_entries_in_range(5, 1)  # Fetch the most recent entry (last 5 minutes)
        
        if not readings:
            print("No glucose data available!")
            return
        
        latest = readings[0]
        sgv = latest["sgv"]
        direction = latest.get("direction", "Unknown")
        timestamp = latest.get("dateString", datetime.now(timezone.utc).isoformat())
        
        # Prepare data for the frontend
        trmnl_data = {
            "glucose": sgv,
            "trend": get_trend_arrow(direction),
            "time": format_timestamp(timestamp),
            "chart_data": [[timestamp[:16], sgv]]  # Send only the latest data point
        }

        return trmnl_data

    except Exception as e:
        print(f"Error: {e}")

def send_data():
    if not TRMNL_API_KEY or not TRMNL_PLUGIN_ID:
        print("Error: Missing TRMNL_API_KEY or TRMNL_PLUGIN_ID")
        return

    if is_mock_mode():
        # Generate sample mock data
        mock_data = generate_mock_data(entries=255)
        trmnl_data = prepare_data_for_trmnl(mock_data)
        print("Mock mode enabled")
    else:
        trmnl_data = get_live_glucose_data()
        print("Live mode (nightschout API) enabled")


    payload = {
        "merge_variables": trmnl_data
    }

    url = f"https://usetrmnl.com/api/custom_plugins/{TRMNL_PLUGIN_ID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }

    try: 
        #print(payload)
        response = requests.post(url, json=payload, headers=headers)
        print(f"Sent to TRMNL ({response.status_code}):", response.text)
    except Exception as e:
        print("Error: sending data to TRMNL:", e)

if __name__ == "__main__":
    #data = get_live_glucose_data()
    #print(data)
    send_data()

