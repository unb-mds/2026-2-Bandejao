import { useEffect, useRef } from 'react'
import type { FontSize } from '@/types'

export interface A11yFloatProps {
  a11yOpen: boolean
  setA11yOpen: (v: boolean) => void
  fontSize: FontSize
  setFontSize: (f: FontSize) => void
  altoContraste: boolean
  setAltoContraste: (v: boolean) => void
  espacamento: boolean
  setEspacamento: (v: boolean) => void
  sublinharLinks: boolean
  setSublinharLinks: (v: boolean) => void
}

export default function A11yFloat({ a11yOpen, setA11yOpen, fontSize, setFontSize, altoContraste, setAltoContraste, espacamento, setEspacamento, sublinharLinks, setSublinharLinks }: A11yFloatProps) {
  const a11yBtnRef = useRef<HTMLButtonElement>(null)
  const a11yPanelRef = useRef<HTMLDivElement>(null)

  const closeA11y = () => { setA11yOpen(false); a11yBtnRef.current?.focus() }

  const trapFocus = (e: React.KeyboardEvent) => {
    if (!a11yPanelRef.current) return
    const focusable = Array.from(a11yPanelRef.current.querySelectorAll<HTMLElement>('button,[tabindex="0"]'))
    if (e.key === 'Tab') {
      const first = focusable[0], last = focusable[focusable.length - 1]
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus() }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus() }
    }
    if (e.key === 'Escape') closeA11y()
  }

  useEffect(() => {
    const sizes = { normal: '16px', grande: '18px', maior: '20px' }
    document.documentElement.style.fontSize = sizes[fontSize]
    return () => { document.documentElement.style.fontSize = '' }
  }, [fontSize])

  return (
      <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end gap-2">
        {a11yOpen && (
          <div ref={a11yPanelRef} id="a11y-dialog" role="dialog" aria-modal="true"
            aria-labelledby="a11y-title" onKeyDown={trapFocus}
            className="bg-white border border-[var(--border)] rounded-2xl shadow-2xl p-5 w-72 space-y-5"
            style={{ color: '#1A1A18' }}>
            <div className="flex items-center justify-between">
              <h2 id="a11y-title" className="font-bold text-base">Acessibilidade</h2>
              <button onClick={closeA11y} aria-label="Fechar painel de acessibilidade"
                className="text-[var(--muted-foreground)] hover:text-[var(--foreground)] text-lg leading-none rounded">
                <span aria-hidden="true">✕</span>
              </button>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted-foreground)] mb-2">Tamanho do texto</p>
              <div className="flex gap-2">
                {(['normal', 'grande', 'maior'] as const).map((f, i) => (
                  <button key={f} onClick={() => setFontSize(f)} aria-pressed={fontSize === f}
                    className={`flex-1 py-2 rounded-lg border-2 font-semibold transition-colors ${fontSize === f ? 'border-[var(--primary)] bg-[var(--primary)] text-white' : 'border-[var(--border)] hover:border-[var(--primary)]'}`}
                    style={{ fontSize: i === 0 ? '12px' : i === 1 ? '14px' : '16px' }}>
                    A{i === 1 ? '+' : i === 2 ? '++' : ''}
                  </button>
                ))}
              </div>
            </div>
            <div className="space-y-3">
              {([
                { label: 'Alto contraste', icon: '◑', val: altoContraste, set: setAltoContraste },
                { label: 'Espaçamento extra', icon: '↔', val: espacamento, set: setEspacamento },
                { label: 'Sublinhar links', icon: 'U̲', val: sublinharLinks, set: setSublinharLinks },
              ] as const).map(({ label, icon, val, set }) => (
                <button key={label} role="switch" aria-checked={val} onClick={() => set(!val)}
                  className={`w-full flex items-center justify-between px-4 py-2.5 rounded-xl border-2 text-sm font-medium transition-colors ${val ? 'border-[var(--primary)] bg-[#F0F7F2]' : 'border-[var(--border)] hover:border-[var(--primary)]'}`}>
                  <span className="flex items-center gap-2"><span className="text-base">{icon}</span>{label}</span>
                  <span className={`w-10 h-5 rounded-full relative transition-colors ${val ? 'bg-[var(--primary)]' : 'bg-[var(--border)]'}`}>
                    <span className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${val ? 'left-5' : 'left-0.5'}`} />
                  </span>
                </button>
              ))}
            </div>
            <button
              onClick={() => { setFontSize('normal'); setAltoContraste(false); setEspacamento(false); setSublinharLinks(false) }}
              className="w-full py-2 text-xs text-[var(--muted-foreground)] hover:text-[var(--foreground)] border border-[var(--border)] rounded-lg transition-colors">
              Redefinir tudo
            </button>
          </div>
        )}
        <button ref={a11yBtnRef} onClick={() => a11yOpen ? closeA11y() : setA11yOpen(true)}
          aria-label={a11yOpen ? 'Fechar opções de acessibilidade' : 'Abrir opções de acessibilidade'}
          aria-expanded={a11yOpen} aria-controls="a11y-dialog"
          className="w-14 h-14 rounded-full shadow-lg flex items-center justify-center text-white text-2xl transition-transform hover:scale-105 active:scale-95"
          style={{ background: 'var(--primary)' }}>
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" className="w-7 h-7">
            <circle cx="12" cy="3.5" r="1.5"/>
            <path d="M15.5 8.5H13V7h-2v1.5H8.5a1 1 0 0 0 0 2H11v2.5l-2.8 4.2a1 1 0 1 0 1.6 1.2L12 14.6l2.2 2.8a1 1 0 1 0 1.6-1.2L13 12V10.5h2.5a1 1 0 0 0 0-2z"/>
          </svg>
        </button>
      </div>
  )
}
