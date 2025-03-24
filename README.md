# Dexcom G7 Plugin for trmnl 🩸

An open-source plugin for [trmnl](https://usetrmnl.com) that fetches glucose data from the **Dexcom G7** via the **Dexcom Share API** and displays:

- ✅ Real-time glucose values
- ✅ Time of last reading
- ✅ Status indicator (🟢/🔴/⚠️)
- ✅ 24-hour ASCII glucose trend chart
- ✅ Offline mock data mode for testing

---

## 📦 Features

- 🌐 **Live mode**: Uses real Dexcom credentials via the Share API
- 🧪 **Mock mode**: Fully testable with realistic simulated glucose data
- 📊 **Trend chart**: Terminal-friendly ASCII graph of 24-hour history

---

## 🔧 Setup Instructions

### 1. Clone the plugin

```bash
git clone https://github.com/YOUR_USERNAME/trmnl-plugin-dexcom-g7.git
cd trmnl-plugin-dexcom-g7
npm install
```

---

### 2. Create the `.env` file

```bash
cp .env.example .env
```

Then fill it out:

```env
DEXCOM_USERNAME=your_dexcom_username
DEXCOM_PASSWORD=your_dexcom_password
USE_MOCK_DATA=true
```

Set `USE_MOCK_DATA=false` to connect to Dexcom servers.

---

### 3. Run the plugin locally (for development)

```bash
npx ts-node index.ts
```

Expected output:

```
📈 24h Glucose Trend (mg/dL)
▃▃▄▅▅▆▆▇▇█▆▅▄▃▃▂▁▂▃▄▅▆▆▇

🩸 Glucose: 145 mg/dL
🕒 Time: 3/24/2025, 10:45:00 PM
Status: 🟢 Normal
```

---

## 🧪 Mock Mode (for offline testing)

Mock mode is enabled by setting:

```env
USE_MOCK_DATA=true
```

It generates 24 hourly readings for chart rendering and random status values. Useful for demo, development, and no-Dexcom scenarios.

---

## 📂 File Structure

```
trmnl-plugin-dexcom-g7/
├── index.ts             # Main plugin render logic
├── manifest.json        # Plugin metadata
├── utils/
│   └── dexcom.ts        # Dexcom Share API + mock data
├── .env.example         # Template for credentials
├── .gitignore
└── README.md
```

---

## 🧪 Testing in trmnl (online)

1. Push this plugin to your GitHub:
   ```
   https://github.com/YOUR_USERNAME/trmnl-plugin-dexcom-g7
   ```

2. Log in to [https://usetrmnl.com](https://usetrmnl.com)

3. Navigate to:
   - `Settings → Plugins` or
   - `Customize → Add Plugin`

4. Add your GitHub repo URL. trmnl will read `manifest.json` and load your plugin.

⚠️ You may need a Pro account or plugin developer access to use external plugins.

---

## 💬 Output Format

```
📈 24h Glucose Trend (mg/dL)
▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇

🩸 Glucose: 152 mg/dL
🕒 Time: 3/24/2025, 9:00 PM
Status: 🟢 Normal
```

---

## 🔐 Notes on Dexcom Share API

- This plugin uses the **unofficial** Dexcom Share API used by the mobile app
- Requires Share to be enabled in your Dexcom G6/G7 app
- No developer key needed (uses `applicationId` fingerprint)

---

## ✅ TODO

- [ ] Automatically fallback to mock mode if Dexcom Share login fails
- [ ] Add trend arrow indicators based on `Trend` field (↗️, ➘, ➖)
- [ ] Add timestamp labels (08h, 12h, 20h) to the ASCII chart
- [ ] Add support for non-US Dexcom accounts (`dexcom-server=EU`)
- [ ] Add in-plugin settings UI (for trmnl integration)
- [ ] Support `asciichart` or other richer graphing libraries
- [ ] Add unit tests and offline data validator

---

## 📄 License

MIT © 2025 Anand Singh
