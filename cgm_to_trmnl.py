from nightscout import fetch_sgv_values, get_trend_arrow

readings = fetch_sgv_values({"count": 24})
latest = readings[0]

print(f"🩸 {latest['sgv']} mg/dL")
print(f"➡️ {get_trend_arrow(latest.get('direction', 'Flat'))}")
print(f"🕒 {latest['dateString']}")