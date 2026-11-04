export interface AvaliacoesDiaLinksProps {
  hoje: Date
  onVerHistorico: () => void
}

export default function AvaliacoesDiaLinks({ hoje, onVerHistorico }: AvaliacoesDiaLinksProps) {
  return (
    <>
        {/* ── AVALIAÇÕES DO DIA — links rápidos ── */}
        {(() => {
          const h = hoje.getHours() + hoje.getMinutes() / 60
          const links: { emoji: string; label: string }[] = []
          if (h >= 7) links.push({ emoji: "☕", label: "Café da Manhã" })
          if (h >= 11) links.push({ emoji: "🍽️", label: "Almoço" })
          if (h >= 17) links.push({ emoji: "🌙", label: "Jantar" })
          if (links.length === 0) return null
          return (
            <div>
              <p
                className="text-xs font-bold uppercase tracking-widest mb-3 px-1"
                style={{ color: "var(--muted-foreground)" }}
              >
                Avaliações de hoje
              </p>
              <div className="flex flex-wrap gap-2">
                {links.map(({ emoji, label }) => (
                  <button
                    key={label}
                    onClick={onVerHistorico}
                    className="flex items-center gap-1.5 px-4 py-2.5 rounded-2xl text-sm font-semibold transition-all active:scale-[0.97]"
                    style={{
                      background: "#fff",
                      border: "1px solid var(--border)",
                      color: "var(--foreground)",
                      boxShadow: "0 1px 6px rgba(0,0,0,0.05)",
                    }}
                    aria-label={`Ver avaliações do ${label} de hoje`}
                  >
                    <span aria-hidden="true">{emoji}</span> {label}
                  </button>
                ))}
              </div>
            </div>
          )
        })()}
    </>
  )
}
