import type { CategoriaReclamacao, Refeicao } from '@/types'

export const ALERGENOS_MAP: Record<string, { label: string; emoji: string; color: string }> = {
  trigo:      { label: 'Trigo/Glúten', emoji: '🌾', color: '#D4A017' },
  soja:       { label: 'Soja',         emoji: '🫘', color: '#7CB518' },
  leite:      { label: 'Leite',        emoji: '🥛', color: '#4A90D9' },
  ovo:        { label: 'Ovo',          emoji: '🥚', color: '#E8A020' },
  amendoim:   { label: 'Amendoim',     emoji: '🥜', color: '#B5651D' },
  oleaginosa: { label: 'Oleaginosa',   emoji: '🌰', color: '#8B4513' },
  suino:      { label: 'Suíno',        emoji: '🐷', color: '#D4748B' },
  pimenta:    { label: 'Pimenta',      emoji: '🌶️', color: '#CC2200' },
  mel:        { label: 'Mel',          emoji: '🍯', color: '#C8960C' },
  cogumelo:   { label: 'Cogumelo',     emoji: '🍄', color: '#8B7355' },
}

export const DIAS_SEMANA = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
export const DIAS_SEMANA_COMPLETO = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

// ═══════════════════════════════════════════════════════════════
// Lotação
// ═══════════════════════════════════════════════════════════════
export const LOTACAO_TIMELINE: Record<Refeicao, { hora: string; pct: number }[]> = {
  cafe: [
    { hora: '7h', pct: 30 }, { hora: '7h30', pct: 55 }, { hora: '8h', pct: 75 },
    { hora: '8h30', pct: 60 }, { hora: '9h', pct: 35 }, { hora: '9h30', pct: 15 },
  ],
  almoco: [
    { hora: '11h', pct: 25 }, { hora: '11h30', pct: 60 }, { hora: '12h', pct: 90 },
    { hora: '12h30', pct: 95 }, { hora: '13h', pct: 85 }, { hora: '13h30', pct: 55 },
    { hora: '14h', pct: 30 }, { hora: '14h30', pct: 10 },
  ],
  jantar: [
    { hora: '17h', pct: 20 }, { hora: '17h30', pct: 50 }, { hora: '18h', pct: 80 },
    { hora: '18h30', pct: 85 }, { hora: '19h', pct: 55 }, { hora: '19h30', pct: 20 },
  ],
}

export const CATEGORIAS_RECLAMACAO: CategoriaReclamacao[] = [
  { id: 'Qualidade da comida', emoji: '🍽️', label: 'Qualidade' },
  { id: 'Higiene', emoji: '🧼', label: 'Higiene' },
  { id: 'Atendimento', emoji: '👥', label: 'Atendimento' },
  { id: 'Quantidade', emoji: '🍛', label: 'Quantidade' },
  { id: 'Infraestrutura', emoji: '🏠', label: 'Estrutura' },
  { id: 'Outro', emoji: '💬', label: 'Outro' },
]

export const SAUDACOES = {
  manha: "Bom dia",
  tarde: "Boa tarde",
  noite: "Boa noite",
}

export const MEAL_ICONS: Record<Refeicao, string> = {
  cafe: "☕",
  almoco: "🍽️",
  jantar: "🌙",
}

export const MEAL_COLORS: Record<Refeicao, { from: string; to: string }> = {
  cafe: { from: "#7C4A1E", to: "#A3622A" },
  almoco: { from: "#1E5631", to: "#2D6A3F" },
  jantar: { from: "#1A2E4A", to: "#243D5E" },
}

export const LOTACAO_INFO = {
  vazio: { emoji: "🟢", label: "Tranquilo", color: "#22C55E", bg: "#F0FDF4" },
  moderado: { emoji: "🟡", label: "Moderado", color: "#F59E0B", bg: "#FFFBEB" },
  cheio: {
    emoji: "🔴",
    label: "Alto movimento",
    color: "#EF4444",
    bg: "#FEF2F2",
  },
}

export const MELHOR_HORARIO: Record<Refeicao, string> = {
  cafe: "7h – 7h30",
  almoco: "11h – 11h30",
  jantar: "17h – 17h30",
}

export const LOTACAO_BAR: Record<Refeicao, number[]> = {
  cafe: [30, 55, 75, 60, 35, 15],
  almoco: [25, 60, 90, 95, 85, 55, 30, 10],
  jantar: [20, 50, 80, 85, 55, 20],
}

export const LOTACAO_HOURS: Record<Refeicao, string[]> = {
  cafe: ["7h", "", "8h", "", "9h", ""],
  almoco: ["11h", "", "12h", "", "13h", "", "14h", ""],
  jantar: ["17h", "", "18h", "", "19h", ""],
}