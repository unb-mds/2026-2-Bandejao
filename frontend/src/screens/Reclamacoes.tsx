import { CATEGORIAS_RECLAMACAO } from '@/data'
import type { CardapioRefeicoes, Refeicao } from '@/types'
import { temRefeicao } from '@/utils'

export interface ReclamacoesProps {
  cardapioDia: CardapioRefeicoes
  refeicao: Refeicao
  setRefeicao: (refeicao: Refeicao) => void
  recCategoria: string
  setRecCategoria: (v: string) => void
  recDescricao: string
  setRecDescricao: (v: string) => void
  recSuccess: boolean
  recErro: string
  recEnviando: boolean
  submitReclamacao: (e: React.FormEvent) => void | Promise<void>
}

export default function Reclamacoes({
  cardapioDia,
  refeicao,
  setRefeicao,
  recCategoria,
  setRecCategoria,
  recDescricao,
  setRecDescricao,
  recSuccess,
  recErro,
  recEnviando,
  submitReclamacao,
}: ReclamacoesProps) {
  const cardapioAtual = cardapioDia[refeicao]
  const refeicaoDisponivel = temRefeicao(cardapioAtual)

  return (
    <>
      <div className="mb-5">
        <h2 className="text-2xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>
          Registrar reclamação
        </h2>
        <p className="text-sm" style={{ color: 'var(--muted-foreground)' }}>
          A reclamação fica vinculada a esta refeição, sem precisar de uma avaliação por nota.
        </p>
      </div>

      <div role="status" aria-live="polite" aria-atomic="true">
        {recSuccess && (
          <div className="mb-5 p-4 rounded-xl flex items-center gap-2 font-semibold text-sm" style={{ background: '#EEF7F1', border: '1px solid #B8DCC5', color: '#1A5C2E' }}>
            <span aria-hidden="true">✅</span> Reclamação registrada. Ela não fica visível para outras pessoas nem gera encaminhamento automático ao RU.
          </div>
        )}
        {recErro && (
          <div className="mb-5 p-4 rounded-xl text-sm" role="alert" style={{ background: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B' }}>
            {recErro}
          </div>
        )}
      </div>

      <form onSubmit={submitReclamacao} className="space-y-4">
        <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
          <h3 className="font-bold mb-3 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>
            Qual refeição?
          </h3>
          <div className="flex gap-2">
            {(['cafe', 'almoco', 'jantar'] as Refeicao[]).map(opcao => (
              <button
                key={opcao}
                type="button"
                onClick={() => setRefeicao(opcao)}
                aria-pressed={refeicao === opcao}
                className="flex-1 py-2.5 rounded-xl text-sm font-semibold border transition-all"
                style={{
                  background: refeicao === opcao ? '#1E5631' : '#fff',
                  color: refeicao === opcao ? '#fff' : 'var(--foreground)',
                  borderColor: refeicao === opcao ? '#1E5631' : 'var(--border)',
                }}
              >
                {cardapioDia[opcao].label}
              </button>
            ))}
          </div>
        </div>

        {!refeicaoDisponivel ? (
          <div className="rounded-2xl p-6 text-center border space-y-2" style={{ background: '#FFFBEB', borderColor: '#FDE68A', color: '#92400E' }}>
            <span className="text-3xl block" aria-hidden="true">🔒</span>
            <h3 className="font-bold text-base">Refeição indisponível</h3>
            <p className="text-xs leading-relaxed max-w-sm mx-auto" style={{ color: '#B45309' }}>
              Não há {cardapioAtual.label.toLowerCase()} cadastrado nesta data para o campus selecionado.
            </p>
          </div>
        ) : (
          <>
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <h3 className="font-bold mb-3 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>Categoria do problema</h3>
              <div className="grid grid-cols-4 gap-2">
                {CATEGORIAS_RECLAMACAO.map(cat => {
                  const sel = recCategoria === cat.id
                  return (
                    <button key={cat.id} type="button" onClick={() => setRecCategoria(cat.id)}
                      aria-pressed={sel}
                      className="flex flex-col items-center gap-1.5 py-3 rounded-2xl border-2 transition-all"
                      style={{
                        background: sel ? '#1E563114' : '#FAFAF7',
                        borderColor: sel ? '#1E5631' : 'var(--border)',
                      }}>
                      <span className="text-2xl" aria-hidden="true">{cat.emoji}</span>
                      <span className="text-[10px] font-bold text-center leading-tight" style={{ color: sel ? '#1E5631' : 'var(--muted-foreground)' }}>{cat.label}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <label htmlFor="rec-descricao" className="block text-sm font-semibold mb-2">
                Descrição <span style={{ color: 'var(--accent)' }} aria-hidden="true">*</span>
                <span className="sr-only">(obrigatório)</span>
              </label>
              <textarea id="rec-descricao" value={recDescricao} onChange={e => setRecDescricao(e.target.value)}
                required aria-required="true" rows={4} maxLength={1000}
                placeholder="Descreva o problema com detalhes. Data, horário e local ajudam na investigação."
                className="w-full px-4 py-3 rounded-xl border text-sm focus:outline-none resize-none"
                style={{ borderColor: 'var(--border)', background: 'var(--background)' }} />
              <p className="mt-1 text-right text-xs" style={{ color: 'var(--muted-foreground)' }}>
                {recDescricao.length}/1000
              </p>
            </div>

            <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
              O formulário não pede nome nem foto, e a reclamação não aparece numa lista pública. O prazo de envio é o mesmo da avaliação: do início do serviço até antes de 00h do dia seguinte, no fuso de Brasília.
            </p>

            <button type="submit" disabled={recEnviando || !recDescricao.trim()}
              className="w-full py-4 rounded-2xl font-bold text-base disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              style={{ background: '#CC2C2C', color: 'white' }}>
              {recEnviando ? 'Enviando…' : 'Enviar reclamação →'}
            </button>
          </>
        )}
      </form>
    </>
  )
}
