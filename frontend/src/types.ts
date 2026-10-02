export type ItemCardapio = string | { nome: string; alergenos?: string[] }

export type Refeicao = 'cafe' | 'almoco' | 'jantar'

export type Tab = 'hoje' | 'cardapio' | 'lotacao' | 'avaliar'

export type TabAvaliar = 'form' | 'historico' | 'reclamacao'

export type MealStatus = 'agora' | 'proxima' | 'encerrado'

export type FontSize = 'normal' | 'grande' | 'maior'

export type CardapiosPorCampus = Record<string, CardapioRefeicoes[]>

export interface Campus {
  id: string
  name: string
}

export type RefeicaoData = {
  id?: number
  data?: string
  fontePdfUrl?: string | null
  itensApi?: import('./api').ItemApi[]
  label: string; horario: string
  prato_principal: ItemCardapio
  opcao_vegetariana: ItemCardapio
  guarnicao: ItemCardapio[]; acompanhamentos: ItemCardapio[]; saladas: ItemCardapio[]; sobremesa: ItemCardapio; suco: string;
  alergenos?: string[]
  // Almoco/Jantar extra
  salada1?: ItemCardapio; salada2?: ItemCardapio; molho_salada?: ItemCardapio; bebida?: ItemCardapio;
  // Cafe extra
  complemento_vegetariano_estrito?: ItemCardapio; opcao_extra?: ItemCardapio; gordura?: ItemCardapio;
  // Dietary
  vegetariano_estrito?: ItemCardapio
}
export type CardapioRefeicoes = { cafe: RefeicaoData; almoco: RefeicaoData; jantar: RefeicaoData }

export interface AvaliacaoLive {
  campus?: string
  id: number | string
  autor: string
  data: string
  horario?: string
  refeicao: string
  geral: number
  comentario: string
  foto?: string | null
}

export interface Reclamacao {
  id: number; autor: string; categoria: string; descricao: string;
  data: string; horario: string; status: 'Aberta' | 'Resolvida';
}

export interface LotacaoStats {
  total: number
  counts: { vazio: number; moderado: number; cheio: number }
  predominante: "vazio" | "moderado" | "cheio"
}

export type NivelLotacao = 'vazio' | 'moderado' | 'cheio'
export type ReportLotacao = { campus: string; restaurante: string; nivel: NivelLotacao; timestamp: number }

export interface DiaPlanejado {
  dia: number
  label: string
  planejado: boolean
}

export interface CategoriaReclamacao {
  id: string
  emoji: string
  label: string
}

export interface FiltrosAlimentares {
  vegetariano: boolean
  vegetarianoEstrito: boolean
  alergenos: string[]
}


export interface Avaliacao {
  id: number | string
  autor: string
  refeicao: string
  campus?: string          // ← novo
  sabor?: number
  sal?: number
  temperatura?: number
  apresentacao?: number
  quantidade?: number
  geral: number
  comentario: string
  foto?: string | null
  data: string
  horario?: string
}