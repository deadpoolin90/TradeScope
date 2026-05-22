import Link from "next/link";
import { TrendingUp, BarChart2, Trophy, Cpu, ArrowRight } from "lucide-react";

const FEATURES = [
  { icon: BarChart2, title: "15+ 트레이딩 모델", desc: "MA, MACD, RSI, 볼린저밴드부터 LSTM, XGBoost까지 주요 전략을 한 곳에서 비교합니다.", href: "/models" },
  { icon: TrendingUp, title: "백테스터", desc: "원하는 종목과 기간을 설정해 모델별 수익률·샤프비율·낙폭을 즉시 비교하세요.", href: "/backtest" },
  { icon: Trophy, title: "수익률 랭킹", desc: "기간별·시장별로 가장 높은 수익을 낸 모델이 무엇인지 실시간으로 확인합니다.", href: "/rankings" },
  { icon: Cpu, title: "AI 시대 가이드", desc: "현재 AI 트레이딩 시대에 어떤 모델이 우세한지, 왜 그런지 데이터로 설명합니다.", href: "/ai-guide" },
];

const MARKETS = [
  { label: "🇺🇸 미국 주식", desc: "AAPL, MSFT, NVDA 등 NASDAQ / NYSE" },
  { label: "🇰🇷 한국 주식", desc: "삼성전자, SK하이닉스, NAVER 등 KRX" },
  { label: "₿  암호화폐",   desc: "Bitcoin, Ethereum, Solana 등" },
];

export default function HomePage() {
  return (
    <div className="space-y-20">
      {/* 히어로 */}
      <section className="text-center py-20 space-y-6">
        <div className="inline-flex items-center gap-2 border border-brand/30 text-brand text-sm px-4 py-1.5 rounded-full bg-brand/5">
          <Cpu size={14} /> AI 시대 트레이딩 모델 비교 플랫폼
        </div>
        <h1 className="text-5xl sm:text-6xl font-bold tracking-tight">
          어떤 전략이<br />
          <span className="text-brand">실제로 수익</span>을 냈을까?
        </h1>
        <p className="text-gray-400 text-lg max-w-xl mx-auto">
          15개 이상의 트레이딩 모델을 직접 백테스팅하고 비교하세요.
          한국·미국·암호화폐 시장 모두 지원합니다.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/backtest" className="btn-primary flex items-center gap-2">
            지금 백테스팅 <ArrowRight size={16} />
          </Link>
          <Link href="/models" className="btn-ghost">모델 둘러보기</Link>
        </div>
      </section>

      {/* 지원 시장 */}
      <section>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {MARKETS.map((m) => (
            <div key={m.label} className="card text-center space-y-1">
              <p className="text-xl font-semibold">{m.label}</p>
              <p className="text-gray-400 text-sm">{m.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 기능 카드 */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold">주요 기능</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {FEATURES.map(({ icon: Icon, title, desc, href }) => (
            <Link key={href} href={href} className="card group hover:border-brand/50 transition-colors space-y-3">
              <div className="w-10 h-10 rounded-xl bg-brand/10 flex items-center justify-center text-brand">
                <Icon size={20} />
              </div>
              <h3 className="font-semibold text-lg group-hover:text-brand transition-colors">{title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{desc}</p>
              <span className="text-brand text-sm flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                바로가기 <ArrowRight size={14} />
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
