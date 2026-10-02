import { CATEGORIAS_RECLAMACAO } from '@/data'
import type { Reclamacao } from '@/types'

export interface ReclamacoesProps {
  recSuccess: boolean
  recCategoria: string
  setRecCategoria: (v: string) => void
  recNome: string
  setRecNome: (v: string) => void
  recDescricao: string
  setRecDescricao: (v: string) => void
  recFoto: string | null
  setRecFoto: (v: string | null) => void
  recFotoRef: React.RefObject<HTMLInputElement | null>
  submitReclamacao: (e: React.FormEvent) => void
  reclamacoes: Reclamacao[]
}

export default function Reclamacoes({ recSuccess, recCategoria, setRecCategoria, recNome, setRecNome, recDescricao, setRecDescricao, recFoto, setRecFoto, recFotoRef, submitReclamacao, reclamacoes }: ReclamacoesProps) {
  return (
    <>
            {/* Reclamações */}
              <div>
                <div role="status" aria-live="polite" aria-atomic="true">
                  {recSuccess && (
                    <div className="mb-4 p-4 rounded-xl flex items-center gap-2 font-semibold text-sm" style={{ background: '#EEF7F1', border: '1px solid #B8DCC5', color: '#1A5C2E' }}>
                      <span aria-hidden="true">✅</span> Reclamação salva nesta sessão de demonstração.
                    </div>
                  )}
                </div>
                <form onSubmit={submitReclamacao} className="space-y-4 mb-8">
                  {/* Category tiles */}
                  <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                    <h3 className="font-bold mb-3 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>Categoria do problema</h3>
                    <div className="grid grid-cols-3 gap-2">
                      {CATEGORIAS_RECLAMACAO.map(cat => {
                        const sel = recCategoria === cat.id
                        return (
                          <button key={cat.id} type="button" onClick={() => setRecCategoria(cat.id)}
                            className="flex flex-col items-center gap-1.5 py-3 rounded-2xl border-2 transition-all"
                            style={{
                              background: sel ? '#1E563114' : '#FAFAF7',
                              borderColor: sel ? '#1E5631' : 'var(--border)',
                            }}
                            aria-pressed={sel}>
                            <span className="text-2xl" aria-hidden="true">{cat.emoji}</span>
                            <span className="text-[10px] font-bold text-center leading-tight" style={{ color: sel ? '#1E5631' : 'var(--muted-foreground)' }}>{cat.label}</span>
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  {/* Nome */}
                  <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                    <label htmlFor="rec-nome" className="block text-sm font-semibold mb-2">Seu nome (opcional)</label>
                    <input id="rec-nome" type="text" value={recNome} onChange={e => setRecNome(e.target.value)}
                      placeholder="Deixe em branco para reclamação anônima"
                      className="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
                      style={{ borderColor: 'var(--border)', background: 'var(--background)' }} />
                  </div>

                  {/* Descrição */}
                  <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                    <label htmlFor="rec-descricao" className="block text-sm font-semibold mb-2">
                      Descrição <span style={{ color: 'var(--accent)' }} aria-hidden="true">*</span>
                      <span className="sr-only">(obrigatório)</span>
                    </label>
                    <textarea id="rec-descricao" value={recDescricao} onChange={e => setRecDescricao(e.target.value)}
                      required aria-required="true" rows={4}
                      placeholder="Descreva o problema com detalhes. Data, horário e local ajudam na investigação."
                      className="w-full px-4 py-3 rounded-xl border text-sm focus:outline-none resize-none"
                      style={{ borderColor: 'var(--border)', background: 'var(--background)' }} />
                  </div>

                  {/* Foto */}
                  <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                    <label className="block text-sm font-semibold mb-2">Foto (opcional)</label>
                    <input ref={recFotoRef} type="file" accept="image/*" className="hidden"
                      onChange={e => {
                        const file = e.target.files?.[0]
                        if (file) { const r = new FileReader(); r.onload = ev => setRecFoto(ev.target?.result as string); r.readAsDataURL(file) }
                      }} />
                    {recFoto ? (
                      <div className="relative inline-block">
                        <img src={recFoto} alt="Foto anexada" className="h-36 rounded-xl object-cover border border-[var(--border)]" />
                        <button type="button" onClick={() => setRecFoto(null)}
                          className="absolute top-1 right-1 bg-black/60 text-white rounded-full w-6 h-6 text-xs flex items-center justify-center hover:bg-black/80">✕</button>
                      </div>
                    ) : (
                      <button type="button" onClick={() => recFotoRef.current?.click()} aria-label="Anexar foto"
                        className="w-full border-2 border-dashed rounded-xl py-7 flex flex-col items-center gap-2 text-sm transition-colors"
                        style={{ borderColor: 'var(--border)', color: 'var(--muted-foreground)' }}>
                        <span className="text-3xl">📷</span>
                        <span>Clique para anexar uma foto</span>
                        <span className="text-xs opacity-60">JPG, PNG ou WEBP</span>
                      </button>
                    )}
                  </div>

                  <button type="submit" disabled={!recDescricao.trim()}
                    className="w-full py-4 rounded-2xl font-bold text-base disabled:opacity-40 disabled:cursor-not-allowed"
                    style={{ background: '#CC2C2C', color: 'white' }}>
                    Enviar reclamação →
                  </button>
                </form>

                {reclamacoes.length > 0 && (
                  <div>
                    <p className="text-xs font-bold uppercase tracking-widest mb-3" style={{ color: 'var(--muted-foreground)' }}>Reclamações desta sessão</p>
                    <div className="space-y-3">
                      {reclamacoes.map(r => {
                        const catEmoji = CATEGORIAS_RECLAMACAO.find(c => c.id === r.categoria)?.emoji ?? '💬'
                        return (
                          <div key={r.id} className="rounded-2xl p-4" style={{ background: '#fff', border: '1px solid var(--border)' }}>
                            <div className="flex items-start gap-3">
                              <span className="text-xl mt-0.5" aria-hidden="true">{catEmoji}</span>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-1">
                                  <p className="font-semibold text-sm">{r.autor}</p>
                                  <span className="text-[10px] px-2 py-0.5 rounded-full font-bold" style={{ background: '#FEF3E2', color: '#B8400A' }}>{r.categoria}</span>
                                </div>
                                <p className="text-xs mb-2" style={{ color: 'var(--muted-foreground)' }}>{r.data} às {r.horario}</p>
                                <p className="text-sm leading-relaxed">{r.descricao}</p>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
    </>
  )
}
