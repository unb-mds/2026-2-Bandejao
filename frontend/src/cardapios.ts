import type { CardapioApi, ItemApi } from './api'
import type { CardapioRefeicoes, ItemCardapio, Refeicao, RefeicaoData } from './types'

const ROTULOS: Record<Refeicao, string> = { cafe: 'Café da Manhã', almoco: 'Almoço', jantar: 'Jantar' }
export const CATEGORIAS: Record<string, string> = {
  bebida: 'Bebida', panificacao: 'Panificação', opcao_extra: 'Opção extra', gordura: 'Gordura',
  salada_1: 'Salada 1', salada_2: 'Salada 2', molho_salada: 'Molho da salada',
  prato_principal: 'Prato principal', guarnicao: 'Guarnição', sopa: 'Sopa', torrada: 'Torrada',
  acompanhamento: 'Acompanhamento', sobremesa: 'Sobremesa', fruta: 'Fruta',
}
export const DIETAS: Record<string, string> = {
  comum: 'Comum', padrao: 'Padrão', ovolactovegetariano: 'Ovolactovegetariano', vegetariano_estrito: 'Vegetariano estrito',
}
const ALERGENOS = {
  contem_leite: 'leite', contem_ovo: 'ovo', contem_gluten: 'trigo', contem_cogumelo: 'cogumelo',
  contem_amendoim: 'amendoim', contem_mel: 'mel', contem_soja: 'soja', contem_pimenta: 'pimenta',
  contem_oleaginosas: 'oleaginosa', contem_carne_suina: 'suino', contem_frutos_do_mar: 'frutos_do_mar',
} as const

export function alergenosDoItem(item: ItemApi): string[] {
  return Object.entries(ALERGENOS).filter(([campo]) => item[campo as keyof typeof ALERGENOS] === true).map(([, nome]) => nome)
}
export function dataLocal(data: Date): string {
  return `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, '0')}-${String(data.getDate()).padStart(2, '0')}`
}
export function inicioSemana(data: Date): string {
  const inicio = new Date(data)
  inicio.setDate(inicio.getDate() - inicio.getDay())
  return dataLocal(inicio)
}
export function dataDaSemana(inicio: string, dia: number): string {
  const data = new Date(`${inicio}T12:00:00`)
  data.setDate(data.getDate() + dia)
  return dataLocal(data)
}
export function refeicaoVazia(refeicao: Refeicao, data: string): RefeicaoData {
  return {
    label: ROTULOS[refeicao], horario: 'Consulte os horários oficiais', data,
    prato_principal: '—', opcao_vegetariana: '', guarnicao: [], acompanhamentos: [], saladas: [],
    sobremesa: '', suco: '', itensApi: [],
  }
}
function resumir(itens: ItemApi[]): ItemCardapio {
  return { nome: itens.map(item => item.nome).join(' · '), alergenos: [...new Set(itens.flatMap(alergenosDoItem))] }
}
export function adaptarCardapio(cardapio: CardapioApi): RefeicaoData {
  const ref = cardapio.tipo_refeicao === 'cafe_da_manha' ? 'cafe' : cardapio.tipo_refeicao
  const porCategoria = (categoria: string) => cardapio.itens.filter(item => item.categoria === categoria)
  const principais = porCategoria('prato_principal')
  const principal = principais.filter(item => item.tipo_dieta === 'padrao' || item.tipo_dieta === 'comum')
  return {
    ...refeicaoVazia(ref, cardapio.data), id: cardapio.id, fontePdfUrl: cardapio.fonte_pdf_url,
    itensApi: cardapio.itens,
    prato_principal: resumir(principal.length ? principal : principais.length ? principais : cardapio.itens.slice(0, 1)),
    opcao_vegetariana: resumir(principais.filter(item => item.tipo_dieta === 'ovolactovegetariano')),
    vegetariano_estrito: resumir(principais.filter(item => item.tipo_dieta === 'vegetariano_estrito')),
    guarnicao: [...porCategoria('guarnicao'), ...porCategoria('panificacao')].map(item => resumir([item])),
    acompanhamentos: porCategoria('acompanhamento').map(item => resumir([item])),
    saladas: [...porCategoria('salada_1'), ...porCategoria('salada_2')].map(item => resumir([item])),
    sobremesa: resumir([...porCategoria('fruta'), ...porCategoria('sobremesa')]),
    bebida: resumir(porCategoria('bebida')), alergenos: [...new Set(cardapio.itens.flatMap(alergenosDoItem))],
  }
}
export function montarSemana(cardapios: CardapioApi[], inicio: string): CardapioRefeicoes[] {
  const semana = Array.from({ length: 7 }, (_, dia) => {
    const data = dataDaSemana(inicio, dia)
    return { cafe: refeicaoVazia('cafe', data), almoco: refeicaoVazia('almoco', data), jantar: refeicaoVazia('jantar', data) }
  })
  for (const cardapio of cardapios) {
    const dia = semana.findIndex(refeicoes => refeicoes.cafe.data === cardapio.data)
    if (dia < 0) continue
    const ref = cardapio.tipo_refeicao === 'cafe_da_manha' ? 'cafe' : cardapio.tipo_refeicao
    semana[dia][ref] = adaptarCardapio(cardapio)
  }
  return semana
}
