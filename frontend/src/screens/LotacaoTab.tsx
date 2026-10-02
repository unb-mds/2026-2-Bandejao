import LotacaoTimeline from "@/components/LotacaoTimeline";
import type { Campus, LotacaoStats, NivelLotacao, Refeicao } from '@/types'

export interface LotacaoTabProps {
  campus: Campus
  currentLotacao: LotacaoStats | null
  lotacaoLabel: string
  lotacaoEmoji: string
  lotacaoColor: string
  lotacaoEnviada: boolean
  lotacaoNivel: NivelLotacao | null
  setLotacaoNivel: (n: NivelLotacao) => void
  reportarLotacao: () => void
  getLotacaoStats: (campusName: string) => LotacaoStats | null
}

export default function LotacaoTab({ campus, currentLotacao, lotacaoLabel, lotacaoEmoji, lotacaoColor, lotacaoEnviada, lotacaoNivel, setLotacaoNivel, reportarLotacao }: LotacaoTabProps) {
  return (
          <div id="panel-lotacao" role="tabpanel" aria-labelledby="tab-lotacao" className="max-w-2xl mx-auto px-4 pt-5 pb-8 space-y-5">
            <div>
              <h2 className="text-2xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>Lotação</h2>
              <p className="text-sm" style={{ color: 'var(--muted-foreground)' }}>Demonstração com relatos desta sessão e exemplos de movimento, sem estimativa real.</p>
            </div>

            {/* Status atual */}
            <div className="rounded-2xl overflow-hidden" style={{ background: '#fff', border: '1px solid var(--border)', boxShadow: '0 1px 12px rgba(0,0,0,0.05)' }}>
              <div className="px-5 pt-5 pb-4">
                <p className="text-xs font-bold uppercase tracking-widest mb-1" style={{ color: 'var(--muted-foreground)' }}>
                  {campus.name}
                </p>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shrink-0"
                    style={{ background: currentLotacao ? `${lotacaoColor}18` : '#F5F2ED' }}>
                    {currentLotacao ? lotacaoEmoji : '⚪'}
                  </div>
                  <div>
                    <p className="font-bold text-lg" style={{ color: currentLotacao ? lotacaoColor : 'var(--muted-foreground)' }}>
                      {currentLotacao ? lotacaoLabel : 'Sem dados ainda'}
                    </p>
                    {currentLotacao && (
                      <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
                        Baseado em {currentLotacao.total} reporte{currentLotacao.total > 1 ? 's' : ''} na última hora
                      </p>
                    )}
                  </div>
                </div>
                {currentLotacao && (
                  <div className="mt-4 flex gap-1.5 h-2 rounded-full overflow-hidden" style={{ background: 'var(--muted)' }}>
                    {currentLotacao.counts.vazio > 0 && <div className="bg-green-400" style={{ width: `${(currentLotacao.counts.vazio/currentLotacao.total)*100}%` }} />}
                    {currentLotacao.counts.moderado > 0 && <div className="bg-yellow-400" style={{ width: `${(currentLotacao.counts.moderado/currentLotacao.total)*100}%` }} />}
                    {currentLotacao.counts.cheio > 0 && <div className="bg-red-400" style={{ width: `${(currentLotacao.counts.cheio/currentLotacao.total)*100}%` }} />}
                  </div>
                )}
              </div>

              {/* Report */}
              <div style={{ borderTop: '1px solid var(--border)', background: '#FAFAF7' }} className="px-5 py-4">
                <p className="text-sm font-semibold mb-3">Como está o movimento agora?</p>
                <div role="status" aria-live="polite" aria-atomic="true">
                  {lotacaoEnviada && (
                    <div className="flex items-center gap-2 py-3 px-4 rounded-xl mb-3" style={{ background: '#EEF7F1', color: '#1E5631' }}>
                      <span aria-hidden="true">✅</span>
                      <p className="font-semibold text-sm">Obrigado pelo reporte!</p>
                    </div>
                  )}
                </div>
                {!lotacaoEnviada && (
                  <div className="space-y-3">
                    <div className="grid grid-cols-3 gap-2">
                      {([
                        { nivel: 'vazio' as const, label: 'Tranquilo', emoji: '🟢', desc: 'Sem fila' },
                        { nivel: 'moderado' as const, label: 'Moderado', emoji: '🟡', desc: 'Fila curta' },
                        { nivel: 'cheio' as const, label: 'Cheio', emoji: '🔴', desc: 'Fila grande' },
                      ]).map(({ nivel, label, emoji, desc }) => {
                        const sel = lotacaoNivel === nivel
                        const colors: Record<string, string> = { vazio: '#22C55E', moderado: '#F59E0B', cheio: '#EF4444' }
                        return (
                          <button key={nivel} type="button" aria-pressed={sel} onClick={() => setLotacaoNivel(nivel)}
                            className="flex flex-col items-center gap-1 py-3.5 rounded-2xl border-2 font-semibold text-sm transition-all"
                            style={{
                              background: sel ? `${colors[nivel]}10` : '#fff',
                              borderColor: sel ? colors[nivel] : 'var(--border)',
                              color: sel ? colors[nivel] : 'var(--foreground)',
                            }}>
                            <span className="text-2xl" aria-hidden="true">{emoji}</span>
                            <span className="text-xs font-bold">{label}</span>
                            <span className="text-[10px] font-normal" style={{ color: 'var(--muted-foreground)' }}>{desc}</span>
                          </button>
                        )
                      })}
                    </div>
                    <button type="button" onClick={reportarLotacao} disabled={!lotacaoNivel}
                      className="w-full py-3 rounded-xl font-bold text-sm disabled:opacity-40 disabled:cursor-not-allowed transition-opacity"
                      style={{ background: 'var(--primary)', color: 'white' }}>
                      Enviar reporte →
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Timelines por refeição */}
            {(['cafe','almoco','jantar'] as Refeicao[]).map(tipo => {
              const labels: Record<Refeicao, string> = { cafe: '☕ Café da Manhã', almoco: '🍽️ Almoço', jantar: '🌙 Jantar' }
              return (
                <div key={tipo} className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                  <p className="text-xs font-bold uppercase tracking-widest mb-3" style={{ color: 'var(--muted-foreground)' }}>
                    Padrão de movimento
                  </p>
                  <p className="font-semibold text-sm mb-4">{labels[tipo]}</p>
                  <LotacaoTimeline tipo={tipo} />
                </div>
              )
            })}
          </div>
  )
}