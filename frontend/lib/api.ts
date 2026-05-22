const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function fetchBacktest(ticker: string, start: string, end: string, strategy: string) {
  const res = await fetch(
    `${BASE}/api/backtest?ticker=${ticker}&start=${start}&end=${end}&strategy=${strategy}`
  );
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchCompare(ticker: string, start: string, end: string, strategies: string[]) {
  const res = await fetch(
    `${BASE}/api/backtest/compare?ticker=${ticker}&start=${start}&end=${end}&strategies=${strategies.join(",")}`
  );
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchModels() {
  const res = await fetch(`${BASE}/api/models`);
  return res.json();
}

export async function fetchModel(slug: string) {
  const res = await fetch(`${BASE}/api/models/${slug}`);
  return res.json();
}

export async function fetchRankings(period = "1Y", market = "us") {
  const res = await fetch(`${BASE}/api/rankings?period=${period}&market=${market}`);
  return res.json();
}

export async function searchTicker(q: string) {
  const res = await fetch(`${BASE}/api/search/ticker?q=${encodeURIComponent(q)}`);
  return res.json();
}

export async function fetchPopular(market = "all") {
  const res = await fetch(`${BASE}/api/search/popular?market=${market}`);
  return res.json();
}
