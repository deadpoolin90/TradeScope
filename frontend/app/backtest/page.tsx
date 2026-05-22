"use client";
import { useState } from "react";
import { fetchCompare, searchTicker } from "@/lib/api";
import { Search, TrendingUp, TrendingDown } from "lucide-react";
import EquityChart from "@/components/charts/EquityChart";
import MetricCard from "@/components/backtest/MetricCard";
import clsx from "clsx";

const PERIODS = [
  { label: "1개월", value: "1M", days: 30 },
  { label: "3개월", value: "3M", days: 90 },
  { label: "6개월", value: "6M", days: 180 },
  { label: "1년",   value: "1Y", days: 365 },
  { label: "3년",   value: "3Y", days: 1095 },
  { label: "5년",   value: "5Y", days: 1825 },
];

const STRATEGIES = [
  { slug: "ma-crossover",   name: "MA 교차" },
  { slug: "macd",           name: "MACD" },
  { slug: "rsi",            name: "RSI" },
  { slug: "bollinger-bands",name: "볼린저밴드" },
  { slug: "momentum",       name: "모멘텀" },
  { slug: "mean-reversion", name: "평균회귀" },
  { slug: "xgboost",        name: "XGBoost" },
];

function dateOffset(days: number) {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d.toISOString().slice(0, 10);
}

export default function BacktestPage() {
  const [ticker,     setTicker]     = useState("AAPL");
  const [tickerName, setTickerName] = useState("Apple Inc.");
  const [searchQ,    setSearchQ]    = useState("");
  const [suggestions,setSuggestions]= useState<any[]>([]);
  const [period,     setPeriod]     = useState("1Y");
  const [selected,   setSelected]   = useState<string[]>(["ma-crossover", "macd", "rsi"]);
  const [results,    setResults]    = useState<any[]>([]);
  const [loading,    setLoading]    = useState(false);
  const [error,      setError]      = useState("");

  // 종목 검색
  async function handleSearch(q: string) {
    setSearchQ(q);
    if (q.length < 1) { setSuggestions([]); return; }
    const data = await searchTicker(q).catch(() => ({ results: [] }));
    setSuggestions(data.results ?? []);
  }

  function selectTicker(t: any) {
    setTicker(t.ticker);
    setTickerName(t.name);
    setSearchQ("");
    setSuggestions([]);
  }

  function toggleStrategy(slug: string) {
    setSelected(prev =>
      prev.includes(slug)
        ? prev.filter(s => s !== slug)
        : prev.length < 3 ? [...prev, slug] : prev
    );
  }

  async function runBacktest() {
    if (selected.length === 0) { setError("전략을 1개 이상 선택하세요"); return; }
    setLoading(true);
    setError("");
    try {
      const days = PERIODS.find(p => p.value === period)?.days ?? 365;
      const start = dateOffset(days);
      const end   = new Date().toISOString().slice(0, 10);
      const data  = await fetchCompare(ticker, start, end, selected);
      setResults(data.results ?? []);
    } catch (e: any) {
      setError("백테스팅 중 오류가 발생했습니다. 종목코드를 확인해주세요.");
    } finally {
      setLoading(false);
    }
  }

  const colors = ["#00D4FF", "#00C896", "#FF6B35", "#A855F7", "#F59E0B", "#EF4444", "#10B981"];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">백테스터</h1>
        <p className="text-gray-400 mt-1">종목·기간·전략을 선택하면 성과를 즉시 비교합니다.</p>
      </div>

      {/* 설정 패널 */}
      <div className="card space-y-6">
        {/* 종목 검색 */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">종목</label>
          <div className="relative">
            <Search size={16} className="absolute left-3 top-3 text-gray-500" />
            <input
              className="w-full bg-surface border border-surface-border rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:border-brand"
              placeholder="티커 또는 종목명 검색 (예: AAPL, 005930, BTC-USD)"
              value={searchQ || (suggestions.length === 0 ? `${ticker} — ${tickerName}` : searchQ)}
              onChange={e => handleSearch(e.target.value)}
              onFocus={() => setSearchQ("")}
            />
            {suggestions.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-surface-card border border-surface-border rounded-xl overflow-hidden shadow-xl">
                {suggestions.map((s: any) => (
                  <button
                    key={s.ticker}
                    onClick={() => selectTicker(s)}
                    className="w-full px-4 py-2.5 text-left hover:bg-surface flex items-center justify-between text-sm"
                  >
                    <span className="font-mono text-brand">{s.ticker}</span>
                    <span className="text-gray-400">{s.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* 기간 선택 */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">기간</label>
          <div className="flex flex-wrap gap-2">
            {PERIODS.map(p => (
              <button
                key={p.value}
                onClick={() => setPeriod(p.value)}
                className={clsx(
                  "px-4 py-1.5 rounded-lg text-sm font-medium transition-colors",
                  period === p.value
                    ? "bg-brand text-black"
                    : "border border-surface-border text-gray-400 hover:border-brand hover:text-brand"
                )}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* 전략 선택 (최대 3개) */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">전략 선택 (최대 3개)</label>
          <div className="flex flex-wrap gap-2">
            {STRATEGIES.map((s, i) => (
              <button
                key={s.slug}
                onClick={() => toggleStrategy(s.slug)}
                className={clsx(
                  "px-4 py-1.5 rounded-lg text-sm font-medium transition-colors border",
                  selected.includes(s.slug)
                    ? "border-transparent text-black"
                    : "border-surface-border text-gray-400 hover:border-brand hover:text-brand"
                )}
                style={selected.includes(s.slug) ? { backgroundColor: colors[i] } : {}}
              >
                {s.name}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-loss text-sm">{error}</p>}

        <button onClick={runBacktest} disabled={loading} className="btn-primary w-full sm:w-auto">
          {loading ? "분석 중..." : "백테스팅 실행"}
        </button>
      </div>

      {/* 결과 */}
      {results.length > 0 && (
        <div className="space-y-6">
          {/* 성과 지표 카드 */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {results.filter(r => !r.error).map((r: any, i: number) => (
              <div key={r.strategy} className="card space-y-4 border-t-2" style={{ borderTopColor: colors[STRATEGIES.findIndex(s => s.slug === r.strategy)] }}>
                <p className="font-semibold">{STRATEGIES.find(s => s.slug === r.strategy)?.name}</p>
                <div className="grid grid-cols-2 gap-3">
                  <MetricCard label="총 수익률"   value={`${r.total_return > 0 ? "+" : ""}${r.total_return}%`} positive={r.total_return > 0} />
                  <MetricCard label="CAGR"        value={`${r.cagr > 0 ? "+" : ""}${r.cagr}%`}                positive={r.cagr > 0} />
                  <MetricCard label="샤프 비율"   value={r.sharpe.toFixed(2)} />
                  <MetricCard label="최대 낙폭"   value={`${r.max_drawdown}%`} positive={false} />
                  <MetricCard label="승률"        value={`${r.win_rate}%`}    positive={r.win_rate > 50} />
                  <MetricCard label="거래 횟수"   value={`${r.trade_count}회`} />
                </div>
              </div>
            ))}
          </div>

          {/* 누적 수익률 차트 */}
          <div className="card">
            <h2 className="font-semibold mb-4">누적 수익률 비교</h2>
            <EquityChart
              series={results.filter(r => !r.error).map((r: any, i: number) => ({
                name:  STRATEGIES.find(s => s.slug === r.strategy)?.name ?? r.strategy,
                color: colors[STRATEGIES.findIndex(s => s.slug === r.strategy)],
                data:  r.equity_curve,
              }))}
            />
          </div>
        </div>
      )}
    </div>
  );
}
