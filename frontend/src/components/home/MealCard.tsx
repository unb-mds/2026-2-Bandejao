import { MEAL_COLORS, MEAL_ICONS } from '@/data'
import type { Refeicao, RefeicaoData } from '@/types'
import { iNome } from '@/utils'
import { CATEGORIAS, DIETAS } from '@/cardapios'

export interface MealCardProps {
  mealTipo: Refeicao
  mealStatus: 'agora' | 'proxima' | 'encerrado'
  mealData: RefeicaoData
  onVerCardapio: () => void
}

export default function MealCard({ mealTipo, mealStatus, mealData, onVerCardapio }: MealCardProps) {
  const mealColors = MEAL_COLORS[mealTipo]

  const statusLabel =
    mealStatus === "agora"
      ? "Refeição do período"
      : mealStatus === "proxima"
        ? "Próxima refeição"
        : "Refeição da noite"

  const statusColor =
    mealStatus === "agora" ? "rgba(201,168,76,0.9)" : "rgba(255,255,255,0.45)"

  return (
    <>
        {/* ── CARD PRINCIPAL — refeição de agora ── */}
        <div
          className="rounded-3xl overflow-hidden"
          style={{ boxShadow: "0 8px 32px rgba(30,86,49,0.18)" }}
        >
          {/* Colored header band */}
          <div
            className="relative px-5 pt-5 pb-0"
            style={{
              background: `linear-gradient(135deg, ${mealColors.from} 0%, ${mealColors.to} 100%)`,
            }}
          >
            {/* Ghost watermark */}
            <div
              aria-hidden="true"
              style={{
                position: "absolute",
                right: "-0.5rem",
                bottom: "-1.5rem",
                fontSize: "9rem",
                lineHeight: 1,
                opacity: 0.06,
                pointerEvents: "none",
                userSelect: "none",
              }}
            >
              {MEAL_ICONS[mealTipo]}
            </div>

            {/* Status badge */}
            <div className="flex items-center gap-2 mb-3">
              <span
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[9px] font-bold tracking-widest uppercase"
                style={{
                  background: "rgba(255,255,255,0.12)",
                  color: statusColor,
                }}
              >
                <span
                  className="w-1.5 h-1.5 rounded-full inline-block"
                  style={{
                    background: statusColor,
                    boxShadow:
                      mealStatus === "agora"
                        ? `0 0 6px ${statusColor}`
                        : "none",
                  }}
                  aria-hidden="true"
                />
                {statusLabel}
              </span>
            </div>

            {/* Meal label + time */}
            <div className="flex items-start justify-between mb-2">
              <div>
                <p
                  className="text-xs font-bold uppercase tracking-widest mb-1"
                  style={{ color: "rgba(255,255,255,0.55)" }}
                >
                  {mealData.label}
                </p>
                <p
                  className="text-white font-bold text-2xl leading-tight"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  {iNome(mealData.prato_principal)}
                </p>
              </div>
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl shrink-0 ml-3"
                style={{ background: "rgba(255,255,255,0.12)" }}
                aria-hidden="true"
              >
                {MEAL_ICONS[mealTipo]}
              </div>
            </div>

            {/* Time */}
            <div className="flex items-center gap-1.5 pb-4">
              <svg
                width="12"
                height="12"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                style={{ color: "rgba(255,255,255,0.4)" }}
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span
                className="text-xs font-semibold"
                style={{ color: "rgba(255,255,255,0.55)" }}
              >
                {mealData.horario}
              </span>
            </div>
          </div>

          {/* Resumo dos itens publicados; o cardápio completo preserva todas as categorias. */}
          <div className="bg-card px-5 py-2">
            {[...new Set((mealData.itensApi ?? []).map(item => item.categoria))].slice(0, 3).map(categoria => (
              <div key={categoria} className="py-3 border-b border-border last:border-0">
                <p className="text-[9px] font-bold uppercase tracking-widest text-primary mb-1">{CATEGORIAS[categoria] ?? categoria}</p>
                {(mealData.itensApi ?? []).filter(item => item.categoria === categoria).map(item => (
                  <p key={item.id} className="text-sm font-semibold text-foreground">{item.nome} <span className="text-xs font-normal text-muted-foreground">· {DIETAS[item.tipo_dieta] ?? item.tipo_dieta}</span></p>
                ))}
              </div>
            ))}
          </div>

          {/* CTA */}
          <button
            onClick={onVerCardapio}
            className="w-full flex items-center justify-between px-5 py-4 font-semibold text-sm transition-opacity hover:opacity-90"
            style={{ background: "#1E5631", color: "#fff" }}
          >
            <span>Ver cardápio completo</span>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </div>
    </>
  )
}
