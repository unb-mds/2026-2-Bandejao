import { AvaliacaoCard } from '@/components/ui'
import type { Avaliacao, CardapioRefeicoes, Refeicao } from '@/types'

export interface AvaliacaoHistoricoProps {
  cardapioDia: CardapioRefeicoes
  refeicao: Refeicao
  setRefeicao: (refeicao: Refeicao) => void
  avaliacoes: Avaliacao[]
  mediaGeral: string
  estado: 'inativo' | 'carregando' | 'pronto' | 'erro'
  erro: string
  onTentarNovamente: () => void
  onAvaliar: () => void
}

export default function AvaliacaoHistorico({
  cardapioDia,
  refeicao,
  setRefeicao,
  avaliacoes,
  mediaGeral,
  estado,
  erro,
  onTentarNovamente,
  onAvaliar,
}: AvaliacaoHistoricoProps) {
  const cardapioAtual = cardapioDia[refeicao]

  return (
    <div className="space-y-4">
      <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
        <h2 className="text-xl font-bold mb-1">Histórico da refeição</h2>
        <p className="text-sm mb-4" style={{ color: 'var(--muted-foreground)' }}>
          São mostradas somente as avaliações da refeição selecionada.
        </p>
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
        {cardapioAtual.data && (
          <p className="mt-3 text-xs" style={{ color: 'var(--muted-foreground)' }}>
            Data da refeição: {new Date(`${cardapioAtual.data}T12:00:00`).toLocaleDateString('pt-BR')}
          </p>
        )}
      </div>

      {estado === 'inativo' && (
        <div className="text-center py-12" role="status" style={{ color: 'var(--muted-foreground)' }}>
          <span className="text-5xl block mb-4" aria-hidden="true">📭</span>
          <p className="font-semibold">Sem avaliações.</p>
          <p className="text-sm">Não há uma refeição publicada para consultar nesta seleção.</p>
        </div>
      )}

      {estado === 'carregando' && <p role="status">Carregando avaliações…</p>}

      {estado === 'erro' && (
        <div className="rounded-xl border border-red-300 p-4" role="alert">
          <p>Não foi possível carregar as avaliações. {erro}</p>
          <button className="mt-2 underline" type="button" onClick={onTentarNovamente}>
            Tentar novamente
          </button>
        </div>
      )}

      {estado === 'pronto' && avaliacoes.length === 0 && (
        <div className="text-center py-12" role="status" style={{ color: 'var(--muted-foreground)' }}>
          <span className="text-5xl block mb-4" aria-hidden="true">📭</span>
          <p className="font-semibold">Sem avaliações para esta refeição.</p>
          <p className="text-sm">Nenhuma nota fictícia é exibida.</p>
          <button
            type="button"
            onClick={onAvaliar}
            className="mt-4 px-5 py-2.5 rounded-xl font-semibold text-sm text-white"
            style={{ background: 'var(--primary)' }}
          >
            Avaliar agora
          </button>
        </div>
      )}

      {estado === 'pronto' && avaliacoes.length > 0 && (
        <>
          <div className="flex items-center gap-4 p-4 rounded-2xl" style={{ background: '#fff', border: '1px solid var(--border)' }}>
            <p className="text-4xl font-bold" style={{ fontFamily: "'Playfair Display', serif", color: '#1E5631' }}>
              {mediaGeral}
            </p>
            <div className="flex-1">
              <p className="text-sm font-semibold">Média desta refeição</p>
              <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
                {avaliacoes.length} {avaliacoes.length === 1 ? 'avaliação' : 'avaliações'}
              </p>
            </div>
          </div>
          <div className="space-y-2">
            {avaliacoes.map(avaliacao => <AvaliacaoCard key={avaliacao.id} av={avaliacao} />)}
          </div>
        </>
      )}
    </div>
  )
}
