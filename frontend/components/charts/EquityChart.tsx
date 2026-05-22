"use client";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { useMemo } from "react";

interface Series {
  name:  string;
  color: string;
  data:  { date: string; value: number }[];
}

export default function EquityChart({ series }: { series: Series[] }) {
  // 모든 날짜를 합쳐 공통 x축 생성
  const merged = useMemo(() => {
    const dateMap: Record<string, any> = {};
    for (const s of series) {
      for (const pt of s.data) {
        if (!dateMap[pt.date]) dateMap[pt.date] = { date: pt.date };
        dateMap[pt.date][s.name] = +((pt.value - 1) * 100).toFixed(2);  // % 변환
      }
    }
    return Object.values(dateMap).sort((a, b) => a.date.localeCompare(b.date));
  }, [series]);

  return (
    <ResponsiveContainer width="100%" height={340}>
      <LineChart data={merged}>
        <XAxis
          dataKey="date"
          tick={{ fill: "#6b7280", fontSize: 11 }}
          tickFormatter={d => d.slice(0, 7)}
          interval="preserveStartEnd"
        />
        <YAxis
          tick={{ fill: "#6b7280", fontSize: 11 }}
          tickFormatter={v => `${v > 0 ? "+" : ""}${v}%`}
          width={60}
        />
        <Tooltip
          contentStyle={{ background: "#1A1D27", border: "1px solid #2A2D3E", borderRadius: 12 }}
          labelStyle={{ color: "#9ca3af", marginBottom: 4 }}
          formatter={(v: any) => [`${v > 0 ? "+" : ""}${v}%`]}
        />
        <Legend wrapperStyle={{ paddingTop: 16 }} />
        {series.map(s => (
          <Line
            key={s.name}
            type="monotone"
            dataKey={s.name}
            stroke={s.color}
            dot={false}
            strokeWidth={2}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
