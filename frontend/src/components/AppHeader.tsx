import type { Campus } from '@/types'

export interface AppHeaderProps {
  campus: Campus
  campi: Campus[]
  hoje: Date
  mediaGeral: string
  totalAvaliacoes: number
  planejadosCount: number
  handleCampusChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
}

export default function AppHeader({ campus, campi, hoje, mediaGeral, totalAvaliacoes, planejadosCount, handleCampusChange }: AppHeaderProps) {
  return (
      <header style={{ background: '#0f2d1a', position: 'relative', overflow: 'hidden' }}>
        <div aria-hidden="true" style={{
          position: 'absolute', right: '-0.5rem', top: '-1rem',
          fontSize: '13rem', fontFamily: "'Playfair Display', serif",
          fontWeight: 700, color: 'rgba(255,255,255,0.035)',
          lineHeight: 1, pointerEvents: 'none', userSelect: 'none',
          letterSpacing: '-0.04em',
        }}>B</div>
        <div style={{ height: '4px', background: 'linear-gradient(90deg, #C9A84C, #e8c96a, #C9A84C)' }} />
        <div className="relative max-w-5xl mx-auto px-5 sm:px-8 pt-5 pb-5 sm:pt-7 sm:pb-6">
          <div className="flex items-start justify-between mb-4 sm:mb-5">
            <div>
              <p style={{ color: '#C9A84C', fontSize: '9px', letterSpacing: '0.26em' }} className="font-semibold uppercase">
                Universidade de Brasília
              </p>
              <p style={{ color: 'rgba(168,213,181,0.5)', fontSize: '9px', letterSpacing: '0.15em' }} className="font-medium uppercase mt-0.5">
                Decanato de Assuntos Comunitários
              </p>
            </div>
            <img src="https://www.unb.br/images/Marca_UnB/EsquemasCores/Branco/UnB-vertical_branco.png"
              alt="UnB" className="h-10 sm:h-12 w-auto object-contain opacity-90"
              onError={e => { (e.target as HTMLImageElement).style.display = 'none' }} />
          </div>
          <h1 style={{
            color: '#ffffff', fontSize: 'clamp(2rem, 7vw, 3.25rem)',
            fontFamily: "'Playfair Display', serif", fontWeight: 700,
            letterSpacing: '-0.03em', lineHeight: 1.05,
          }}>
            Bandejão <span style={{ color: '#C9A84C' }}>UnB</span>
          </h1>
          <div style={{ height: '1.5px', width: '3rem', background: '#C9A84C', marginTop: '0.75rem', marginBottom: '1.25rem', borderRadius: '2px' }} aria-hidden="true" />
          <div className="flex flex-row gap-2">
            <div className="relative">
              <select disabled={campi.length === 0} value={campus.id} onChange={handleCampusChange} aria-label="Selecionar campus"
                className="appearance-none cursor-pointer text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-[#C9A84C]"
                style={{ background: 'rgba(255,255,255,0.07)', color: '#fff', border: '1px solid rgba(201,168,76,0.35)', borderRadius: '999px', padding: '0.55rem 2.4rem 0.55rem 1.1rem' }}>
                {campi.length === 0 && <option value="">Nenhum campus disponível</option>}
                {campi.map(c => <option key={c.id} value={c.id} style={{ color: '#1A1A18', background: '#fff' }}>{c.name}</option>)}
              </select>
              <svg aria-hidden="true" className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2" width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2.5 4.5l3.5 3 3.5-3" stroke="#C9A84C" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
        <div style={{ borderTop: '1px solid rgba(201,168,76,0.15)', background: 'rgba(0,0,0,0.25)' }} className="px-5 sm:px-8 py-2">
          <div className="max-w-5xl mx-auto flex flex-wrap items-center gap-x-4 gap-y-0.5 text-[10px] mono" style={{ color: 'rgba(168,213,181,0.7)' }}>
            <span>📍 {campus.name}</span>
            <span aria-hidden="true" className="opacity-30">·</span>
            <span>📅 {hoje.toLocaleDateString('pt-BR', { weekday: 'short', day: 'numeric', month: 'short' })}</span>
            <span aria-hidden="true" className="opacity-30">·</span>
            <span>⭐ {mediaGeral}/5 ({totalAvaliacoes} aval.)</span>
            {planejadosCount > 0 && <>
              <span aria-hidden="true" className="opacity-30">·</span>
              <span>📋 {planejadosCount} planejadas</span>
            </>}
          </div>
        </div>
      </header>
  )
}