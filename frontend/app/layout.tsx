import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/ui/Navbar";

export const metadata: Metadata = {
  title: "TradeScope — 트레이딩 모델 비교 분석",
  description: "MA, MACD, RSI, 볼린저밴드, LSTM, XGBoost 등 주요 트레이딩 모델의 백테스팅 결과를 종목·기간별로 비교합니다.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className="dark">
      <body className="bg-surface text-white min-h-screen font-sans antialiased">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
