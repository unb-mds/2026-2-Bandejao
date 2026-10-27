export interface CampusApi {
  id: number
  nome: string
  ultima_importacao_em: string | null
  ultima_fonte_pdf_url: string | null
}
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
export interface AvaliacaoApi {
  id: number
  cardapio_id: number
  nota: number
  comentario: string | null
  criado_em: string
}
export interface AvaliacaoPayload {
  nota: number
  comentario: string | null
}
export interface ReclamacaoPayload {
  categoria: string
  descricao: string
}
export interface ReclamacaoConfirmacaoApi {
  id: number
  mensagem: string
}
interface Opcoes {
  signal?: AbortSignal
  baseUrl?: string
  fetchImpl?: (url: URL, init: RequestInit) => Promise<Pick<Response, 'ok' | 'status' | 'json'>>
  method?: string
  headers?: Record<string, string>
  body?: string
}
type Parametros = Record<string, string | number | null | undefined>
const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'

interface ErroValidacaoApi {
  loc?: unknown[]
  msg?: string
  type?: string
  ctx?: Record<string, unknown>
}

function mensagemValidacao(erro: ErroValidacaoApi): string {
  const tipo = erro.type ?? ''
  const contexto = erro.ctx ?? {}

  if (tipo === 'string_too_long' && typeof contexto.max_length === 'number') {
    return `deve ter no máximo ${contexto.max_length} caracteres`
  }
  if (tipo === 'greater_than_equal' && contexto.ge !== undefined) {
    return `deve ser maior ou igual a ${contexto.ge}`
  }
  if (tipo === 'less_than_equal' && contexto.le !== undefined) {
    return `deve ser menor ou igual a ${contexto.le}`
  }
  if (tipo === 'int_parsing' || tipo === 'int_type') return 'deve ser um número inteiro'
  return erro.msg || 'possui um valor inválido'
}

export function mensagemErroApi(corpo: unknown, status: number): string {
  if (typeof corpo === 'object' && corpo !== null && 'detail' in corpo) {
    const detalhe = (corpo as { detail?: unknown }).detail
    if (typeof detalhe === 'string') return detalhe
    if (Array.isArray(detalhe) && detalhe.length > 0) {
      const erro = detalhe[0] as ErroValidacaoApi
      const campo = erro.loc?.at(-1)
      const prefixo = typeof campo === 'string' ? `Campo “${campo}”: ` : 'Dados inválidos: '
      return `${prefixo}${mensagemValidacao(erro)}.`
    }
  }
  return `A API respondeu com HTTP ${status}.`
}

export async function requisitarJson<T>(caminho: string, parametros: Parametros = {}, opcoes: Opcoes = {}): Promise<T> {
  const {
    signal,
    fetchImpl = globalThis.fetch,
    baseUrl = API_BASE_URL,
    method = 'GET',
    headers = {},
    body,
  } = opcoes
  const base = baseUrl.replace(/\/+$/, '')
  const url = new URL(caminho.replace(/^\/+/, ''), `${base}/`)
  for (const [chave, valor] of Object.entries(parametros)) {
    if (valor !== '' && valor !== null && valor !== undefined) url.searchParams.set(chave, String(valor))
  }
  const resposta = await fetchImpl(url, {
    signal,
    method,
    body,
    headers: { Accept: 'application/json', ...headers },
  })
  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null)
    throw new Error(mensagemErroApi(corpo, resposta.status))
  }
  return resposta.json()
}
export function listarCampi(opcoes?: Opcoes) {
  return requisitarJson<CampusApi[]>('campi/', {}, opcoes)
}
export function listarCardapios(filtros: Parametros, opcoes?: Opcoes) {
  return requisitarJson<CardapioApi[]>('cardapios/', filtros, opcoes)
}
export function listarAvaliacoes(cardapioId: number, opcoes?: Opcoes) {
  return requisitarJson<AvaliacaoApi[]>(`cardapios/${cardapioId}/avaliacoes/`, {}, opcoes)
}
export function salvarAvaliacao(
  cardapioId: number,
  payload: AvaliacaoPayload,
  identidade: string,
  opcoes: Opcoes = {},
) {
  return requisitarJson<AvaliacaoApi>(
    `cardapios/${cardapioId}/avaliacoes/`,
    {},
    {
      ...opcoes,
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
        'X-Identidade': identidade,
        ...opcoes.headers,
      },
    },
  )
}
export function salvarReclamacao(
  cardapioId: number,
  payload: ReclamacaoPayload,
  identidade: string,
  opcoes: Opcoes = {},
) {
  return requisitarJson<ReclamacaoConfirmacaoApi>(
    `cardapios/${cardapioId}/reclamacoes/`,
    {},
    {
      ...opcoes,
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
        'X-Identidade': identidade,
        ...opcoes.headers,
      },
    },
  )
}
