export interface CommunityMiniProps {
  totalAvaliacoes: number
  mediaAvaliacoes: string
}

export default function CommunityMini({ totalAvaliacoes, mediaAvaliacoes }: CommunityMiniProps) {
  return (
    <>
        {/* ── Avaliação da comunidade (mini) ── */}
        {totalAvaliacoes > 0 && (
          <div
            className="rounded-2xl p-4 flex items-center gap-4"
            style={{ background: "#FAFAF7", border: "1px solid var(--border)" }}
          >
            <div className="text-center shrink-0">
              <p
                className="text-3xl font-bold leading-none"
                style={{
                  fontFamily: "'Playfair Display', serif",
                  color: "#1E5631",
                }}
              >
                {mediaAvaliacoes}
              </p>
              <div className="flex gap-0.5 mt-1 justify-center">
                {[1, 2, 3, 4, 5].map((s) => (
                  <span
                    key={s}
                    style={{
                      fontSize: "10px",
                      color:
                        s <= Math.round(Number(mediaAvaliacoes))
                          ? "#E8570A"
                          : "#D5CFC5",
                    }}
                  >
                    ★
                  </span>
                ))}
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold">Avaliação da comunidade</p>
              <p
                className="text-xs"
                style={{ color: "var(--muted-foreground)" }}
              >
                Baseado em {totalAvaliacoes} avaliação
                {totalAvaliacoes > 1 ? "ões" : ""} recentes
              </p>
            </div>
          </div>
        )}
    </>
  )
}
