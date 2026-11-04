export interface FeedbackCTAProps {
  totalAvaliacoes: number
  mediaAvaliacoes: string
  onAvaliar: () => void
  onReclamar: () => void
}

export default function FeedbackCTA({ totalAvaliacoes, mediaAvaliacoes, onAvaliar, onReclamar }: FeedbackCTAProps) {
  return (
    <>
        {/* ── FEEDBACK ── */}
        <div>
          <p
            className="text-xs font-bold uppercase tracking-widest mb-3 px-1"
            style={{ color: "var(--muted-foreground)" }}
          >
            Participar
          </p>
          <div className="grid grid-cols-2 gap-3">
            {/* Avaliar */}
            <button
              onClick={onAvaliar}
              className="rounded-2xl p-5 flex flex-col gap-3 text-left transition-all hover:shadow-md active:scale-[0.98]"
              style={{
                background: "#1E5631",
                color: "#fff",
                boxShadow: "0 2px 12px rgba(30,86,49,0.2)",
              }}
            >
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                style={{ background: "rgba(255,255,255,0.15)" }}
                aria-hidden="true"
              >
                ⭐
              </div>
              <div>
                <p className="font-bold text-sm">Avaliar refeição</p>
                <p
                  className="text-xs mt-0.5"
                  style={{ color: "rgba(255,255,255,0.6)" }}
                >
                  {totalAvaliacoes} avaliações · {mediaAvaliacoes}/5
                </p>
              </div>
              <div
                className="flex items-center gap-1 text-xs font-semibold"
                style={{ color: "#C9A84C" }}
              >
                Avaliar agora
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </button>

            {/* Reclamar */}
            <button
              onClick={onReclamar}
              className="rounded-2xl p-5 flex flex-col gap-3 text-left transition-all hover:shadow-md active:scale-[0.98]"
              style={{
                background: "#fff",
                color: "#1A1A18",
                border: "1.5px solid var(--border)",
                boxShadow: "0 1px 8px rgba(0,0,0,0.05)",
              }}
            >
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                style={{ background: "#FEF2F2" }}
                aria-hidden="true"
              >
                💬
              </div>
              <div>
                <p className="font-bold text-sm">Enviar reclamação</p>
                <p
                  className="text-xs mt-0.5"
                  style={{ color: "var(--muted-foreground)" }}
                >
                  Registro nesta sessão
                </p>
              </div>
              <div
                className="flex items-center gap-1 text-xs font-semibold"
                style={{ color: "#CC2C2C" }}
              >
                Registrar
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </button>
          </div>
        </div>
    </>
  )
}
