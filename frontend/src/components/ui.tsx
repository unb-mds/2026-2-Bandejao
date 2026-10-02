import { useState } from 'react'
import { ALERGENOS_MAP } from '@/data'
import type { Avaliacao, AvaliacaoLive, ItemCardapio } from '@/types'
import { iAlerg } from '@/utils'

export function StarRating({ value, onChange, label, id }: { value: number; onChange?: (v: number) => void; label?: string; id?: string }) {
  const [hovered, setHovered] = useState(0)
  return (
    <div className="flex flex-col gap-1.5">
      {label && <span id={id} className="text-xs font-semibold text-[var(--muted-foreground)] uppercase tracking-wider">{label}</span>}
      <div className="flex gap-0.5" role="group" aria-labelledby={id}>
        {[1,2,3,4,5].map(s => (
          <button
            key={s} type="button"
            aria-label={`${s} estrela${s > 1 ? 's' : ''}${label ? ` para ${label}` : ''}`}
            aria-pressed={s === value}
            className="text-2xl leading-none rounded-sm transition-transform hover:scale-110"
            style={{ color: s <= (onChange ? (hovered || value) : value) ? '#E8570A' : '#D5CFC5' }}
            onMouseEnter={() => onChange && setHovered(s)}
            onMouseLeave={() => onChange && setHovered(0)}
            onClick={() => onChange?.(s)}
          >★</button>
        ))}
      </div>
    </div>
  )
}

export function RatingBar({ label, value }: { label: string; value: number }) {
  const color = value >= 4 ? '#2D6A3F' : value === 3 ? '#92600A' : '#CC2C2C'
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-[var(--muted-foreground)] w-14 shrink-0">{label}</span>
      <div className="flex-1 h-1.5 rounded-full bg-[var(--muted)] overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${(value/5)*100}%`, background: color }} />
      </div>
      <span className="text-xs font-bold w-6 text-right" style={{ color }}>{value}</span>
    </div>
  )
}

export function AvaliacaoCard({ av }: { av: Avaliacao }) {
  const [expanded, setExpanded] = useState(false)
  const [photoOpen, setPhotoOpen] = useState(false)
  return (
    <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl overflow-hidden">
      <div className="p-5">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold text-white shrink-0"
              style={{ background: 'linear-gradient(135deg,#1E5631,#2D6A3F)' }}>
              {av.autor.charAt(0)}
            </div>
            <div>
              <p className="font-semibold text-sm leading-tight">{av.autor}</p>
              <p className="text-xs text-[var(--muted-foreground)]">{av.refeicao}{av.campus ? ` · ${av.campus}` : ''} · {av.data}</p>
            </div>
          </div>
          <div className="flex items-center gap-1 px-2.5 py-1 rounded-full" style={{ background: '#FEF3E2' }}>
            <span className="text-[#E8570A] font-bold text-sm">{av.geral}</span>
            <span className="text-[#E8570A] text-xs">★</span>
          </div>
        </div>
        <p className="text-sm text-[var(--foreground)] leading-relaxed">{av.comentario}</p>
        <div className="mt-3 flex items-center gap-3">
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs font-semibold text-[var(--primary)] flex items-center gap-1"
          >
            {expanded ? 'Ocultar detalhes ↑' : 'Ver notas por critério ↓'}
          </button>
          {av.foto && (
            <button
              onClick={() => setPhotoOpen(v => !v)}
              className="text-xs font-semibold flex items-center gap-1"
              style={{ color: '#C9A84C' }}
            >
              <span aria-hidden="true">{photoOpen ? '🙈' : '📷'}</span>
              {photoOpen ? 'Ocultar foto' : 'Ver foto'}
            </button>
          )}
        </div>
        {photoOpen && av.foto && (
          <img
            src={av.foto}
            alt="Foto da refeição"
            className="mt-3 rounded-xl object-cover w-full max-h-52"
            style={{ border: '1px solid var(--border)' }}
          />
        )}
      </div>
      {expanded && (
        <div className="px-5 pb-5 pt-2 border-t border-[var(--border)] space-y-2">
          <RatingBar label="Sabor" value={av.sabor ?? 0} />
          <RatingBar label="Sal" value={av.sal ?? 0} />
          <RatingBar label="Temp." value={av.temperatura ?? 0} />
          <RatingBar label="Apresent." value={av.apresentacao ?? 0} />
          <RatingBar label="Qtd." value={av.quantidade ?? 0} />
        </div>
      )}
    </div>
  )
}

