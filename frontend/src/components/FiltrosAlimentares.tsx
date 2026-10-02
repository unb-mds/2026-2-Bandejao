import { useState, useEffect, useRef } from 'react'
import { ALERGENOS_MAP } from '@/data'
import type { FiltrosAlimentares } from '@/types'

export interface FiltrosAlimentaresProps {
  filtros: FiltrosAlimentares
  setFiltros: (f: FiltrosAlimentares) => void
}

export default function FiltrosAlimentares({ filtros, setFiltros }: FiltrosAlimentaresProps) {
  const [aberto, setAberto] = useState(false)
  const painelRef = useRef<HTMLDivElement>(null)
  const botaoRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!aberto) return
    const handleClick = (e: MouseEvent) => {
      if (
        painelRef.current && !painelRef.current.contains(e.target as Node) &&
        botaoRef.current && !botaoRef.current.contains(e.target as Node)
      ) {
        setAberto(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [aberto])

  const toggleAlergeno = (id: string) => {
    const novos = filtros.alergenos.includes(id)
      ? filtros.alergenos.filter(a => a !== id)
      : [...filtros.alergenos, id]
    setFiltros({ ...filtros, alergenos: novos })
  }

  const totalAtivos =
    filtros.alergenos.length +
    (filtros.vegetariano ? 1 : 0) +
    (filtros.vegetarianoEstrito ? 1 : 0)

  return (
    <div className="relative">
      <button
        ref={botaoRef}
        onClick={() => setAberto(v => !v)}
        aria-expanded={aberto}
        aria-controls="filtros-panel"
        className="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold transition-colors"
        style={{
          background: totalAtivos > 0 ? '#1E5631' : '#fff',
          color: totalAtivos > 0 ? '#fff' : '#1A1A18',
          border: '1px solid var(--border)',
        }}
      >
        <span aria-hidden="true">🍽️</span>
        Filtros alimentares
        {totalAtivos > 0 && (
          <span
            className="ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold"
            style={{ background: '#C9A84C', color: '#0f2d1a' }}
          >
            {totalAtivos}
          </span>
        )}
      </button>

      {aberto && (
        <div
          ref={painelRef}
          id="filtros-panel"
          role="dialog"
          aria-label="Filtros alimentares"
          className="absolute z-50 mt-2 right-0 w-80 rounded-2xl p-5 space-y-4"
          style={{
            background: '#fff',
            border: '1px solid var(--border)',
            boxShadow: '0 12px 40px rgba(0,0,0,0.18)',
            maxHeight: '70vh',
            overflowY: 'auto',
          }}
        >
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-base">Filtros alimentares</h3>
            <button
              onClick={() => setAberto(false)}
              aria-label="Fechar filtros"
              className="text-lg leading-none"
            >
              ✕
            </button>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider mb-2" style={{ color: 'var(--muted-foreground)' }}>
              Preferências
            </p>
            <div className="space-y-2">
              <button
                role="switch"
                aria-checked={filtros.vegetariano}
                onClick={() => setFiltros({ ...filtros, vegetariano: !filtros.vegetariano })}
                className="w-full flex items-center justify-between px-3 py-2 rounded-xl border-2 text-sm font-medium transition-colors"
                style={{
                  borderColor: filtros.vegetariano ? '#1E5631' : 'var(--border)',
                  background: filtros.vegetariano ? '#F0F7F2' : '#fff',
                }}
              >
                Vegetariano (ovolacto)
                <span
                  className="w-9 h-5 rounded-full relative transition-colors"
                  style={{ background: filtros.vegetariano ? '#1E5631' : 'var(--border)' }}
                >
                  <span
                    className="absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all"
                    style={{ left: filtros.vegetariano ? '1.25rem' : '0.125rem' }}
                  />
                </span>
              </button>
              <button
                role="switch"
                aria-checked={filtros.vegetarianoEstrito}
                onClick={() => setFiltros({ ...filtros, vegetarianoEstrito: !filtros.vegetarianoEstrito })}
                className="w-full flex items-center justify-between px-3 py-2 rounded-xl border-2 text-sm font-medium transition-colors"
                style={{
                  borderColor: filtros.vegetarianoEstrito ? '#1E5631' : 'var(--border)',
                  background: filtros.vegetarianoEstrito ? '#F0F7F2' : '#fff',
                }}
              >
                Vegetariano estrito
                <span
                  className="w-9 h-5 rounded-full relative transition-colors"
                  style={{ background: filtros.vegetarianoEstrito ? '#1E5631' : 'var(--border)' }}
                >
                  <span
                    className="absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all"
                    style={{ left: filtros.vegetarianoEstrito ? '1.25rem' : '0.125rem' }}
                  />
                </span>
              </button>
            </div>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider mb-2" style={{ color: 'var(--muted-foreground)' }}>
              Evitar alérgenos
            </p>
            <div className="flex flex-wrap gap-1.5">
              {Object.entries(ALERGENOS_MAP).map(([id, a]) => {
                const ativo = filtros.alergenos.includes(id)
                return (
                  <button
                    key={id}
                    onClick={() => toggleAlergeno(id)}
                    aria-pressed={ativo}
                    className="flex items-center gap-1 px-2.5 py-1.5 rounded-full text-xs font-semibold transition-colors"
                    style={{
                      background: ativo ? a.color : '#fff',
                      color: ativo ? '#fff' : 'var(--foreground)',
                      border: `1.5px solid ${ativo ? a.color : 'var(--border)'}`,
                    }}
                  >
                    <span aria-hidden="true">{a.emoji}</span>
                    {a.label}
                  </button>
                )
              })}
            </div>
          </div>

          {totalAtivos > 0 && (
            <button
              onClick={() => setFiltros({ vegetariano: false, vegetarianoEstrito: false, alergenos: [] })}
              className="w-full py-2 text-xs font-semibold rounded-lg border transition-colors"
              style={{ borderColor: 'var(--border)', color: 'var(--muted-foreground)' }}
            >
              Limpar filtros
            </button>
          )}
        </div>
      )}
    </div>
  )
}