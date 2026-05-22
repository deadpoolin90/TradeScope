import Link from "next/link";
import { fetchModels } from "@/lib/api";
import { ArrowRight } from "lucide-react";

const CATEGORY_LABEL: Record<string, string> = {
  technical: "📊 기술적 분석",
  quant:     "🔢 퀀트 전략",
  ml:        "🤖 AI / ML",
};

export default async function ModelsPage() {
  const data = await fetchModels().catch(() => ({ models: [] }));
  const models = data.models ?? [];

  // 카테고리별 분류
  const grouped = models.reduce((acc: Record<string, typeof models>, m: any) => {
    const cat = m.category ?? "technical";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(m);
    return acc;
  }, {});

  return (
    <div className="space-y-12">
      <div>
        <h1 className="text-3xl font-bold">트레이딩 모델 목록</h1>
        <p className="text-gray-400 mt-2">각 모델의 원리, 장단점, 적합한 시장 환경을 확인하세요.</p>
      </div>

      {Object.entries(grouped).map(([cat, catModels]: any) => (
        <section key={cat} className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-300">
            {CATEGORY_LABEL[cat] ?? cat}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {catModels.map((m: any) => (
              <Link
                key={m.slug}
                href={`/models/${m.slug}`}
                className="card group hover:border-brand/50 transition-colors space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-lg group-hover:text-brand transition-colors">
                      {m.name_ko}
                    </p>
                    <p className="text-gray-500 text-sm">{m.name}</p>
                  </div>
                  <ArrowRight size={16} className="text-gray-600 group-hover:text-brand transition-colors mt-1" />
                </div>
                <p className="text-gray-400 text-sm leading-relaxed line-clamp-3">
                  {m.description}
                </p>
                {m.best_market && (
                  <span className="inline-block text-xs border border-surface-border text-gray-400 px-2 py-1 rounded-lg">
                    ✅ {m.best_market}
                  </span>
                )}
              </Link>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
