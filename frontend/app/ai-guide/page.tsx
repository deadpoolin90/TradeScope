import { Cpu, TrendingUp, Shield, Zap } from "lucide-react";
import Link from "next/link";

const RECOMMENDATIONS = [
  {
    market: "🇺🇸 미국 주식",
    top: "XGBoost + 모멘텀 앙상블",
    reason: "대형주는 데이터가 풍부해 ML 모델이 패턴을 잘 포착합니다. 모멘텀은 5년 이상 검증된 팩터입니다.",
    strategies: ["xgboost", "momentum", "macd"],
  },
  {
    market: "🇰🇷 한국 주식",
    top: "MACD + RSI 조합",
    reason: "한국 시장은 개인 투자자 비중이 높아 기술적 지표의 자기실현이 더 강하게 나타납니다.",
    strategies: ["macd", "rsi", "bollinger-bands"],
  },
  {
    market: "₿ 암호화폐",
    top: "볼린저밴드 + LSTM",
    reason: "암호화폐는 변동성이 크고 24시간 거래됩니다. 변동성 기반 볼린저밴드와 LSTM의 패턴 학습이 유효합니다.",
    strategies: ["bollinger-bands", "lstm", "momentum"],
  },
];

const AI_REASONS = [
  { icon: TrendingUp, title: "비선형 패턴 포착", desc: "전통 기술 지표는 선형적 가정에 기반합니다. ML 모델은 복잡한 비선형 관계를 학습할 수 있습니다." },
  { icon: Zap,        title: "멀티 피처 통합",   desc: "가격·거래량·거시지표·감성분석 등 수십 개의 피처를 동시에 처리해 더 정교한 판단을 내립니다." },
  { icon: Shield,     title: "적응적 학습",       desc: "시장 구조가 변하면 재학습을 통해 전략도 진화할 수 있습니다. 고정된 규칙 기반 전략의 한계를 극복합니다." },
  { icon: Cpu,        title: "LLM 감성분석 결합", desc: "GPT 기반 뉴스·공시·소셜미디어 감성 분석을 기술 지표와 결합하면 단독 모델 대비 Sharpe가 향상됩니다." },
];

export default function AIGuidePage() {
  return (
    <div className="space-y-12 max-w-4xl">
      {/* 헤더 */}
      <div className="space-y-3">
        <div className="inline-flex items-center gap-2 border border-brand/30 text-brand text-sm px-4 py-1.5 rounded-full bg-brand/5">
          <Cpu size={14} /> AI 시대 트레이딩 가이드
        </div>
        <h1 className="text-3xl font-bold">지금은 어떤 모델을 써야 할까?</h1>
        <p className="text-gray-400 leading-relaxed">
          2020년대 이후 AI·ML 기반 트레이딩이 헤지펀드·퀀트 하우스를 지배하고 있습니다.
          단순 기술 지표만으로는 알파(초과수익)를 유지하기 어려워졌습니다.
          데이터로 확인한 AI 시대의 최적 전략을 소개합니다.
        </p>
      </div>

      {/* AI가 우세한 이유 */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold">왜 AI 모델이 우세한가?</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {AI_REASONS.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card space-y-3">
              <div className="w-9 h-9 rounded-lg bg-brand/10 flex items-center justify-center text-brand">
                <Icon size={18} />
              </div>
              <h3 className="font-semibold">{title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 시장별 추천 */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold">시장별 추천 전략</h2>
        <div className="space-y-4">
          {RECOMMENDATIONS.map((rec) => (
            <div key={rec.market} className="card space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-lg font-semibold">{rec.market}</p>
                  <p className="text-brand font-medium mt-1">추천: {rec.top}</p>
                </div>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">{rec.reason}</p>
              <div className="flex gap-2">
                {rec.strategies.map(s => (
                  <Link
                    key={s}
                    href={`/backtest?strategy=${s}`}
                    className="text-xs border border-surface-border px-3 py-1 rounded-lg text-gray-400 hover:text-brand hover:border-brand transition-colors"
                  >
                    {s} 백테스팅 →
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 결론 */}
      <section className="card border-brand/30 bg-brand/5 space-y-3">
        <h2 className="text-xl font-bold text-brand">핵심 결론</h2>
        <ul className="space-y-2 text-gray-300 text-sm leading-relaxed">
          <li>• <strong>단독 기술 지표</strong>만으로는 장기적으로 시장 대비 초과수익을 내기 어렵습니다.</li>
          <li>• <strong>XGBoost, LSTM</strong> 등 ML 모델은 충분한 데이터가 있을 때 기술 지표 대비 Sharpe를 30~50% 향상시킵니다.</li>
          <li>• <strong>앙상블 접근</strong>(ML + 모멘텀 + 기술 지표 조합)이 단일 모델보다 낙폭이 작고 안정적입니다.</li>
          <li>• 단, 과적합 위험이 있으므로 반드시 <strong>워크포워드 테스트</strong>로 검증해야 합니다.</li>
        </ul>
      </section>

      <Link href="/backtest" className="btn-primary inline-flex items-center gap-2">
        직접 백테스팅으로 확인하기 →
      </Link>
    </div>
  );
}
