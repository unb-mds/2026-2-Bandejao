import { StarRating } from '@/components/ui'
import type { Campus, CardapioRefeicoes, Refeicao, RefeicaoData } from '@/types'

export interface AvaliacaoFormProps {
  cardapioDia: CardapioRefeicoes
  refeicao: Refeicao
  setRefeicao: (r: Refeicao) => void
  campus: Campus
  avNome: string
  setAvNome: (v: string) => void
  avSabor: number
  setAvSabor: (v: number) => void
  avSal: number
  setAvSal: (v: number) => void
  avTemp: number
  setAvTemp: (v: number) => void
  avApres: number
  setAvApres: (v: number) => void
  avQtd: number
  setAvQtd: (v: number) => void
  avGeral: number
  setAvGeral: (v: number) => void
  avComentario: string
  setAvComentario: (v: string) => void
  avFoto: string | undefined
  setAvFoto: (v: string | undefined) => void
  avSuccess: boolean
  fileRef: React.RefObject<HTMLInputElement | null>
  dragging: boolean
  setDragging: (v: boolean) => void
  handleFoto: (file: File) => void
  handleDrop: (e: React.DragEvent) => void
  submitAvaliacao: (e: React.FormEvent) => void
}

// ── Mesma função usada na HomeScreen ──
function temRefeicao(mealData: RefeicaoData | undefined | null): boolean {
  if (!mealData) return false
  if (mealData.itensApi) return mealData.itensApi.length > 0
  const prato = mealData.prato_principal
  if (prato === '—') return false
  if (typeof prato === 'object' && prato?.nome === '—') return false
  return true
}

