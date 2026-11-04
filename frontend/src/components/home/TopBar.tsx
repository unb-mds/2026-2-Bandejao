import { useMemo } from 'react'

export interface TopBarProps {
  hoje: Date
  campusName: string
  restauranteName: string
}

export default function TopBar({ hoje, campusName, restauranteName }: TopBarProps) {
  const dataFormatada = useMemo(
    () =>
      hoje.toLocaleDateString("pt-BR", {
        weekday: "long",
        day: "numeric",
        month: "long",
      }),
    [hoje],
  )

  return (
    <>
      {/* ── Top bar ── */}
      <div
        className="sticky top-0 z-20 px-5 py-3 flex items-center justify-between"
        style={{
          background: "#0f2d1a",
          borderBottom: "1px solid rgba(201,168,76,0.15)",
        }}
      >
        {/* Logo area */}
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-xl flex items-center justify-center text-sm font-black"
            style={{
              background: "linear-gradient(135deg,#C9A84C,#e8c96a)",
              color: "#0f2d1a",
            }}
            aria-hidden="true"
          >
            B
          </div>
          <div>
            <p className="text-white font-bold text-sm leading-none">
              Bandejão UnB
            </p>
            <p
              className="text-[10px] leading-tight"
              style={{ color: "rgba(168,213,181,0.6)" }}
            >
              {campusName}
              {restauranteName !== campusName ? ` — ${restauranteName}` : ""}
            </p>
          </div>
        </div>

        {/* Date chip */}
        <div
          className="px-3 py-1.5 rounded-full text-[10px] font-semibold capitalize"
          style={{
            background: "rgba(255,255,255,0.08)",
            color: "rgba(168,213,181,0.8)",
          }}
        >
          {dataFormatada}
        </div>
      </div>
    </>
  )
}
