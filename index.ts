import { getDexcomData } from './utils/dexcom';

function parseDexcomTime(dt: string): string {
  const match = dt.match(/\/Date\((\d+)\)\//);
  if (match) {
    const timestamp = parseInt(match[1], 10);
    return new Date(timestamp).toLocaleString();
  }
  return dt;
}

export default async function render() {
  const data = await getDexcomData();

  if (!data || data.length === 0) {
    return "❌ No glucose data available.";
  }

  const latest = data[0];
  const value = latest.Value;
  const time = parseDexcomTime(latest.DT);
  const status = value < 70 ? "⚠️ Low" : value > 180 ? "🔴 High" : "🟢 Normal";

  return `🩸 Glucose: ${value} mg/dL\n🕒 Time: ${time}\nStatus: ${status}`;
}
