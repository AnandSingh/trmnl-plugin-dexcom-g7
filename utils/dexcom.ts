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

export async function getDexcomData() {
  const sessionId = await getSessionId();

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
        maxCount: 1,
      },
    });

    return response.data;
  } catch (err: any) {
    console.error('Dexcom data fetch failed:', err.response?.data || err.message);
    throw new Error('Failed to fetch glucose data.');
  }
}
