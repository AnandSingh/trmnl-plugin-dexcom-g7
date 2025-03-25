import { getDexcomData } from './utils/dexcom';

function parseDexcomTime(dt: string): string {
  const match = dt.match(/\/Date\((\d+)\)\//);
  if (match) {
    const timestamp = parseInt(match[1], 10);
    return new Date(timestamp).toLocaleString();
  }
  return dt;
}


function renderAsciiChart(data: { Value: number }[]) {
  const blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];

  const values = data.map(d => d.Value);
  const min = Math.min(...values);
  const max = Math.max(...values);

  const scale = max - min || 1;

  const bars = values.map(v => {
    const index = Math.floor(((v - min) / scale) * (blocks.length - 1));
    return blocks[index];
  });

  return `📈 24h Glucose Trend (mg/dL)\n${bars.join('')}\n`;
}


export default async function render() {
  const data = await getDexcomData();
  //console.log("Data Received", data);

  if (!data || data.length === 0) {
    return "❌ No glucose data available.";
  }

  const latest = data[data.length - 1];
  const value = latest.Value;

  const match = latest.DT.match(/\/Date\((\d+)\)\//);
  const time = match ? new Date(parseInt(match[1],10)).toLocaleString() : 'Unknown';

  const status = value < 70 ? "⚠️ Low" : value > 180 ? "🔴 High" : "🟢 Normal";

  const chart = renderAsciiChart(data);

  return `${chart}\n🩸 Current Glucose: ${value} mg/dL\n🕒 Time:
${time}\nStatus: ${status}`;
}


render().then(console.log).catch(console.error);
