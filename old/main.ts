import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const TRMNL_API_KEY = process.env.TRMNL_API_KEY!;
const TRMNL_PLUGIN_ID = process.env.TRMNL_PLUGIN_ID!;
const USE_MOCK_DATA = process.env.USE_MOCK_DATA === 'true';

function generateMockData() {
  const now = new Date();
  const latestValue = 80 + Math.floor(Math.random() * 100); // 80–180

  const trend = latestValue < 70 ? "⚠️ Low" : latestValue > 180 ? "🔴 High" : "🟢 Normal";

  return {
    glucose: latestValue,
    trend,
    time: now.toLocaleString(),
    chart: generateAsciiChart()
  };
}

function generateAsciiChart() {
  const blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];
  const readings = Array.from({ length: 24 }, () => 80 +
Math.floor(Math.random() * 100));
  const min = Math.min(...readings);
  const max = Math.max(...readings);
  const range = max - min || 1;

  return readings.map(v => blocks[Math.floor(((v - min) / range) *
(blocks.length - 1))]).join('');
}

async function sendToTrmnl(data: any) {
  const url = `https://usetrmnl.com/api/custom_plugins/${TRMNL_PLUGIN_ID}`;

  try {
    const response = await axios.post(
      url,
      { data },
      {
        headers: {
          Authorization: `Bearer ${TRMNL_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('✅ Data sent to TRMNL:', response.status);
  } catch (err: any) {
    console.error('❌ Failed to send data to TRMNL:',
err.response?.data || err.message);
  }
}

async function main() {
  if (!TRMNL_API_KEY || !TRMNL_PLUGIN_ID) {
    console.error('❌ Missing TRMNL credentials in .env');
    return;
  }

  const payload = USE_MOCK_DATA ? generateMockData() : {}; // later we add real Dexcom here
  console.log('📦 Sending payload to TRMNL:', payload);
  await sendToTrmnl(payload);
}

main();
