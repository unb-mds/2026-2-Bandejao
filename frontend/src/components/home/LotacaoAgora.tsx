import { LOTACAO_BAR, LOTACAO_HOURS, LOTACAO_INFO, MELHOR_HORARIO } from '@/data'
import type { LotacaoStats, Refeicao, RefeicaoData } from '@/types'
import { getLotacaoColor } from '@/utils'

export interface LotacaoAgoraProps {
  lotacao: LotacaoStats | null
  mealData: RefeicaoData
  mealTipo: Refeicao
  onVerLotacao: () => void
}

export default function LotacaoAgora({ lotacao, mealData, mealTipo, onVerLotacao }: LotacaoAgoraProps) {
  const lotInfo = lotacao ? LOTACAO_INFO[lotacao.predominante] : null
  const bars = LOTACAO_BAR[mealTipo]
  const hours = LOTACAO_HOURS[mealTipo]
  return (
    <>
        {/* ── LOTAÇÃO AGORA ── */}
        <div
          className="rounded-2xl overflow-hidden"
          style={{
            background: "#fff",
            border: "1px solid var(--border)",
            boxShadow: "0 1px 10px rgba(0,0,0,0.04)",
          }}
        >
          <div className="px-5 pt-4 pb-3">
            {/* Header row */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <svg
                  width="15"
                  height="15"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ color: "var(--muted-foreground)" }}
                  aria-hidden="true"
                >
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
                <p
                  className="text-xs font-bold uppercase tracking-widest"
                  style={{ color: "var(--muted-foreground)" }}
                >
                  Lotação — demonstração
                </p>
              </div>
              <button
                onClick={onVerLotacao}
                className="text-[10px] font-bold px-2.5 py-1 rounded-full transition-colors"
                style={{ background: "#EEF7F1", color: "#1E5631" }}
              >
                Ver lotação →
              </button>
            </div>

            {/* Status */}
            {lotInfo ? (
              <div className="flex items-center gap-3 mb-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-xl shrink-0"
                  style={{ background: lotInfo.bg }}
                  aria-hidden="true"
                >
                  {lotInfo.emoji}
                </div>
                <div>
                  <p
                    className="font-bold text-base"
                    style={{ color: lotInfo.color }}
                  >
                    {lotInfo.label}
                  </p>
                  {lotacao && (
                    <p
                      className="text-xs"
                      style={{ color: "var(--muted-foreground)" }}
                    >
                      {lotacao.total} reporte{lotacao.total > 1 ? "s" : ""} na
                      última hora
                    </p>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 mb-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-xl shrink-0"
                  style={{ background: "#F5F2ED" }}
                  aria-hidden="true"
                >
                  ⚪
                </div>
                <div>
                  <p
                    className="font-semibold text-sm"
                    style={{ color: "var(--muted-foreground)" }}
                  >
                    Sem dados ainda
                  </p>
                  <p
                    className="text-xs"
                    style={{ color: "var(--muted-foreground)" }}
                  >
                    Seja o primeiro a reportar
                  </p>
                </div>
              </div>
            )}

            {/* Bar chart */}
            <div>
              <p
                className="text-[9px] font-bold uppercase tracking-widest mb-2"
                style={{ color: "var(--muted-foreground)" }}
              >
                Exemplo de lotação · {mealData.label}
              </p>
              <div className="flex items-end gap-1 h-10 mb-1">
                {bars.map((pct, i) => (
                  <div
                    key={i}
                    className="flex-1 rounded-t-sm"
                    style={{
                      height: `${Math.max(pct * 0.4, 3)}px`,
                      background: getLotacaoColor(pct),
                      opacity: 0.82,
                    }}
                    aria-hidden="true"
                  />
                ))}
              </div>
              <div className="flex gap-1">
                {hours.map((h, i) => (
                  <div key={i} className="flex-1 text-center">
                    <span
                      style={{
                        fontSize: "7px",
                        color: "var(--muted-foreground)",
                        fontWeight: h ? 600 : 400,
                      }}
                    >
                      {h}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Best time strip */}
          <div
            className="px-5 py-3 flex items-center gap-2"
            style={{ background: "#F0FDF4", borderTop: "1px solid #DCFCE7" }}
          >
            <span className="text-sm" aria-hidden="true">
              💡
            </span>
            <p className="text-xs font-semibold" style={{ color: "#166534" }}>
              Exemplo de horário: <strong>{MELHOR_HORARIO[mealTipo]}</strong>
            </p>
          </div>
        </div>
    </>
  )
}
