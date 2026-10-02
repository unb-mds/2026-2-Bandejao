import { useState } from 'react'
import MealContent from '@/components/MealContent'
import FiltrosAlimentares from '@/components/FiltrosAlimentares'
import { DIAS_SEMANA, DIAS_SEMANA_COMPLETO } from '@/data'
import type { CardapioRefeicoes, Refeicao, RefeicaoData, FiltrosAlimentares as Filtros } from '@/types'

export interface CardapioTabProps {
  cardapioDia: CardapioRefeicoes
  diaSemana: number
  setDiaSemana: (d: number) => void
  diasDisponiveis: number[]
  refeicao: Refeicao
  setRefeicao: (r: Refeicao) => void
  isPlanejada: (dia: number, ref: Refeicao) => boolean
  planejadosCount: number
  cardapio: RefeicaoData
  togglePlanejada: (dia: number, refeicao: Refeicao) => void
}

export default function CardapioTab({ cardapioDia, diaSemana, setDiaSemana, diasDisponiveis, refeicao, setRefeicao, isPlanejada, planejadosCount, cardapio, togglePlanejada }: CardapioTabProps) {
  const [filtros, setFiltros] = useState<Filtros>({
    vegetariano: false,
    vegetarianoEstrito: false,
    alergenos: [],
  })

  return (
    <div id="panel-cardapio" role="tabpanel" aria-labelledby="tab-cardapio">

      {/* Cabeçalho com filtros */}
      <div style={{ background: '#fff', borderBottom: '1px solid #f0ede8' }}>
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider" style={{ color: 'var(--muted-foreground)' }}>
            Cardápio da semana
          </h2>
          <FiltrosAlimentares filtros={filtros} setFiltros={setFiltros} />
        </div>
      </div>

      {/* Day selector */}
      <div style={{ background: '#fff', borderBottom: '1px solid #f0ede8' }}>
        <div className="max-w-5xl mx-auto" style={{ padding: '0.5em 0.75em 0.4em' }}>
          <div role="group" aria-label="Selecionar dia da semana"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(${diasDisponiveis.length}, minmax(2.8em, 1fr))`,
              gap: 0, overflowX: 'auto',
              WebkitOverflowScrolling: 'touch', scrollbarWidth: 'none', msOverflowStyle: 'none',
            }}
            className="no-scrollbar">
            {diasDisponiveis.map((d, i) => {
              const hojeD = new Date().getDay()
              const base = new Date(`${cardapioDia.cafe.data}T12:00:00`)
              base.setDate(base.getDate() - diaSemana + d)
              const dia = String(base.getDate()).padStart(2, '0')
              const mes = String(base.getMonth() + 1).padStart(2, '0')
              const isHoje = d === hojeD && base.toDateString() === new Date().toDateString()
              const isAtivo = d === diaSemana
              const isFirst = i === 0
              const isLast = i === diasDisponiveis.length - 1
              const hasPlanned = (['cafe','almoco','jantar'] as Refeicao[]).some(r => isPlanejada(d, r))
              return (
                <button key={d} onClick={() => setDiaSemana(d)} aria-pressed={isAtivo}
                  className="flex flex-col items-center justify-center transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#1E5631]"
                  style={{
                    minWidth: '2.8em', paddingTop: '0.45em', paddingBottom: '0.45em',
                    paddingLeft: '0.15em', paddingRight: '0.15em',
                    background: isAtivo ? '#1E5631' : 'transparent',
                    borderRadius: isFirst ? '0.6em 0 0 0.6em' : isLast ? '0 0.6em 0.6em 0' : '0',
                    borderBottom: isAtivo ? 'none' : isHoje ? '0.15em solid #1E5631' : '0.15em solid transparent',
                    position: 'relative',
                  }}
                  aria-label={`${DIAS_SEMANA_COMPLETO[d]}, ${dia}/${mes}${isHoje ? ', hoje' : ''}`}>
                  {hasPlanned && !isAtivo && (
                    <span style={{ position: 'absolute', top: '0.2em', right: '0.3em', width: '0.35em', height: '0.35em', borderRadius: '50%', background: '#C9A84C', display: 'block' }} aria-hidden="true" />
                  )}
                  <span style={{ fontSize: '0.6em', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', lineHeight: 1, marginBottom: '0.3em', color: isAtivo ? '#fff' : isHoje ? '#1E5631' : '#9a9a90' }}>
                    {DIAS_SEMANA[d]}
                  </span>
                  <span style={{ fontSize: '0.65em', fontWeight: 600, lineHeight: 1, color: isAtivo ? 'rgba(255,255,255,0.8)' : isHoje ? '#1E5631' : '#c0bdb8' }}>
                    {dia}/{mes}
                  </span>
                  {isHoje && (
                    <span style={{ marginTop: '0.3em', width: '0.3em', height: '0.3em', borderRadius: '50%', display: 'block', background: isAtivo ? 'rgba(255,255,255,0.5)' : '#C9A84C' }} aria-hidden="true" />
                  )}
                </button>
              )
            })}
          </div>
        </div>
      </div>

      {/* Planning summary pill */}
      {planejadosCount > 0 && (
        <div style={{ background: '#F5F2ED', borderBottom: '1px solid #E8E2D9' }}>
          <div className="max-w-5xl mx-auto px-4 py-2 flex items-center gap-2">
            <span className="text-xs font-semibold" style={{ color: '#1E5631' }}>
              📋 {planejadosCount} refeição{planejadosCount > 1 ? 'ões' : ''} planejada{planejadosCount > 1 ? 's' : ''} esta semana
            </span>
          </div>
        </div>
      )}

      {/* Meal selector */}
      <div style={{ background: '#F5F2ED', borderBottom: '1px solid #E8E2D9' }} className="px-3 py-3">
        <div role="group" aria-label="Selecionar refeição" className="flex gap-2 max-w-5xl mx-auto">
          {([
            {
              id: 'cafe' as Refeicao, label: 'Café da Manhã', accent: '#C9A84C',
              icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="2" x2="6" y2="5"/><line x1="10" y1="2" x2="10" y2="5"/><line x1="14" y1="2" x2="14" y2="5"/></svg>,
            },
            {
              id: 'almoco' as Refeicao, label: 'Almoço', accent: '#C9A84C',
              icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"><line x1="11" y1="21" x2="11" y2="13"/><path d="M9 9V3H7v6"/><line x1="13" y1="9" x2="9" y2="9"/><path d="M13 3v6"/><line x1="17" y1="3" x2="17" y2="21"/><path d="M15 3c0 0 4 2 4 6s-4 6-4 6"/></svg>,
            },
            {
              id: 'jantar' as Refeicao, label: 'Jantar', accent: '#C9A84C',
              icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>,
            },
          ]).map(({ id, label, accent, icon }) => {
            const ativo = refeicao === id
            const planned = isPlanejada(diaSemana, id)
            return (
              <button key={id} onClick={() => setRefeicao(id)} aria-pressed={ativo}
                className="flex-1 flex flex-col items-center gap-1.5 rounded-2xl transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-[#1E5631]"
                style={{
                  padding: '0.85rem 0.5rem 0.75rem',
                  background: ativo ? '#1A4228' : '#fff',
                  border: `1px solid ${ativo ? '#1A4228' : '#E0DBD2'}`,
                  boxShadow: ativo ? '0 4px 18px rgba(26,66,40,0.22)' : '0 1px 4px rgba(0,0,0,0.05)',
                  position: 'relative',
                }}>
                {planned && (
                  <span style={{ position: 'absolute', top: '0.4rem', right: '0.5rem', fontSize: '0.6rem', color: ativo ? '#f5d070' : '#C9A84C' }} aria-hidden="true">✓</span>
                )}
                <span style={{ color: ativo ? accent : '#8A9E8F', transition: 'color 0.2s' }}>{icon}</span>
                <span style={{ fontSize: '0.68rem', fontWeight: 700, letterSpacing: '0.05em', textTransform: 'uppercase', lineHeight: 1.25, color: ativo ? '#fff' : '#3D4A3E', textAlign: 'center', transition: 'color 0.2s' }}>
                  {label}
                </span>
                <span className="mono" style={{ fontSize: '0.57rem', letterSpacing: '0.08em', color: ativo ? 'rgba(201,168,76,0.85)' : '#A8A29E', transition: 'color 0.2s' }}>
                  {cardapioDia[id].horario}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Conteúdo da refeição — COM FILTRO */}
      <div className="px-4 pt-4 pb-6 max-w-5xl mx-auto">
        {cardapio.itensApi && cardapio.itensApi.length > 0 && <button
          className="mb-4 rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground"
          aria-pressed={isPlanejada(diaSemana, refeicao)} onClick={() => togglePlanejada(diaSemana, refeicao)}>
          {isPlanejada(diaSemana, refeicao) ? 'Remover do planejamento desta sessão' : 'Planejar esta refeição nesta sessão'}
        </button>}
        <MealContent data={cardapio} dia={diaSemana} refeicao={refeicao} filtros={filtros} />
      </div>
    </div>
  )
}