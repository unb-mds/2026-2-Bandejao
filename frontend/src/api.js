const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'

export async function requisitarJson(caminho, parametros = {}, opcoes = {}) {
  const { signal, fetchImpl = globalThis.fetch, baseUrl = API_BASE_URL } = opcoes
  const base = baseUrl.replace(/\/+$/, '')
  const url = new URL(caminho.replace(/^\/+/, ''), `${base}/`)

  for (const [chave, valor] of Object.entries(parametros)) {
    if (valor !== '' && valor !== null && valor !== undefined) {
      url.searchParams.set(chave, String(valor))
    }
  }

  const resposta = await fetchImpl(url, {
    signal,
    headers: { Accept: 'application/json' },
  })

  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null)
    const detalhe = typeof corpo?.detail === 'string' ? corpo.detail : null
    throw new Error(detalhe || `A API respondeu com HTTP ${resposta.status}.`)
  }

  return resposta.json()
}

export function listarCampi(opcoes) {
  return requisitarJson('campi/', {}, opcoes)
}

export function listarCardapios(filtros, opcoes) {
  return requisitarJson('cardapios/', filtros, opcoes)
}
