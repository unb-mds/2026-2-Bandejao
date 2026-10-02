import { SAUDACOES } from "@/data";
import type { ItemCardapio, Refeicao, FiltrosAlimentares, RefeicaoData } from '@/types'

export function iNome(item: ItemCardapio): string {
  return typeof item === 'string' ? item : item.nome
}
export function iAlerg(item: ItemCardapio): string[] {
  return typeof item === 'string' ? [] : (item.alergenos ?? [])
}

export function getFruitEmoji(nome: string): string {
  const n = nome.toLowerCase()
  if (n.includes('melão')) return '🍈'
  if (n.includes('banana')) return '🍌'
  if (n.includes('abacaxi')) return '🍍'
  if (n.includes('manga')) return '🥭'
  if (n.includes('uva')) return '🍇'
  if (n.includes('maçã')) return '🍎'
  if (n.includes('pera')) return '🍐'
  if (n.includes('laranja') || n.includes('maracujá')) return '🍊'
  if (n.includes('melancia')) return '🍉'
  if (n.includes('mamão')) return '🍑'
  return '🍓'
}

export function getCurrentMealInfo(): { tipo: Refeicao; status: 'agora' | 'proxima' | 'encerrado' } {
  const now = new Date()
  const mins = now.getHours() * 60 + now.getMinutes()

  // Café: 07:00 às 09:30
  if (mins >= 7 * 60 && mins <= 9 * 60 + 30) return { tipo: 'cafe', status: 'agora' }
  // Almoço: 11:00 às 14:30
  if (mins >= 11 * 60 && mins <= 14 * 60 + 30) return { tipo: 'almoco', status: 'agora' }
  // Jantar: 17:00 às 19:30
  if (mins >= 17 * 60 && mins <= 19 * 60 + 30) return { tipo: 'jantar', status: 'agora' }

  if (mins < 7 * 60) return { tipo: 'cafe', status: 'proxima' }
  if (mins < 11 * 60) return { tipo: 'almoco', status: 'proxima' }
  if (mins < 17 * 60) return { tipo: 'jantar', status: 'proxima' }

  return { tipo: 'jantar', status: 'encerrado' }
}

export function getLotacaoColorClass(pct: number): string {
  if (pct >= 75) return '#EF4444'
  if (pct >= 45) return '#F59E0B'
  return '#22C55E'
}

export function getSaudacao(h: number) {
  if (h < 12) return SAUDACOES.manha
  if (h <= 18) return SAUDACOES.tarde
  return SAUDACOES.noite
}

export function getLotacaoColor(pct: number) {
  if (pct >= 75) return "#EF4444"
  if (pct >= 45) return "#F59E0B"
  return "#22C55E"
}

export function passaNoFiltro(data: RefeicaoData, filtros: FiltrosAlimentares): boolean {
  // Filtro vegetariano (ovolacto)
  if (filtros.vegetariano && !data.opcao_vegetariana) return false

  // Filtro vegetariano estrito
  if (filtros.vegetarianoEstrito && !data.vegetariano_estrito) return false

  // Filtro de alérgenos
  if (filtros.alergenos.length > 0) {
    // 1. Checar alérgenos no nível da refeição (data.alergenos)
    const temAlergenoNaRefeicao = filtros.alergenos.some(a =>
      (data.alergenos ?? []).includes(a)
    )
    if (temAlergenoNaRefeicao) return false

    // 2. Checar alérgenos nos itens individuais
    const todosItens: ItemCardapio[] = [
      data.prato_principal,
      data.opcao_vegetariana,
      data.vegetariano_estrito,
      data.opcao_extra,
      data.gordura,
      data.molho_salada,
      data.salada1,
      data.salada2,
      data.bebida,
      data.sobremesa,
      ...data.guarnicao,
      ...data.acompanhamentos,
      ...data.saladas,
    ].filter((i): i is ItemCardapio => i !== undefined)

    const temAlergenoNosItens = todosItens.some(item =>
      filtros.alergenos.some(a => iAlerg(item).includes(a))
    )
    if (temAlergenoNosItens) return false
  }

  return true
}