export default function AvaliacaoForm({
  cardapioDia,
  refeicao,
  setRefeicao,
  // campus é mantido na interface para não quebrar o App.tsx,
  // mas não é mais usado na lógica
  campus: _campus,
  avNome,
  setAvNome,
  avSabor,
  setAvSabor,
  avSal,
  setAvSal,
  avTemp,
  setAvTemp,
  avApres,
  setAvApres,
  avQtd,
  setAvQtd,
  avGeral,
  setAvGeral,
  avComentario,
  setAvComentario,
  avFoto,
  setAvFoto,
  avSuccess,
  fileRef,
  dragging,
  setDragging,
  handleFoto,
  handleDrop,
  submitAvaliacao,
}: AvaliacaoFormProps) {
  const cardapioAtual = cardapioDia[refeicao]

  // ── Detecta se a refeição tem conteúdo real (dinâmico) ──
  const temComidaHoje = temRefeicao(cardapioAtual)

  // ── Horário atual (minutos desde 00:00) ──
  const agora = new Date()
  const mins = agora.getHours() * 60 + agora.getMinutes()

  const INICIO_REFEICAO: Record<Refeicao, number> = {
    cafe: 7 * 60,      // 7h
    almoco: 11 * 60,   // 11h
    jantar: 17 * 60,   // 17h
  }

  const refeicaoJaComecou = mins >= INICIO_REFEICAO[refeicao]

  // Pode avaliar se: tem refeição cadastrada E já começou
  const podeAvaliar = temComidaHoje && refeicaoJaComecou

  return (
    <>
      {/* ── Cabeçalho ── */}
      <div className="mb-5">
        <h2 className="text-2xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>
          Avaliar refeição
        </h2>
        <p className="text-sm" style={{ color: 'var(--muted-foreground)' }}>
          Sua opinião ajuda a melhorar a qualidade do bandejão.
        </p>
      </div>

      <div role="status" aria-live="polite" aria-atomic="true">
        {avSuccess && (
          <div
            className="mb-5 p-4 rounded-xl flex items-center gap-2 font-semibold text-sm"
            style={{ background: '#EEF7F1', border: '1px solid #B8DCC5', color: '#1A5C2E' }}
          >
            <span aria-hidden="true">✅</span> Avaliação salva nesta sessão de demonstração.
          </div>
        )}
      </div>

      <form onSubmit={submitAvaliacao} className="space-y-4">
        {/* Seletor de Refeição */}
        <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
          <h3 className="font-bold mb-3 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>
            Qual refeição?
          </h3>
          <div className="flex gap-2">
            {(['cafe', 'almoco', 'jantar'] as Refeicao[]).map(r => (
              <button
                key={r}
                type="button"
                onClick={() => setRefeicao(r)}
                className="flex-1 py-2.5 rounded-xl text-sm font-semibold border transition-all"
                style={{
                  background: refeicao === r ? '#1E5631' : '#fff',
                  color: refeicao === r ? '#fff' : 'var(--foreground)',
                  borderColor: refeicao === r ? '#1E5631' : 'var(--border)',
                }}
              >
                {cardapioDia[r].label}
              </button>
            ))}
          </div>
        </div>

        {/* Bloqueio ou formulário */}
        {!podeAvaliar ? (
          <div
            className="rounded-2xl p-6 text-center border space-y-2"
            style={{ background: '#FFFBEB', borderColor: '#FDE68A', color: '#92400E' }}
          >
            <span className="text-3xl block" aria-hidden="true">🔒</span>
            {!temComidaHoje ? (
              <>
                <h3 className="font-bold text-base">Sem funcionamento hoje</h3>
                <p className="text-xs leading-relaxed max-w-sm mx-auto" style={{ color: '#B45309' }}>
                  Não há <strong>{cardapioAtual.label}</strong> cadastrado para hoje neste campus.
                </p>
              </>
            ) : (
              <>
                <h3 className="font-bold text-base">Avaliação Indisponível</h3>
                <p className="text-xs leading-relaxed max-w-sm mx-auto" style={{ color: '#B45309' }}>
                  A avaliação para o <strong>{cardapioAtual.label}</strong> estará liberada a partir das {refeicao === 'cafe' ? '7h' : refeicao === 'almoco' ? '11h' : '17h'} e ficará disponível até o final do dia.
                </p>
              </>
            )}
          </div>
        ) : (
          <>
            {/* Nome */}
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <label htmlFor="av-nome" className="block text-sm font-semibold mb-2">
                Seu nome (opcional)
              </label>
              <input
                id="av-nome"
                type="text"
                value={avNome}
                onChange={e => setAvNome(e.target.value)}
                placeholder="Ex.: João Silva ou deixe em branco"
                className="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
                style={{ borderColor: 'var(--border)', background: 'var(--background)' }}
              />
            </div>

            {/* Notas por critério */}
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <h3 className="font-bold mb-4 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>
                Notas por critério
              </h3>
              <div className="space-y-5">
                {[
                  { val: avSabor, set: setAvSabor, label: 'Sabor', id: 'sr-sabor', icon: '🍴' },
                  { val: avSal, set: setAvSal, label: 'Sal (equilíbrio)', id: 'sr-sal', icon: '🧂' },
                  { val: avTemp, set: setAvTemp, label: 'Temperatura', id: 'sr-temp', icon: '🌡️' },
                  { val: avApres, set: setAvApres, label: 'Apresentação', id: 'sr-apres', icon: '👁️' },
                  { val: avQtd, set: setAvQtd, label: 'Quantidade', id: 'sr-qtd', icon: '⚖️' },
                  { val: avGeral, set: setAvGeral, label: 'Nota Geral', id: 'sr-geral', icon: '⭐' },
                ].map(({ val, set, label, id, icon }) => (
                  <div key={id} className="flex items-center gap-3">
                    <span className="text-xl w-7 text-center shrink-0" aria-hidden="true">
                      {icon}
                    </span>
                    <div className="flex-1">
                      <StarRating value={val} onChange={set} label={label} id={id} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Foto */}
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <h3 className="font-bold mb-1 text-sm uppercase tracking-widest" style={{ color: 'var(--muted-foreground)' }}>
                Foto (opcional)
              </h3>
              <p className="text-xs mb-4" style={{ color: 'var(--muted-foreground)' }}>
                Ajude outros estudantes a saber como está o prato hoje.
              </p>
              <div
                role="button"
                tabIndex={0}
                aria-label="Enviar foto da refeição"
                className={`upload-zone rounded-xl p-6 text-center cursor-pointer ${dragging ? 'dragover' : ''}`}
                onClick={() => fileRef.current?.click()}
                onKeyDown={e => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), fileRef.current?.click())}
                onDragOver={e => {
                  e.preventDefault()
                  setDragging(true)
                }}
                onDragLeave={() => setDragging(false)}
                onDrop={handleDrop}
              >
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={e => e.target.files?.[0] && handleFoto(e.target.files[0])}
                />
                {avFoto ? (
                  <div className="relative">
                    <img src={avFoto} alt="Preview" className="max-h-48 mx-auto rounded-lg object-cover" />
                    <button
                      type="button"
                      onClick={e => {
                        e.stopPropagation()
                        setAvFoto(undefined)
                      }}
                      className="absolute top-2 right-2 bg-white rounded-full w-7 h-7 flex items-center justify-center text-sm shadow border border-[var(--border)] hover:bg-red-50"
                    >
                      ✕
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <span className="text-4xl">📷</span>
                    <p className="text-sm font-medium" style={{ color: 'var(--muted-foreground)' }}>
                      Clique ou arraste uma foto aqui
                    </p>
                    <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
                      JPG, PNG ou WEBP
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Comentário */}
            <div className="rounded-2xl p-5" style={{ background: '#fff', border: '1px solid var(--border)' }}>
              <label
                htmlFor="av-comentario"
                className="block font-bold mb-2 text-sm uppercase tracking-widest"
                style={{ color: 'var(--muted-foreground)' }}
              >
                Comentário
              </label>
              <textarea
                id="av-comentario"
                value={avComentario}
                onChange={e => setAvComentario(e.target.value)}
                rows={4}
                placeholder="Conte como foi a sua experiência hoje..."
                className="w-full px-4 py-3 rounded-xl border text-sm focus:outline-none resize-none"
                style={{ borderColor: 'var(--border)', background: 'var(--background)' }}
              />
            </div>

            <button
              type="submit"
              disabled={!avSabor || !avSal || !avTemp || !avApres || !avQtd || !avGeral}
              className="w-full py-4 rounded-2xl font-bold text-base disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              style={{ background: 'var(--primary)', color: 'white' }}
            >
              Enviar avaliação →
            </button>
          </>
        )}
      </form>
    </>
  )
}