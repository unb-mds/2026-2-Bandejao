/**
 * HOME — HOJE NO RU
 * Artboard independente. Não altera nenhuma tela existente.
 */
import AvaliacoesDiaLinks from '@/components/home/AvaliacoesDiaLinks'
import CommunityMini from '@/components/home/CommunityMini'
import FeedbackCTA from '@/components/home/FeedbackCTA'
import GreetingHeader from '@/components/home/GreetingHeader'
import LiveReviews from '@/components/home/LiveReviews'
import LotacaoAgora from '@/components/home/LotacaoAgora'
import MealCard from '@/components/home/MealCard'
import PlanejamentoSemana from '@/components/home/PlanejamentoSemana'
import TopBar from '@/components/home/TopBar'
import type { Avaliacao, DiaPlanejado, LotacaoStats, Refeicao, RefeicaoData } from '@/types'

export interface HomeScreenProps {
  hoje: Date
  campusName: string
  restauranteName: string
  mealTipo: Refeicao
  mealStatus: "agora" | "proxima" | "encerrado"
  mealData: RefeicaoData
  lotacao: LotacaoStats | null
  planejadosCount: number
  diasPlanejados: DiaPlanejado[]
  mediaAvaliacoes: string
  totalAvaliacoes: number
  avaliacoesHoje: Avaliacao[]
  onVerCardapio: () => void
  onVerLotacao: () => void
  onAvaliar: () => void
  onVerHistorico: () => void
  onReclamar: () => void
  onPlanejar: () => void
}

// ── Detecta se a refeição tem conteúdo real (não é placeholder) ──
function temRefeicao(mealData: RefeicaoData | undefined | null): boolean {
  if (!mealData) return false
  if (mealData.itensApi) return mealData.itensApi.length > 0
  const prato = mealData.prato_principal
  if (prato === '—') return false
  if (typeof prato === 'object' && prato?.nome === '—') return false
  return true
}

export default function HomeScreen({
  hoje,
  campusName,
  restauranteName,
  mealTipo,
  mealStatus,
  mealData,
  lotacao,
  planejadosCount,
  diasPlanejados = [],
  mediaAvaliacoes,
  totalAvaliacoes,
  avaliacoesHoje = [],
  onVerCardapio,
  onVerLotacao,
  onAvaliar,
  onVerHistorico,
  onReclamar,
  onPlanejar,
}: HomeScreenProps) {
  const temComida = temRefeicao(mealData)

  return (
    <div
      className="min-h-screen"
      style={{ background: "var(--background)", color: "var(--foreground)" }}
    >
      <TopBar hoje={hoje} campusName={campusName} restauranteName={restauranteName} />
      <div className="max-w-lg mx-auto px-4 pt-6 pb-32 space-y-5">
        <GreetingHeader hoje={hoje} />
        <PlanejamentoSemana diasPlanejados={diasPlanejados} planejadosCount={planejadosCount} onPlanejar={onPlanejar} />

        {temComida ? (
          <>
            <MealCard
              mealTipo={mealTipo}
              mealStatus={mealStatus}
              mealData={mealData}
              onVerCardapio={onVerCardapio}
            />
            <LiveReviews
              avaliacoesHoje={avaliacoesHoje}
              mealData={mealData}
              restauranteName={restauranteName}
              mealStatus={mealStatus}
              onAvaliar={onAvaliar}
            />
            <AvaliacoesDiaLinks hoje={hoje} onVerHistorico={onVerHistorico} />
            <LotacaoAgora lotacao={lotacao} mealData={mealData} mealTipo={mealTipo} onVerLotacao={onVerLotacao} />
            <FeedbackCTA totalAvaliacoes={totalAvaliacoes} mediaAvaliacoes={mediaAvaliacoes} onAvaliar={onAvaliar} onReclamar={onReclamar} />
            <CommunityMini totalAvaliacoes={totalAvaliacoes} mediaAvaliacoes={mediaAvaliacoes} />
          </>
        ) : (
          <div
            className="rounded-3xl p-6 text-center"
            style={{
              background: '#FFFBEB',
              border: '1px solid #FDE68A',
              color: '#92400E',
            }}
          >
            <span className="text-4xl block mb-3" aria-hidden="true">🔒</span>
            <h3 className="font-bold text-lg mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>
              Cardápio não disponível
            </h3>
            <p className="text-sm leading-relaxed max-w-xs mx-auto" style={{ color: '#B45309' }}>
              O <strong>{campusName}</strong> não tem itens publicados para esta refeição. Consulte a fonte oficial para confirmar o funcionamento.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}