export function AlergLegende({ alergenos }: { alergenos?: string[] }) {
  if (!alergenos?.length) return null
  return (
    <div className="rounded-2xl px-4 py-3 flex flex-wrap items-center gap-x-3 gap-y-2" style={{ background: '#FFFBEB', border: '1px solid #FDE68A' }}>
      <span className="text-[9px] font-bold uppercase tracking-widest shrink-0" style={{ color: '#92400E' }}>Contém</span>
      {alergenos.map(id => {
        const a = ALERGENOS_MAP[id]
        if (!a) return null
        return (
          <span key={id} className="flex items-center gap-1 text-xs font-semibold" style={{ color: a.color }}>
            <span className="w-5 h-5 rounded-full flex items-center justify-center text-[11px]"
              style={{ background: '#fff', border: `1.5px solid ${a.color}` }} aria-hidden="true">{a.emoji}</span>
            {a.label}
          </span>
        )
      })}
    </div>
  )
}

export function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-[9px] font-bold tracking-widest uppercase mb-1" style={{ color: 'var(--muted-foreground)' }}>
      {children}
    </p>
  )
}

export function AlergDots({ item }: { item: ItemCardapio }) {
  const alerg = iAlerg(item)
  if (!alerg.length) return null
  return (
    <span className="inline-flex gap-0.5 ml-1.5 align-middle" aria-label={`Alérgenos: ${alerg.map(id => ALERGENOS_MAP[id]?.label).join(', ')}`}>
      {alerg.map(id => {
        const a = ALERGENOS_MAP[id]
        if (!a) return null
        return (
          <span key={id} title={a.label} aria-hidden="true"
            className="w-[18px] h-[18px] rounded-full inline-flex items-center justify-center shrink-0"
            style={{ background: a.color, fontSize: '10px', lineHeight: 1 }}>
            {a.emoji}
          </span>
        )
      })}
    </span>
  )
}

export function LiveAvaliacaoCard({
  av,
  mealLabel,
  restauranteName,
}: {
  av: AvaliacaoLive
  mealLabel: string
  restauranteName: string
}) {
  const [photoOpen, setPhotoOpen] = useState(false)
  const initials = av.autor
    .split(" ")
    .map((w: string) => w[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()
  const hue =
    av.autor
      .split("")
      .reduce((acc: number, c: string) => acc + c.charCodeAt(0), 0) % 360
  return (
    <div
      className="rounded-2xl p-4"
      style={{ background: "#fff", border: "1px solid var(--border)" }}
    >
      <div className="flex items-start gap-3">
        <div
          className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-sm font-bold text-white"
          style={{ background: `hsl(${hue},50%,42%)` }}
          aria-hidden="true"
        >
          {initials}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <p className="font-semibold text-sm">{av.autor}</p>
            <div className="flex gap-0.5">
              {[1, 2, 3, 4, 5].map((s) => (
                <span
                  key={s}
                  style={{
                    fontSize: "11px",
                    color: s <= av.geral ? "#E8570A" : "#D5CFC5",
                  }}
                >
                  ★
                </span>
              ))}
            </div>
          </div>
          <p
            className="text-[10px] mb-2 flex items-center gap-1.5 flex-wrap"
            style={{ color: "var(--muted-foreground)" }}
          >
            <span
              className="px-1.5 py-0.5 rounded-full font-bold text-[9px] uppercase tracking-wider"
              style={{ background: "#EEF7F1", color: "#1E5631" }}
            >
              {mealLabel}
            </span>
            {av.campus ?? restauranteName} · {av.data}
            {av.horario ? ` às ${av.horario}` : ""}
          </p>
          {av.comentario && (
            <p className="text-sm leading-relaxed mb-2">{av.comentario}</p>
          )}
          {av.foto && (
            <>
              <button
                onClick={() => setPhotoOpen((v) => !v)}
                className="text-xs font-semibold flex items-center gap-1 mb-2"
                style={{ color: "#1E5631" }}
              >
                <span aria-hidden="true">{photoOpen ? "🙈" : "📷"}</span>
                {photoOpen ? "Ocultar foto" : "Ver foto"}
              </button>
              {photoOpen && (
                <img
                  src={av.foto}
                  alt="Foto da refeição"
                  className="rounded-xl object-cover w-full max-h-44"
                  style={{ border: "1px solid var(--border)" }}
                />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}