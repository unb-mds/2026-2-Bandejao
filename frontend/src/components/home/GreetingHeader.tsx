import { getSaudacao } from '@/utils'

export interface GreetingHeaderProps {
  hoje: Date
}

export default function GreetingHeader({ hoje }: GreetingHeaderProps) {
  const saudacao = getSaudacao(hoje.getHours())
  return (
    <>
        {/* Greeting */}
        <div>
          <h1
            className="font-bold leading-tight"
            style={{
              fontSize: "clamp(1.5rem, 5vw, 2rem)",
              fontFamily: "'Playfair Display', serif",
            }}
          >
            {saudacao} <span style={{ color: "var(--primary)" }}>👋</span>
          </h1>
          <p
            className="text-sm mt-0.5"
            style={{ color: "var(--muted-foreground)" }}
          >
            Veja o que está acontecendo no RU hoje.
          </p>
        </div>
    </>
  )
}
