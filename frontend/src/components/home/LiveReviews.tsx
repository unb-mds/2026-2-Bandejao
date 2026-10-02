import { useState } from 'react'
import { LiveAvaliacaoCard } from '@/components/ui'
import type { Avaliacao, RefeicaoData } from '@/types'

export interface LiveReviewsProps {
  avaliacoesHoje: Avaliacao[]
  mealData: RefeicaoData
  restauranteName: string
  mealStatus: 'agora' | 'proxima' | 'encerrado'
  onAvaliar: () => void
}

export default function LiveReviews({ avaliacoesHoje, mealData, restauranteName, mealStatus, onAvaliar }: LiveReviewsProps) {
  const [avalExpanded, setAvalExpanded] = useState(false)
  return (
    <>
        {/* ── AVALIAÇÕES EM TEMPO REAL ── */}
        <div>
          <div className="flex items-center justify-between mb-3 px-1">
            <p
              className="text-xs font-bold uppercase tracking-widest"
              style={{ color: "var(--muted-foreground)" }}
            >
              já provou? conte pra gente!
            </p>
            {mealStatus === "agora" && (
              <span
                className="text-[10px] font-bold px-2 py-0.5 rounded-full animate-pulse"
                style={{ background: "#EEF7F1", color: "#1E5631" }}
              >
                ● demonstração
              </span>
            )}
          </div>
          {avaliacoesHoje.length === 0 ? (
            <div
              className="rounded-2xl p-4 flex items-center gap-3"
              style={{
                background: "#F5F2ED",
                border: "1px solid var(--border)",
              }}
            >
              <span className="text-2xl shrink-0" aria-hidden="true">
                💬
              </span>
              <p
                className="text-sm"
                style={{ color: "var(--muted-foreground)" }}
              >
                Nenhuma avaliação desta refeição até o momento.
              </p>
            </div>
          ) : (
            <>
              <div className="space-y-3">
                {(avalExpanded
                  ? avaliacoesHoje
                  : avaliacoesHoje.slice(0, 3)
                ).map((av) => (
                  <LiveAvaliacaoCard
                    key={av.id}
                    av={av}
                    mealLabel={mealData.label}
                    restauranteName={restauranteName}
                  />
                ))}
              </div>
              {avaliacoesHoje.length > 3 && (
                <button
                  onClick={() => setAvalExpanded((v) => !v)}
                  className="w-full mt-3 py-3 rounded-2xl text-sm font-semibold transition-all active:scale-[0.98] flex items-center justify-center gap-1.5"
                  style={{
                    background: "var(--muted)",
                    color: "var(--foreground)",
                  }}
                >
                  {avalExpanded
                    ? "Mostrar menos ↑"
                    : `Ver outras ${avaliacoesHoje.length - 3} avaliações ↓`}
                </button>
              )}
            </>
          )}
          <div className="mt-3">
            <button
              onClick={onAvaliar}
              className="w-full py-3.5 rounded-2xl text-sm font-bold transition-all active:scale-[0.98] flex items-center justify-center gap-2"
              style={{
                background: "linear-gradient(135deg,#1E5631,#2D6A3F)",
                color: "#fff",
                boxShadow: "0 2px 12px rgba(30,86,49,0.25)",
              }}
            >
              <span aria-hidden="true">⭐</span> Avaliar esta refeição
            </button>
          </div>
        </div>
    </>
  )
}
