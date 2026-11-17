// Teste de carga do RNF01 nas consultas de cardápio (issue #96).
//
// 50 usuários por 5 minutos, depois de 1 minuto de aquecimento, com 1 segundo
// de pausa entre as consultas. Cada usuário alterna entre os três tipos de
// consulta: semana sem filtro, por dieta e excluindo um alérgeno.
//
// Uso: k6 run cardapio.js   (antes, rode gerar_massa.py para criar massa.json)

import http from 'k6/http'
import { check, sleep } from 'k6'

const massa = JSON.parse(open('./massa.json'))
const API_URL = __ENV.API_URL || massa.api_url

// Valores do RNF01. Só mude para testar o script rapidamente (não vale como medição).
const VUS = Number(__ENV.VUS || 50)
const AQUECIMENTO = __ENV.AQUECIMENTO || '1m'
const MEDICAO = __ENV.MEDICAO || '5m'

export const options = {
  scenarios: {
    aquecimento: { executor: 'constant-vus', vus: VUS, duration: AQUECIMENTO, tags: { fase: 'aquecimento' } },
    medicao: { executor: 'constant-vus', vus: VUS, duration: MEDICAO, startTime: AQUECIMENTO, tags: { fase: 'medicao' } },
  },
  // Só a fase de medição conta: p95 de até 2 s em cada tipo e menos de 1% de falhas.
  thresholds: {
    'http_req_duration{fase:medicao,tipo:semanal}': ['p(95)<=2000'],
    'http_req_duration{fase:medicao,tipo:dieta}': ['p(95)<=2000'],
    'http_req_duration{fase:medicao,tipo:exclusao}': ['p(95)<=2000'],
    'checks{fase:medicao}': ['rate>0.99'],
    // Estas linhas só servem para o resumo mostrar quantas consultas houve de cada tipo.
    'http_reqs{fase:medicao,tipo:semanal}': ['count>=0'],
    'http_reqs{fase:medicao,tipo:dieta}': ['count>=0'],
    'http_reqs{fase:medicao,tipo:exclusao}': ['count>=0'],
  },
}

function sortear(lista) {
  return lista[Math.floor(Math.random() * lista.length)]
}

function somarDias(data, dias) {
  const d = new Date(data + 'T00:00:00Z')
  d.setUTCDate(d.getUTCDate() + dias)
  return d.toISOString().slice(0, 10)
}

export default function () {
  const tipo = ['semanal', 'dieta', 'exclusao'][__ITER % 3]
  const campus = sortear(massa.campi)
  const inicio = sortear(massa.semanas)
  const dieta = sortear(massa.dietas)
  const alergeno = sortear(massa.exclusoes)

  let url = `${API_URL}/cardapios/?campus_id=${campus.id}&data_inicio=${inicio}&data_fim=${somarDias(inicio, 6)}`
  if (tipo === 'dieta') url += `&tipo_dieta=${dieta}`
  if (tipo === 'exclusao') url += `&excluir_alergenos=${alergeno}`

  const resposta = http.get(url, { tags: { tipo }, timeout: '10s' })

  // Uma resposta só conta como sucesso se vier 200 e com o conteúdo certo para a consulta.
  check(resposta, {
    'resposta válida': (r) => {
      if (r.status !== 200) return false
      const cardapios = r.json()
      if (!Array.isArray(cardapios) || cardapios.length === 0) return false
      for (const cardapio of cardapios) {
        if (cardapio.campus_id !== campus.id) return false
        for (const item of cardapio.itens) {
          if (tipo === 'dieta' && dieta === 'vegetariano_estrito' && item.tipo_dieta !== 'vegetariano_estrito') return false
          if (tipo === 'dieta' && dieta === 'ovolactovegetariano' && item.tipo_dieta === 'padrao') return false
          if (tipo === 'exclusao' && item['contem_' + alergeno]) return false
        }
      }
      return true
    },
  }, { tipo })

  sleep(1)
}
