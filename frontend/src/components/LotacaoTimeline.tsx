import { LOTACAO_TIMELINE } from '@/data'
import type { Refeicao } from '@/types'
import { getLotacaoColorClass } from '@/utils'

export interface LotacaoTimelineProps {
  tipo: Refeicao
}

export default function LotacaoTimeline({ tipo }: LotacaoTimelineProps) {
  // Lotação timeline
    const timeline = LOTACAO_TIMELINE[tipo]
    const quietSlot = [...timeline].sort((a, b) => a.pct - b.pct)[0]
    return (
      <div>
        <div className="flex items-end gap-1.5 h-16 mb-1">
          {timeline.map(({ hora, pct }) => (
            <div key={hora} className="flex-1 flex flex-col items-center gap-0.5">
              <div className="w-full rounded-t-sm transition-all"
                style={{ height: `${Math.max(pct * 0.56, 4)}px`, background: getLotacaoColorClass(pct), opacity: 0.85 }} />
            </div>
          ))}
        </div>
        <div className="flex gap-1.5">
          {timeline.map(({ hora }) => (
            <div key={hora} className="flex-1 text-center">
              <span className="text-[8px] text-[var(--muted-foreground)]">{hora}</span>
            </div>
          ))}
        </div>
        <p className="text-xs text-[var(--muted-foreground)] mt-3 flex items-center gap-1.5">
          <span style={{ color: '#22C55E' }}>●</span>
          Horário mais tranquilo estimado: <strong className="text-[var(--foreground)]">{quietSlot.hora}</strong>
        </p>
      </div>
    )
}
