import type { Tab } from '@/types'

export interface AppNavProps {
  tab: Tab
  setTab: (t: Tab) => void
}

export default function AppNav({ tab, setTab }: AppNavProps) {
  return (
      <nav aria-label="Seções do site" className="sticky top-0 z-10" style={{ background: '#FAFAF7', borderBottom: '1px solid #E8E2D9' }}>
        <div role="tablist" aria-label="Seções" className="max-w-5xl mx-auto flex">
          {([
            {
              id: 'hoje', label: 'Hoje',
              icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><circle cx="12" cy="16" r="2" fill="currentColor" stroke="none"/></svg>,
            },
            {
              id: 'cardapio', label: 'Cardápio',
              icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/><circle cx="7" cy="6" r="1" fill="currentColor" stroke="none"/><circle cx="7" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="7" cy="18" r="1" fill="currentColor" stroke="none"/></svg>,
            },
            {
              id: 'lotacao', label: 'Lotação',
              icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
            },
            {
              id: 'avaliar', label: 'Avaliar',
              icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>,
            },
          ] as { id: typeof tab; label: string; icon: React.ReactNode }[]).map(({ id, label, icon }) => {
            const ativo = tab === id
            return (
              <button key={id} role="tab" aria-selected={ativo} aria-controls={`panel-${id}`}
                id={`tab-${id}`} onClick={() => setTab(id)}
                className="flex-1 flex flex-col items-center justify-center gap-1 py-3 sm:py-3.5 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#1E5631]"
                style={{ position: 'relative', minWidth: 0 }}>
                <span aria-hidden="true" style={{
                  position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)',
                  width: ativo ? '20px' : '0', height: '2px', background: '#C9A84C',
                  borderRadius: '0 0 3px 3px', transition: 'width 0.2s ease',
                }} />
                <span style={{ color: ativo ? '#1A4228' : '#3D3D38', transition: 'color 0.15s', display: 'flex' }}>{icon}</span>
                <span style={{
                  fontSize: '0.6rem', fontWeight: ativo ? 700 : 500, letterSpacing: '0.04em',
                  textTransform: 'uppercase', color: ativo ? '#1A4228' : '#1A1A18',
                  transition: 'color 0.15s', lineHeight: 1, whiteSpace: 'nowrap',
                  overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '4rem',
                }}>{label}</span>
              </button>
            )
          })}
        </div>
      </nav>
  )
}
