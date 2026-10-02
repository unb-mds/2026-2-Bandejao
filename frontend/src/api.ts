export interface CampusApi { id: number; nome: string }
export interface ItemApi {
  id: number
  categoria: string
  tipo_dieta: string
  nome: string
  contem_leite: boolean
  contem_ovo: boolean
  contem_gluten: boolean
  contem_cogumelo: boolean
  contem_amendoim: boolean
  contem_mel: boolean
  contem_soja: boolean
  contem_pimenta: boolean
  contem_oleaginosas: boolean
  contem_carne_suina: boolean
  contem_frutos_do_mar: boolean
}
export interface CardapioApi {
  id: number
  campus_id: number
  data: string
  tipo_refeicao: 'cafe_da_manha' | 'almoco' | 'jantar'
  fonte_pdf_url: string | null
  itens: ItemApi[]
}
interface Opcoes {
  signal?: AbortSignal
  baseUrl?: string
  fetchImpl?: (url: URL, init: RequestInit) => Promise<Pick<Response, 'ok' | 'status' | 'json'>>
}
type Parametros = Record<string, string | number | null | undefined>
const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'

export async function requisitarJson<T>(caminho: string, parametros: Parametros = {}, opcoes: Opcoes = {}): Promise<T> {
  const { signal, fetchImpl = globalThis.fetch, baseUrl = API_BASE_URL } = opcoes
  const base = baseUrl.replace(/\/+$/, '')
  const url = new URL(caminho.replace(/^\/+/, ''), `${base}/`)
  for (const [chave, valor] of Object.entries(parametros)) {
    if (valor !== '' && valor !== null && valor !== undefined) url.searchParams.set(chave, String(valor))
  }
  const resposta = await fetchImpl(url, { signal, headers: { Accept: 'application/json' } })
  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null)
    const detalhe = typeof corpo?.detail === 'string' ? corpo.detail : null
    throw new Error(detalhe || `A API respondeu com HTTP ${resposta.status}.`)
  }
  return resposta.json()
}
export function listarCampi(opcoes?: Opcoes) {
  return requisitarJson<CampusApi[]>('campi/', {}, opcoes)
}
export function listarCardapios(filtros: Parametros, opcoes?: Opcoes) {
  return requisitarJson<CardapioApi[]>('cardapios/', filtros, opcoes)
}
