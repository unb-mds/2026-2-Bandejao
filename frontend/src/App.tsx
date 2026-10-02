import { useState, useRef, useMemo, useEffect } from 'react'
import HomeScreen from '@/screens/HomeScreen'
import A11yFloat from '@/components/A11yFloat'
import AppFooter from '@/components/AppFooter'
import AppHeader from '@/components/AppHeader'
import AppNav from '@/components/AppNav'
import AvaliarTab from '@/screens/AvaliarTab'
import CardapioTab from '@/screens/CardapioTab'
import LotacaoTab from '@/screens/LotacaoTab'

import { DIAS_SEMANA } from './data'
import { listarCampi, listarCardapios } from './api'
import type { CardapioApi } from './api'
import { inicioSemana, dataDaSemana, montarSemana } from './cardapios'
import type { Campus } from './types'
import type { Avaliacao, NivelLotacao, Reclamacao, Refeicao, ReportLotacao } from './types'
import { getCurrentMealInfo } from './utils'

export default function App() {
  const [campi, setCampi] = useState<Campus[]>([])
  const [campus, setCampus] = useState<Campus>({ id: '', name: 'Selecione um campus' })
  const [semanaInicio, setSemanaInicio] = useState(() => inicioSemana(new Date()))
  const [cardapiosApi, setCardapiosApi] = useState<CardapioApi[]>([])
  const [estadoCampi, setEstadoCampi] = useState<'carregando' | 'pronto' | 'erro'>('carregando')
  const [estadoCardapiosResultado, setEstadoCardapios] = useState<'inativo' | 'carregando' | 'pronto' | 'erro'>('inativo')
  const [erroCampi, setErroCampi] = useState('')
  const [erroCardapiosResultado, setErroCardapios] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [consultaCarregada, setConsultaCarregada] = useState('')
  const consultaAtual = `${campus.id}:${semanaInicio}:${tentativa}`
  const resultadoAtual = consultaCarregada === consultaAtual
  const estadoCardapios = resultadoAtual ? estadoCardapiosResultado : campus.id ? 'carregando' : 'inativo'
  const erroCardapios = resultadoAtual ? erroCardapiosResultado : ''

  useEffect(() => {
    const controller = new AbortController()
    listarCampi({ signal: controller.signal }).then(resultado => {
      if (controller.signal.aborted) return
      const disponiveis = resultado.map(c => ({ id: String(c.id), name: c.nome }))
      setCampi(disponiveis)
      setCampus(atual => disponiveis.find(c => c.id === atual.id) ?? disponiveis[0] ?? { id: '', name: 'Nenhum campus disponível' })
      setEstadoCampi('pronto')
    }).catch((erro: unknown) => {
      if (controller.signal.aborted) return
      setErroCampi(erro instanceof Error ? erro.message : 'Erro ao carregar campi.')
      setEstadoCampi('erro')
    })
    return () => controller.abort()
  }, [tentativa])

  useEffect(() => {
    if (!campus.id || estadoCampi !== 'pronto') return
    const controller = new AbortController()
    const chave = `${campus.id}:${semanaInicio}:${tentativa}`
    listarCardapios({ campus_id: campus.id, data_inicio: semanaInicio, data_fim: dataDaSemana(semanaInicio, 6) }, { signal: controller.signal })
      .then(resultado => {
        if (controller.signal.aborted) return
        setConsultaCarregada(chave)
        setErroCardapios('')
        setCardapiosApi(resultado)
        setEstadoCardapios('pronto')
      }).catch((erro: unknown) => {
        if (controller.signal.aborted) return
        setConsultaCarregada(chave)
        setCardapiosApi([])
        setErroCardapios(erro instanceof Error ? erro.message : 'Erro ao carregar cardápios.')
        setEstadoCardapios('erro')
      })
    return () => controller.abort()
  }, [campus.id, semanaInicio, estadoCampi, tentativa])
  const [refeicao, setRefeicao] = useState<Refeicao>('almoco')
  const [tab, setTab] = useState<'hoje' | 'cardapio' | 'lotacao' | 'avaliar'>('hoje')
  const [diaSemana, setDiaSemana] = useState<number>(new Date().getDay())
  const [tabAvaliar, setTabAvaliar] = useState<'form' | 'historico' | 'reclamacao'>('form')

  const [refeicoesPlanejadas, setRefeicoesPlanejadas] = useState<Set<string>>(new Set())
  const togglePlanejada = (dia: number, tipo: Refeicao) => {
    const key = `${campus.id}:${dataDaSemana(semanaInicio, dia)}:${tipo}`
    setRefeicoesPlanejadas(prev => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }
  const isPlanejada = (dia: number, tipo: Refeicao) => refeicoesPlanejadas.has(`${campus.id}:${dataDaSemana(semanaInicio, dia)}:${tipo}`)

  const [agora, setAgora] = useState(() => Date.now())
  useEffect(() => {
    const timer = setInterval(() => setAgora(Date.now()), 60000)
    return () => clearInterval(timer)
  }, [])

  const [lotacaoReports, setLotacaoReports] = useState<ReportLotacao[]>([])
  const [lotacaoEnviada, setLotacaoEnviada] = useState(false)
  const [lotacaoNivel, setLotacaoNivel] = useState<NivelLotacao | null>(null)

  const reportarLotacao = () => {
    if (!lotacaoNivel) return
    setLotacaoReports(prev => [...prev, { campus: campus.name, restaurante: '', nivel: lotacaoNivel, timestamp: Date.now() }])
    setLotacaoEnviada(true)
    setLotacaoNivel(null)
    setTimeout(() => setLotacaoEnviada(false), 2500)
  }

  const getLotacaoStats = (campusName: string) => {
    const recentes = lotacaoReports.filter(r => r.campus === campusName && agora - r.timestamp < 3600000)
    const total = recentes.length
    if (total === 0) return null
    const counts = { vazio: 0, moderado: 0, cheio: 0 }
    recentes.forEach(r => counts[r.nivel]++)
    const predominante = (Object.entries(counts) as [NivelLotacao, number][]).sort((a, b) => b[1] - a[1])[0][0]
    return { total, counts, predominante }
  }

  const currentLotacao = getLotacaoStats(campus.name)
  const lotacaoLabel = currentLotacao?.predominante === 'cheio' ? 'Alto movimento' :
                       currentLotacao?.predominante === 'moderado' ? 'Movimento moderado' : 'Tranquilo'
  const lotacaoEmoji = currentLotacao?.predominante === 'cheio' ? '🔴' :
                       currentLotacao?.predominante === 'moderado' ? '🟡' : '🟢'
  const lotacaoColor = currentLotacao?.predominante === 'cheio' ? '#EF4444' :
                       currentLotacao?.predominante === 'moderado' ? '#F59E0B' : '#22C55E'

  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[]>([])
  const [reclamacoes, setReclamacoes] = useState<Reclamacao[]>([])

  const [avNome, setAvNome] = useState('')
  const [avSabor, setAvSabor] = useState(0)
  const [avSal, setAvSal] = useState(0)
  const [avTemp, setAvTemp] = useState(0)
  const [avApres, setAvApres] = useState(0)
  const [avQtd, setAvQtd] = useState(0)
  const [avGeral, setAvGeral] = useState(0)
  const [avComentario, setAvComentario] = useState('')
  const [avFoto, setAvFoto] = useState<string | undefined>()
  const [avSuccess, setAvSuccess] = useState(false)

  const [recNome, setRecNome] = useState('')
  const [recCategoria, setRecCategoria] = useState('Qualidade da comida')
  const [recDescricao, setRecDescricao] = useState('')
  const [recFoto, setRecFoto] = useState<string | null>(null)
  const [recSuccess, setRecSuccess] = useState(false)
  const recFotoRef = useRef<HTMLInputElement>(null)

  const fileRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)

  const handleCampusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const c = campi.find(x => x.id === e.target.value)
    if (!c) return
    setCampus(c)
  }

  const handleFoto = (file: File) => {
    const reader = new FileReader()
    reader.onload = () => setAvFoto(reader.result as string)
    reader.readAsDataURL(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file?.type.startsWith('image/')) handleFoto(file)
  }

  const handleSubmitAvaliacao = (e: React.FormEvent) => {
    e.preventDefault()
    if (!avSabor || !avSal || !avTemp || !avApres || !avQtd || !avGeral) return
    const nova: Avaliacao = {
      id: crypto.randomUUID(), autor: avNome || 'Anônimo',
      refeicao: cardapioDia[refeicao].label,
      campus: campus.name,
      sabor: avSabor, sal: avSal, temperatura: avTemp,
      apresentacao: avApres, quantidade: avQtd, geral: avGeral,
      comentario: avComentario, foto: avFoto,
      data: new Date().toLocaleDateString('pt-BR'),
      horario: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
    }
    setAvaliacoes(prev => [nova, ...prev])
    setAvNome(''); setAvSabor(0); setAvSal(0); setAvTemp(0); setAvApres(0); setAvQtd(0); setAvGeral(0)
    setAvComentario(''); setAvFoto(undefined)
    setAvSuccess(true)
    setTimeout(() => { setAvSuccess(false); setTab('avaliar'); setTabAvaliar('historico') }, 1800)
  }

  const submitReclamacao = (e: React.FormEvent) => {
    e.preventDefault()
    if (!recDescricao.trim()) return
    const nova: Reclamacao = {
      id: Date.now(), autor: recNome || 'Anônimo', categoria: recCategoria,
      descricao: recDescricao,
      data: new Date().toLocaleDateString('pt-BR'),
      horario: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
      status: 'Aberta',
    }
    setReclamacoes(prev => [nova, ...prev])
    setRecNome(''); setRecDescricao(''); setRecCategoria('Qualidade da comida'); setRecFoto(null)
    setRecSuccess(true)
    setTimeout(() => setRecSuccess(false), 3000)
  }

  // ── Cardápio do campus atual ──
  const cardapioSemana = useMemo(() => montarSemana(resultadoAtual ? cardapiosApi : [], semanaInicio), [cardapiosApi, semanaInicio, resultadoAtual])
  const cardapioDia = cardapioSemana[diaSemana]
  const cardapio = cardapioDia[refeicao]
  const diasDisponiveis = [0,1,2,3,4,5,6]

  // ── Avaliações e média por campus ──
  const avaliacoesDoCampus = avaliacoes.filter(a => !a.campus || a.campus === campus.name)
  const mediaGeral = avaliacoesDoCampus.length
    ? (avaliacoesDoCampus.reduce((s, a) => s + a.geral, 0) / avaliacoesDoCampus.length).toFixed(1) : '—'

  const hoje = new Date(agora)
  const hojeIdx = hoje.getDay()
  const hojeCardapio = cardapioSemana[hojeIdx]
  const mealInfo = getCurrentMealInfo()
  const hojeMeal = hojeCardapio[mealInfo.tipo]
  const planejadosCount = [...refeicoesPlanejadas].filter(key => key.startsWith(`${campus.id}:`) && key.split(':')[1] >= semanaInicio && key.split(':')[1] <= dataDaSemana(semanaInicio, 6)).length

  const diasPlanejadosHome = diasDisponiveis.map(d => ({
      dia: d,
      label: DIAS_SEMANA[d],
      planejado: (['cafe','almoco','jantar'] as Refeicao[]).some(r => isPlanejada(d, r)),
    }))

  const [a11yOpen, setA11yOpen] = useState(false)
  const [fontSize, setFontSize] = useState<'normal' | 'grande' | 'maior'>('normal')
  const [altoContraste, setAltoContraste] = useState(false)
  const [espacamento, setEspacamento] = useState(false)
  const [sublinharLinks, setSublinharLinks] = useState(false)

  return (
    <div
      className={`min-h-screen ${espacamento ? 'tracking-wide leading-loose' : ''} ${sublinharLinks ? 'underline-links' : ''} ${altoContraste ? 'alto-contraste' : ''}`}
      style={{ background: 'var(--background)', color: 'var(--foreground)' }}
    >
      <a href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:rounded-lg focus:font-semibold focus:text-sm focus:text-white focus:shadow-lg"
        style={{ background: 'var(--primary)' }}>
        Pular para o conteúdo
      </a>

    <A11yFloat a11yOpen={a11yOpen} setA11yOpen={setA11yOpen} fontSize={fontSize} setFontSize={setFontSize} altoContraste={altoContraste} setAltoContraste={setAltoContraste} espacamento={espacamento} setEspacamento={setEspacamento} sublinharLinks={sublinharLinks} setSublinharLinks={setSublinharLinks} />

    <AppHeader campi={campi} campus={campus} hoje={hoje} mediaGeral={mediaGeral} totalAvaliacoes={avaliacoesDoCampus.length} planejadosCount={planejadosCount} handleCampusChange={handleCampusChange} />

    <AppNav tab={tab} setTab={novaTab => { if (novaTab === 'hoje') setSemanaInicio(inicioSemana(new Date())); setTab(novaTab) }} />

      <main id="main-content" style={{ scrollMarginTop: '60px', background: 'var(--background)' }}>

        <section className="max-w-5xl mx-auto px-4 py-4 space-y-3" aria-label="Consulta de cardápios">
          {(tab === 'hoje' || tab === 'cardapio') && <label className="flex flex-wrap items-center gap-3 text-sm font-semibold">
            Semana do cardápio
            <input className="rounded-lg border border-border bg-card px-3 py-2" type="date" value={semanaInicio}
              onChange={e => { if (e.target.value) { setSemanaInicio(inicioSemana(new Date(`${e.target.value}T12:00:00`))); setTab('cardapio') } }} />
            <span className="text-muted-foreground font-normal">Até {new Date(`${dataDaSemana(semanaInicio, 6)}T12:00:00`).toLocaleDateString('pt-BR')}</span>
          </label>}
          {estadoCampi === 'carregando' && <p role="status">Carregando campi…</p>}
          {estadoCampi === 'pronto' && campi.length === 0 && <p role="status">Nenhum campus cadastrado. Os cardápios serão exibidos quando estiverem disponíveis.</p>}
          {(erroCampi || erroCardapios) && <div role="alert" className="rounded-xl border border-red-300 p-4">
            <p>Não foi possível consultar os dados. {erroCampi || erroCardapios}</p>
            <button className="mt-2 underline" onClick={() => { setEstadoCampi('carregando'); setErroCampi(''); setTentativa(valor => valor + 1) }}>Tentar novamente</button>
          </div>}
          {estadoCampi === 'pronto' && estadoCardapios === 'carregando' && <p role="status">Carregando cardápios…</p>}
          {estadoCampi === 'pronto' && estadoCardapios === 'pronto' && cardapiosApi.length === 0 && <p role="status">Nenhum cardápio publicado para esta semana. Isso não confirma que o RU esteja fechado.</p>}
          <p className="text-xs text-muted-foreground">Avaliações, reclamações e planejamento são demonstrações nesta versão: os registros ficam apenas nesta sessão e não são enviados ao RU. A tela de lotação usa exemplos, sem estimativa real.</p>
        </section>
        {tab === 'hoje' && estadoCampi === 'pronto' && estadoCardapios === 'pronto' && campus.id && (
          <div id="panel-hoje" role="tabpanel" aria-labelledby="tab-hoje">
            <HomeScreen
              hoje={hoje}
              campusName={campus.name}
              restauranteName={campus.name}
              mealTipo={mealInfo.tipo}
              mealStatus={mealInfo.status}
              mealData={hojeMeal}
              lotacao={currentLotacao}
              planejadosCount={planejadosCount}
              diasPlanejados={diasPlanejadosHome}
              mediaAvaliacoes={mediaGeral}
              totalAvaliacoes={avaliacoesDoCampus.length}
              avaliacoesHoje={avaliacoesDoCampus.filter(a => {
                if (!hojeMeal || a.refeicao !== hojeMeal.label) return false
                const hojeStr = hoje.toLocaleDateString('pt-BR')
                return a.data === hojeStr || a.data === 'hoje'
              })}
              onVerCardapio={() => { setSemanaInicio(inicioSemana(new Date())); setTab('cardapio'); setDiaSemana(hojeIdx); setRefeicao(mealInfo.tipo) }}
              onVerLotacao={() => setTab('lotacao')}
              onAvaliar={() => { setTab('avaliar'); setTabAvaliar('form'); setRefeicao(mealInfo.tipo) }}
              onVerHistorico={() => { setTab('avaliar'); setTabAvaliar('historico') }}
              onReclamar={() => { setTab('avaliar'); setTabAvaliar('reclamacao') }}
              onPlanejar={() => { setSemanaInicio(inicioSemana(new Date())); setTab('cardapio'); setDiaSemana(hojeIdx) }}
            />
          </div>
        )}

    {tab === 'cardapio' && estadoCampi === 'pronto' && estadoCardapios === 'pronto' && campus.id && (
      <CardapioTab cardapioDia={cardapioDia} diaSemana={diaSemana} setDiaSemana={setDiaSemana} diasDisponiveis={diasDisponiveis} refeicao={refeicao} setRefeicao={setRefeicao} isPlanejada={isPlanejada} planejadosCount={planejadosCount} cardapio={cardapio} togglePlanejada={togglePlanejada} />
    )}

    {tab === 'lotacao' && campus.id && (
      <LotacaoTab campus={campus} currentLotacao={currentLotacao} lotacaoLabel={lotacaoLabel} lotacaoEmoji={lotacaoEmoji} lotacaoColor={lotacaoColor} lotacaoEnviada={lotacaoEnviada} lotacaoNivel={lotacaoNivel} setLotacaoNivel={setLotacaoNivel} reportarLotacao={reportarLotacao} getLotacaoStats={getLotacaoStats} />
    )}

    {tab === 'avaliar' && campus.id && (
      <AvaliarTab
        tabAvaliar={tabAvaliar}
        setTabAvaliar={setTabAvaliar}
        formProps={{ cardapioDia, refeicao, setRefeicao, campus, avNome, setAvNome, avSabor, setAvSabor, avSal, setAvSal, avTemp, setAvTemp, avApres, setAvApres, avQtd, setAvQtd, avGeral, setAvGeral, avComentario, setAvComentario, avFoto, setAvFoto, avSuccess, fileRef, dragging, setDragging, handleFoto, handleDrop, submitAvaliacao: handleSubmitAvaliacao }}
        historicoProps={{ avaliacoes: avaliacoesDoCampus, mediaGeral, setTab }}
        reclamacoesProps={{ recSuccess, recCategoria, setRecCategoria, recNome, setRecNome, recDescricao, setRecDescricao, recFoto, setRecFoto, recFotoRef, submitReclamacao, reclamacoes }}
      />
    )}
      </main>

    <AppFooter campus={campus} />
  </div>
  )
}