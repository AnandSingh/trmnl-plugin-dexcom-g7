import os
import random
from datetime import datetime, timedelta, timezone

def generate_mock_data(entries=10):
    """Generate mock glucose data for testing."""
    data = []
    current_time = datetime.now(timezone.utc)

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

def generate_chart(data):
    chart_blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    sgv_values = [entry["sgv"] for entry in data]

    min_val = min(sgv_values)
    max_val = max(sgv_values)
    range_val = max_val - min_val or 1  # Prevent division by zero

    chart = ''.join([
        chart_blocks[int((sgv - min_val) / range_val * (len(chart_blocks) - 1))]
        for sgv in sgv_values
    ])
    return chart

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

def test():
    # Generate sample mock data
    mock_data = generate_mock_data(entries=10)
    latest_entry = mock_data[-1]  # Use the most recent reading

    # Prepare the data to send to TRMNL
    trmnl_data = {
        "glucose": latest_entry["sgv"],
        "trend": get_trend_arrow(latest_entry["direction"]),
        "time": latest_entry["dateString"],
        "chart": generate_chart(mock_data)
    }

    # Print the data for testing
    print(trmnl_data)
