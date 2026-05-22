"use client";
import { useState, useEffect } from "react";
import { fetchRankings } from "@/lib/api";
import clsx from "clsx";
import { Trophy } from "lucide-react";

const PERIODS = ["1M","3M","6M","1Y","3Y","5Y"];
const MARKETS  = [
  { value: "us",     label: "🇺🇸 미국" },
  { value: "kr",     label: "🇰🇷 한국" },
  { value: "crypto", label: "₿ 코인" },
  { value: "all",    label: "전체" },
];

const STRATEGY_NAME: Record<string,string> = {
  "ma-crossover":   "MA 교차",
  "macd":           "MACD",
  "rsi":            "RSI",
  "bollinger-bands":"볼린저밴드",
  "momentum":       "모멘텀",
  "mean-reversion": "평균회귀",
};

export default function RankingsPage() {
  const [period,   setPeriod]   = useState("1Y");
  const [market,   setMarket]   = useState("us");
  const [rows,     setRows]     = useState<any[]>([]);
  const [loading,  setLoading]  = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchRankings(period, market)
      .then(d => setRows(d.rankings ?? []))
      .catch(() => setRows([]))
      .finally(() => setLoading(false));
  }, [period, market]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <Trophy className="text-yellow-400" /> 수익률 랭킹
        </h1>
        <p className="text-gray-400 mt-1">기간·시장별로 가장 높은 수익을 낸 전략을 확인하세요.</p>
      </div>

      {/* 필터 */}
      <div className="flex flex-wrap gap-6">
        <div className="space-y-2">
          <p className="text-sm text-gray-400 font-medium">기간</p>
          <div className="flex gap-2">
            {PERIODS.map(p => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={clsx(
                  "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                  period === p ? "bg-brand text-black" : "border border-surface-border text-gray-400 hover:text-brand hover:border-brand"
                )}
              >
                {p}
              </button>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <p className="text-sm text-gray-400 font-medium">시장</p>
          <div className="flex gap-2">
            {MARKETS.map(m => (
              <button
                key={m.value}
                onClick={() => setMarket(m.value)}
                className={clsx(
                  "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                  market === m.value ? "bg-brand text-black" : "border border-surface-border text-gray-400 hover:text-brand hover:border-brand"
                )}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 테이블 */}
      <div className="card p-0 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-surface-border text-gray-400 text-left">
              <th className="px-4 py-3 w-10">#</th>
              <th className="px-4 py-3">종목</th>
              <th className="px-4 py-3">전략</th>
              <th className="px-4 py-3 text-right">총 수익률</th>
              <th className="px-4 py-3 text-right">샤프 비율</th>
              <th className="px-4 py-3 text-right">최대 낙폭</th>
              <th className="px-4 py-3 text-right">승률</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={7} className="px-4 py-12 text-center text-gray-500">불러오는 중...</td></tr>
            ) : rows.length === 0 ? (
              <tr><td colSpan={7} className="px-4 py-12 text-center text-gray-500">데이터가 없습니다</td></tr>
            ) : (
              rows.map((r: any, i: number) => (
                <tr key={`${r.ticker}-${r.strategy}-${i}`} className="border-b border-surface-border/50 hover:bg-surface-card/50 transition-colors">
                  <td className="px-4 py-3 font-bold text-gray-500">
                    {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i + 1}
                  </td>
                  <td className="px-4 py-3 font-mono text-brand">{r.ticker}</td>
                  <td className="px-4 py-3 text-gray-300">{STRATEGY_NAME[r.strategy] ?? r.strategy}</td>
                  <td className={clsx("px-4 py-3 text-right font-semibold font-mono", r.total_return >= 0 ? "text-profit" : "text-loss")}>
                    {r.total_return >= 0 ? "+" : ""}{r.total_return}%
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-gray-300">{r.sharpe.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right font-mono text-loss">{r.max_drawdown}%</td>
                  <td className="px-4 py-3 text-right font-mono text-gray-300">{r.win_rate}%</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
