import { AvaliacaoCard } from '@/components/ui'
import type { Avaliacao, Tab } from '@/types'

export interface AvaliacaoHistoricoProps {
  avaliacoes: Avaliacao[]
  mediaGeral: string
  setTab: (t: Tab) => void
}

export default function AvaliacaoHistorico({ avaliacoes, mediaGeral, setTab }: AvaliacaoHistoricoProps) {
  return (
    <>
            {/* ── Histórico ── */}
              <div className="space-y-4">
                {avaliacoes.length === 0 ? (
                  <div className="text-center py-16" style={{ color: 'var(--muted-foreground)' }}>
                    <span className="text-5xl block mb-4">📭</span>
                    <p className="font-semibold">Nenhuma avaliação ainda.</p>
                    <p className="text-sm">Seja o primeiro a avaliar o bandejão hoje!</p>
                    <button onClick={() => setTab('avaliar')} className="mt-4 px-5 py-2.5 rounded-xl font-semibold text-sm text-white" style={{ background: 'var(--primary)' }}>
                      Avaliar agora
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="flex items-center gap-4 p-4 rounded-2xl" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                      <p className="text-4xl font-bold" style={{ fontFamily: "'Playfair Display', serif", color: '#1E5631' }}>{mediaGeral}</p>
                      <div className="flex-1">
                        <p className="text-sm font-semibold">Média geral</p>
                        <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>{avaliacoes.length} avaliações</p>
                        <div className="flex gap-0.5 mt-1">
                          {[1,2,3,4,5].map(s => (
                            <span key={s} className="text-base" style={{ color: s <= Math.round(Number(mediaGeral)) ? '#E8570A' : '#D5CFC5' }}>★</span>
                          ))}
                        </div>
                      </div>
                    </div>
                    {(() => {
                      // Group by date, then by refeicao within each date
                      const byDate: Record<string, Record<string, typeof avaliacoes>> = {}
                      avaliacoes.forEach(av => {
                        if (!byDate[av.data]) byDate[av.data] = {}
                        if (!byDate[av.data][av.refeicao]) byDate[av.data][av.refeicao] = []
                        byDate[av.data][av.refeicao].push(av)
                      })
                      const MEAL_ORDER = ['Café da Manhã', 'Almoço', 'Jantar']
                      return Object.entries(byDate).map(([data, porRefeicao]) => (
                        <div key={data} className="space-y-3">
                          <p className="text-xs font-bold uppercase tracking-widest px-1 pt-2" style={{ color: 'var(--muted-foreground)' }}>
                            {data}
                          </p>
                          {MEAL_ORDER.filter(r => porRefeicao[r]).map(refeicao => (
                            <div key={refeicao} className="space-y-2">
                              <div className="flex items-center gap-2 px-1">
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider" style={{ background: '#EEF7F1', color: '#1E5631' }}>
                                  {refeicao === 'Café da Manhã' ? '☕' : refeicao === 'Almoço' ? '🍽️' : '🌙'} {refeicao}
                                </span>
                                <span className="text-[10px]" style={{ color: 'var(--muted-foreground)' }}>{porRefeicao[refeicao].length} aval.</span>
                              </div>
                              {porRefeicao[refeicao].map(av => <AvaliacaoCard key={av.id} av={av} />)}
                            </div>
                          ))}
                        </div>
                      ))
                    })()}
                  </>
                )}
              </div>
    </>
  )
}
