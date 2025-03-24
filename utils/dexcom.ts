import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const DEXCOM_BASE_URL = 'https://share2.dexcom.com/ShareWebServices/Services';
const APPLICATION_ID = 'd89443d2-327c-4a6f-89e5-496bbb0317db';

async function getSessionId(): Promise<string> {
  const url = `${DEXCOM_BASE_URL}/General/LoginPublisherAccountByName`;

  try {
    const response = await axios.post(url, {
      accountName: process.env.DEXCOM_USERNAME,
      password: process.env.DEXCOM_PASSWORD,
      applicationId: APPLICATION_ID,
    }, {
      headers: {
        'User-Agent': 'Dexcom Share/3.0.2.11',
        'Content-Type': 'application/json',
    }});
    return response.data;
  } catch (err: any) {
    console.error('Dexcom login failed:', err.response?.data || err.message);
    throw new Error('Failed to authenticate with Dexcom Share API.');
  }
}

function generateMockData(count = 24) {
  const now = Date.now();
  const readings = [];

  for (let i = 0; i < count; i++) {
    const timestamp = now - (i * 60 * 60 * 1000); // 1 hour apart
    const value = 80 + Math.floor(Math.random() * 100); // 80–180
    const trend = Math.floor(Math.random()*9);
    readings.unshift({
      Value: value,
      Trend: trend,
      DT: `/Date(${timestamp})/`
    });
  }

  return readings;
}


export async function getDexcomData() {
  if(process.env.USE_MOCK_DATA === 'true') {
    console.log(" Mock mode enabled, Returing simulated glucose data ...")
    return generateMockData();
  }
  if (!process.env.DEXCOM_USERNAME || !process.env.DEXCOM_PASSWORD) {
    throw new Error('Missing Dexcom username or password.');
  }
  const sessionId = await getSessionId();
  console.log('Dexcom session ID:', sessionId);

  const url = `${DEXCOM_BASE_URL}/Publisher/ReadPublisherLatestGlucoseValues`;
  try {
    const response = await axios.post(url, null, {
      headers: {
        'User-Agent': 'Dexcom Share/3.0.2.11',
        'Content-Type': 'application/json',
      },
      params: {
        sessionId,
        minutes: 1440,
        maxCount: 10,
      },
    });
    console.log('Dexcom data fetch succeeded:', response.data);
    return response.data;
  } catch (err: any) {
    console.error('Dexcom data fetch failed:', err.response?.data || err.message);
    throw new Error('Failed to fetch glucose data.');
  }
}
