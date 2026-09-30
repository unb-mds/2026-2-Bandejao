import { useEffect, useState } from 'react'

import { listarCampi, listarCardapios } from './api.js'
import './App.css'

const REFEICOES = {
  cafe_da_manha: 'Café da manhã',
  almoco: 'Almoço',
  jantar: 'Jantar',
}
const ORDEM_REFEICOES = Object.keys(REFEICOES)

const CATEGORIAS = {
  acompanhamento: 'Acompanhamento',
  bebida: 'Bebida',
  fruta: 'Fruta',
  gordura: 'Gordura',
  guarnicao: 'Guarnição',
  molho_salada: 'Molho da salada',
  opcao_extra: 'Opção extra',
  panificacao: 'Panificação',
  prato_principal: 'Prato principal',
  salada_1: 'Salada 1',
  salada_2: 'Salada 2',
  sopa: 'Sopa',
  sobremesa: 'Sobremesa',
  torrada: 'Torrada',
}

function formatarData(valor) {
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'full',
    timeZone: 'UTC',
  }).format(new Date(`${valor}T00:00:00Z`))
}

function rotuloCategoria(categoria) {
  return CATEGORIAS[categoria] || categoria.replaceAll('_', ' ')
}

function App() {
  const [campi, setCampi] = useState([])
  const [campusId, setCampusId] = useState('')
  const [dataInicio, setDataInicio] = useState('')
  const [dataFim, setDataFim] = useState('')
  const [tipoRefeicao, setTipoRefeicao] = useState('')
  const [estadoCampi, setEstadoCampi] = useState('carregando')
  const [erroCampi, setErroCampi] = useState('')
  const [consulta, setConsulta] = useState(null)
  const [cardapios, setCardapios] = useState([])
  const [estadoConsulta, setEstadoConsulta] = useState('inativa')
  const [erroConsulta, setErroConsulta] = useState('')
  const [erroFormulario, setErroFormulario] = useState('')

  useEffect(() => {
    const controller = new AbortController()
    setEstadoCampi('carregando')

    listarCampi({ signal: controller.signal })
      .then((resultado) => {
        setCampi(resultado)
        setEstadoCampi('concluida')

        if (resultado.length > 0) {
          const primeiroCampus = String(resultado[0].id)
          setCampusId(primeiroCampus)
          setConsulta({ campus_id: primeiroCampus })
        }
      })
      .catch((erro) => {
        if (erro.name === 'AbortError') return
        setErroCampi(erro.message)
        setEstadoCampi('erro')
      })

    return () => controller.abort()
  }, [])

  useEffect(() => {
    if (!consulta) return undefined

    const controller = new AbortController()
    setEstadoConsulta('carregando')
    setErroConsulta('')

    listarCardapios(consulta, { signal: controller.signal })
      .then((resultado) => {
        setCardapios(
          [...resultado].sort((a, b) => (
            a.data.localeCompare(b.data)
            || ORDEM_REFEICOES.indexOf(a.tipo_refeicao) - ORDEM_REFEICOES.indexOf(b.tipo_refeicao)
          )),
        )
        setEstadoConsulta('concluida')
      })
      .catch((erro) => {
        if (erro.name === 'AbortError') return
        setErroConsulta(erro.message)
        setEstadoConsulta('erro')
      })

    return () => controller.abort()
  }, [consulta])

  function consultar(evento) {
    evento.preventDefault()
    setErroFormulario('')

    if (dataInicio && dataFim && dataInicio > dataFim) {
      setErroFormulario('A data inicial precisa ser anterior ou igual à data final.')
      return
    }

    const filtros = { campus_id: campusId }
    if (dataInicio) filtros.data_inicio = dataInicio
    if (dataFim) filtros.data_fim = dataFim
    if (tipoRefeicao) filtros.tipo_refeicao = tipoRefeicao
    setConsulta(filtros)
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#inicio" aria-label="Bandejão, início">
          <span className="brand-mark" aria-hidden="true">B</span>
          <span>Bandejão</span>
        </a>
        <span className="connection-status">
          <span className="status-dot" aria-hidden="true" />
          Consulta à API
        </span>
      </header>

      <section className="intro" id="inicio">
        <p className="eyebrow">RESTAURANTES UNIVERSITÁRIOS DA UNB</p>
        <h1>Cardápios dos<br /><span>RUs da UnB.</span></h1>
        <p className="intro-copy">
          Consulte os cardápios que já estão disponíveis na plataforma e escolha
          o campus, o período e a refeição.
        </p>
      </section>

      <section className="search-panel" aria-labelledby="search-title">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">CONSULTA</p>
            <h2 id="search-title">Encontre um cardápio</h2>
          </div>
          <span className="api-label">Dados da API</span>
        </div>

        {estadoCampi === 'erro' && (
          <p className="message message-error" role="alert">
            Não foi possível carregar os campi. Confira a conexão com a API. {erroCampi}
          </p>
        )}

        {estadoCampi === 'concluida' && campi.length === 0 && (
          <p className="message message-empty" role="status">
            A API ainda não tem campi cadastrados. Importe um cardápio ou carregue
            os dados de exemplo para começar.
          </p>
        )}

        <form className="filters" onSubmit={consultar}>
          <label className="filter-field campus-field">
            <span>Campus</span>
            <select
              value={campusId}
              onChange={(evento) => setCampusId(evento.target.value)}
              disabled={estadoCampi !== 'concluida' || campi.length === 0}
              required
            >
              {campi.length === 0 && <option value="">Selecione um campus</option>}
              {campi.map((campus) => (
                <option key={campus.id} value={campus.id}>{campus.nome}</option>
              ))}
            </select>
          </label>

          <label className="filter-field">
            <span>Data inicial</span>
            <input
              type="date"
              value={dataInicio}
              onChange={(evento) => setDataInicio(evento.target.value)}
              disabled={campi.length === 0}
            />
          </label>

          <label className="filter-field">
            <span>Data final</span>
            <input
              type="date"
              value={dataFim}
              onChange={(evento) => setDataFim(evento.target.value)}
              disabled={campi.length === 0}
            />
          </label>

          <label className="filter-field">
            <span>Refeição</span>
            <select
              value={tipoRefeicao}
              onChange={(evento) => setTipoRefeicao(evento.target.value)}
              disabled={campi.length === 0}
            >
              <option value="">Todas</option>
              {Object.entries(REFEICOES).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>{rotulo}</option>
              ))}
            </select>
          </label>

          <button
            className="search-button"
            type="submit"
            disabled={estadoCampi !== 'concluida' || campi.length === 0}
          >
            Consultar cardápios
          </button>
        </form>
        {erroFormulario && <p className="message message-error" role="alert">{erroFormulario}</p>}
        <p className="filter-note">
          Os filtros alimentares ainda não estão disponíveis; a semântica das marcações
          depende de validação dos dados publicados.
        </p>
      </section>

      <section className="results" aria-labelledby="results-title" aria-live="polite">
        <div className="results-heading">
          <div>
            <p className="eyebrow">CARDÁPIOS PUBLICADOS</p>
            <h2 id="results-title">Refeições encontradas</h2>
          </div>
          {estadoConsulta === 'concluida' && cardapios.length > 0 && (
            <span className="result-count">{cardapios.length} refeições</span>
          )}
        </div>

        {estadoConsulta === 'carregando' && (
          <div className="message message-loading" role="status">
            Consultando os dados do campus…
          </div>
        )}

        {estadoConsulta === 'erro' && (
          <p className="message message-error" role="alert">
            Não foi possível consultar os cardápios. {erroConsulta}
          </p>
        )}

        {estadoConsulta === 'concluida' && cardapios.length === 0 && (
          <p className="message message-empty" role="status">
            A API não retornou cardápios para esta consulta. Isso indica falta de
            registros para os filtros escolhidos, não confirma que o RU esteja fechado.
          </p>
        )}

        {estadoConsulta === 'concluida' && cardapios.length > 0 && (
          <div className="menu-grid">
            {cardapios.map((cardapio) => (
              <article className="menu-card" key={cardapio.id}>
                <div className="menu-card-heading">
                  <div>
                    <p className="menu-date">{formatarData(cardapio.data)}</p>
                    <h3>{REFEICOES[cardapio.tipo_refeicao] || cardapio.tipo_refeicao}</h3>
                  </div>
                  <span className="meal-icon" aria-hidden="true">
                    {cardapio.tipo_refeicao === 'cafe_da_manha' ? '☀' : cardapio.tipo_refeicao === 'jantar' ? '☾' : '◒'}
                  </span>
                </div>

                {cardapio.itens.length > 0 ? (
                  <ul className="menu-items">
                    {cardapio.itens.map((item) => (
                      <li className="menu-item" key={item.id}>
                        <span className="category-tag">{rotuloCategoria(item.categoria)}</span>
                        <span className="item-name">{item.nome}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-items">Nenhum item consta neste registro.</p>
                )}

                {cardapio.fonte_pdf_url && (
                  <a className="source-link" href={cardapio.fonte_pdf_url} target="_blank" rel="noreferrer">
                    Ver PDF da fonte <span aria-hidden="true">↗</span>
                  </a>
                )}
              </article>
            ))}
          </div>
        )}
      </section>

      <footer className="page-footer">
        <p>Bandejão · Cardápios dos Restaurantes Universitários da UnB</p>
        <p>O RU pode alterar o cardápio sem aviso prévio. Confira a fonte oficial.</p>
      </footer>
    </main>
  )
}

export default App
