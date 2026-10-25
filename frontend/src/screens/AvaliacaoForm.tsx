import { StarRating } from '@/components/ui'
import type { CardapioRefeicoes, Refeicao, RefeicaoData } from '@/types'

export interface AvaliacaoFormProps {
  cardapioDia: CardapioRefeicoes
  refeicao: Refeicao
  setRefeicao: (refeicao: Refeicao) => void
  avGeral: number
  setAvGeral: (valor: number) => void
  avComentario: string
  setAvComentario: (valor: string) => void
  avSuccess: boolean
  avErro: string
  avEnviando: boolean
  submitAvaliacao: (evento: React.FormEvent) => void | Promise<void>
}

function temRefeicao(refeicao: RefeicaoData | undefined | null): boolean {
  if (!refeicao?.id) return false
  if (refeicao.itensApi) return refeicao.itensApi.length > 0
  const prato = refeicao.prato_principal
  if (prato === '—') return false
  return !(typeof prato === 'object' && prato?.nome === '—')
}

export default function AvaliacaoForm({
  cardapioDia,
  refeicao,
  setRefeicao,
  avGeral,
  setAvGeral,
  avComentario,
  setAvComentario,
  avSuccess,
  avErro,
  avEnviando,
  submitAvaliacao,
}: AvaliacaoFormProps) {
  const cardapioAtual = cardapioDia[refeicao]
  const refeicaoDisponivel = temRefeicao(cardapioAtual)

  return (
    <>
      <div className="mb-5">
        <h2 className="text-2xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>
          Avaliar refeição
        </h2>
        <p className="text-sm" style={{ color: 'var(--muted-foreground)' }}>
          A nota e o comentário ficam vinculados a esta refeição.
        </p>
      </div>

      <div role="status" aria-live="polite" aria-atomic="true">
        {avSuccess && (
          <div
            className="mb-5 p-4 rounded-xl flex items-center gap-2 font-semibold text-sm"
            style={{ background: '#EEF7F1', border: '1px solid #B8DCC5', color: '#1A5C2E' }}
          >
            <span aria-hidden="true">✅</span> Avaliação salva na API.
          </div>
        )}
        {avErro && (
          <div
            className="mb-5 p-4 rounded-xl text-sm"
            role="alert"
            style={{ background: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B' }}
          >
            {avErro}
          </div>
        )}
      </div>

      <form onSubmit={submitAvaliacao} className="space-y-4">
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
          <div
            className="rounded-2xl p-6 text-center border space-y-2"
            style={{ background: '#FFFBEB', borderColor: '#FDE68A', color: '#92400E' }}
          >
            <span className="text-3xl block" aria-hidden="true">🔒</span>
            <h3 className="font-bold text-base">Refeição indisponível</h3>
            <p className="text-xs leading-relaxed max-w-sm mx-auto" style={{ color: '#B45309' }}>
              Não há {cardapioAtual.label.toLowerCase()} cadastrado nesta data para o campus selecionado.
            </p>
          </div>
        ) : (
          <>
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <StarRating
                value={avGeral}
                onChange={setAvGeral}
                label="Nota geral"
                id="avaliacao-nota-geral"
              />
              <p className="mt-3 text-xs" style={{ color: 'var(--muted-foreground)' }}>
                Escolha uma nota inteira de 1 a 5.
              </p>
            </div>

            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <label
                htmlFor="av-comentario"
                className="block font-bold mb-2 text-sm uppercase tracking-widest"
                style={{ color: 'var(--muted-foreground)' }}
              >
                Comentário opcional
              </label>
              <textarea
                id="av-comentario"
                value={avComentario}
                onChange={evento => setAvComentario(evento.target.value)}
                maxLength={500}
                rows={4}
                placeholder="Conte como foi a sua experiência..."
                className="w-full px-4 py-3 rounded-xl border text-sm focus:outline-none resize-none"
                style={{ borderColor: 'var(--border)', background: 'var(--background)' }}
              />
              <p className="mt-1 text-right text-xs" style={{ color: 'var(--muted-foreground)' }}>
                {avComentario.length}/500
              </p>
            </div>

            <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
              O prazo da avaliação é validado pela API no fuso de Brasília. Se estiver fechado, o motivo aparecerá aqui.
            </p>

            <button
              type="submit"
              disabled={avEnviando || avGeral === 0}
              className="w-full py-4 rounded-2xl font-bold text-base disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              style={{ background: 'var(--primary)', color: 'white' }}
            >
              {avEnviando ? 'Enviando…' : 'Enviar avaliação →'}
            </button>
          </>
        )}
      </form>
    </>
  )
}
