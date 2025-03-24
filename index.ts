import { getDexcomData } from './utils/dexcom';

export default async function render() {
  const data = await getDexcomData();

  if (!data || data.length === 0) {
    return "📉 No glucose data found.";
  }

  const latest = data[0];
  const emoji = latest.value < 70 ? "⚠️ Low" : latest.value > 180 ?
"🔴 High" : "🟢 Normal";

  return `🩸 Glucose: ${latest.value} mg/dL\n🕒 Time:
${latest.displayTime}\nStatus: ${emoji}`;
}
