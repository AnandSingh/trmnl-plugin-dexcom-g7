# Dexcom G7 Plugin for TRMNL 🩸

This plugin displays real-time or mock Dexcom G7 glucose data in your [TRMNL](https://usetrmnl.com) dashboard using their **Custom Plugin API** and webhook strategy.

It supports:
- ✅ Real-time glucose readings via Dexcom Share API (planned)
- ✅ Fully offline mock mode for development & testing
- ✅ ASCII 24-hour glucose chart (auto-generated)
- ✅ Python or TypeScript-based data push
- ✅ Liquid/HTML dashboard rendering

---

## 📦 Project Structure

```
trmnl-plugin-dexcom-g7/
├── main.ts                 # Webhook sender using TypeScript + axios
├── send_to_trmnl.py        # Python version of the webhook sender
├── template.html.liquid    # Renders dashboard display
├── .env.example            # API keys and config
├── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Plugin

```bash
git clone https://github.com/YOUR_USERNAME/trmnl-plugin-dexcom-g7.git
cd trmnl-plugin-dexcom-g7
npm install
```

Install Python deps (if using Python):

```bash
pip install -r requirements.txt
```

---

### 2. Create the `.env` File

```bash
cp .env.example .env
```

Then add:

```
TRMNL_API_KEY=your_actual_trmnl_api_key
TRMNL_PLUGIN_ID=your_plugin_id_from_trmnl
USE_MOCK_DATA=true
```

---

### 3. Add the Dashboard Template

In your [TRMNL dashboard](https://usetrmnl.com):

1. Go to: **Plugins → Private Plugin → Your Plugin**
2. Paste contents of `template.html.liquid` into the **Markup** or **Template** field
3. Save

---

### 4. Send Data (Choose one)

#### Option A: TypeScript

```bash
npx ts-node main.ts
```

#### Option B: Python

```bash
python send_to_trmnl.py
```

---

### ✅ Output in TRMNL

```
🩸 Glucose: 145 mg/dL
📈 Chart: ▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▅▆
🕒 Time: 2025-03-24 23:45:00
Status: 🟢 Normal
```

---

## 🔮 Future Features

- [ ] Dexcom Share live API integration
- [ ] Auto-push when new data is available
- [ ] Trend arrows (↗️, ↘️, ➖)
- [ ] Alert logic for high/low readings
- [ ] GitHub Action-based cron trigger
- [ ] Device association from TRMNL dashboard
- [ ] ASCII + Unicode graph visual options

---

## 🧪 Development Mode

Keep `USE_MOCK_DATA=true` to develop without hitting the Dexcom API.

---

## 📄 License

MIT © 2025 Your Name
