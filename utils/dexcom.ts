import { DexcomApi } from 'dexcom-cloud';
import dotenv from 'dotenv';

dotenv.config();

const dexcom = new DexcomApi({
  username: process.env.DEXCOM_USERNAME!,
  password: process.env.DEXCOM_PASSWORD!,
  accountName: 'dexcom'
});

export async function getDexcomData() {
  return await dexcom.fetchGlucoseReadings(1);
}
