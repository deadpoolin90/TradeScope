import { fetchModel } from "@/lib/api";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle } from "lucide-react";
import { notFound } from "next/navigation";

export default async function ModelDetailPage({ params }: { params: { slug: string } }) {
  const model = await fetchModel(params.slug).catch(() => null);
  if (!model || model.error) notFound();

  return (
    <div className="max-w-3xl space-y-8">
      {/* 뒤로 가기 */}
      <Link href="/models" className="flex items-center gap-2 text-gray-400 hover:text-white text-sm transition-colors">
        <ArrowLeft size={16} /> 모델 목록으로
      </Link>

      {/* 헤더 */}
      <div className="space-y-2">
        <span className="text-brand text-sm font-medium uppercase tracking-wider">
          {model.category}
        </span>
        <h1 className="text-4xl font-bold">{model.name_ko}</h1>
        <p className="text-gray-400 text-lg">{model.name}</p>
      </div>

      {/* 설명 */}
      <div className="card space-y-3">
        <h2 className="font-semibold text-gray-300">전략 설명</h2>
        <p className="text-gray-300 leading-relaxed">{model.description}</p>
      </div>

      {/* 파라미터 */}
      {model.params?.length > 0 && (
        <div className="card space-y-4">
          <h2 className="font-semibold text-gray-300">파라미터</h2>
          <div className="space-y-2">
            {model.params.map((p: any) => (
              <div key={p.name} className="flex items-center justify-between border-b border-surface-border pb-2 last:border-0 last:pb-0">
                <div>
                  <span className="font-mono text-brand text-sm">{p.name}</span>
                  <span className="text-gray-400 text-sm ml-3">{p.desc}</span>
                </div>
                <span className="font-mono text-sm text-gray-300 bg-surface px-2 py-0.5 rounded">
                  기본값: {p.default}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 장단점 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="card space-y-3">
          <h2 className="font-semibold text-profit flex items-center gap-2">
            <CheckCircle size={16} /> 장점
          </h2>
          <ul className="space-y-2">
            {model.pros?.map((p: string) => (
              <li key={p} className="text-gray-300 text-sm flex items-start gap-2">
                <span className="text-profit mt-0.5">•</span> {p}
              </li>
            ))}
          </ul>
        </div>
        <div className="card space-y-3">
          <h2 className="font-semibold text-loss flex items-center gap-2">
            <XCircle size={16} /> 단점
          </h2>
          <ul className="space-y-2">
            {model.cons?.map((c: string) => (
              <li key={c} className="text-gray-300 text-sm flex items-start gap-2">
                <span className="text-loss mt-0.5">•</span> {c}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 적합한 시장 */}
      {model.best_market && (
        <div className="card flex items-center gap-3">
          <span className="text-2xl">✅</span>
          <div>
            <p className="text-sm text-gray-400">가장 효과적인 시장</p>
            <p className="font-semibold">{model.best_market}</p>
          </div>
        </div>
      )}

      {/* 바로 백테스팅 */}
      <Link
        href={`/backtest?strategy=${params.slug}`}
        className="btn-primary inline-flex items-center gap-2"
      >
        이 전략으로 백테스팅하기 →
      </Link>
    </div>
  );
}
