"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { TrendingUp } from "lucide-react";

const NAV = [
  { href: "/",          label: "홈"        },
  { href: "/models",    label: "모델 목록"  },
  { href: "/backtest",  label: "백테스터"   },
  { href: "/rankings",  label: "랭킹"       },
  { href: "/ai-guide",  label: "AI 가이드"  },
];

export default function Navbar() {
  const path = usePathname();
  return (
    <nav className="border-b border-surface-border bg-surface/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center gap-8 h-16">
        {/* 로고 */}
        <Link href="/" className="flex items-center gap-2 font-bold text-lg text-brand shrink-0">
          <TrendingUp size={22} />
          TradeScope
        </Link>

        {/* 메뉴 */}
        <div className="flex items-center gap-1">
          {NAV.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                path === href
                  ? "text-brand bg-brand/10"
                  : "text-gray-400 hover:text-white hover:bg-surface-card"
              )}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
