import assert from 'node:assert/strict'
import { test } from 'node:test'
import { adaptarCardapio, alergenosDoItem, dataDaSemana, dietaCompativelComFiltros, formatarInstanteImportacao, inicioSemana, montarSemana } from '../src/cardapios.ts'
import type { CardapioApi, ItemApi } from '../src/api.ts'
import type { FiltrosAlimentares } from '../src/types.ts'

const item: ItemApi = {
  id: 1, nome: 'Prato publicado', categoria: 'prato_principal', tipo_dieta: 'padrao',
  contem_leite: false, contem_ovo: false, contem_gluten: false, contem_cogumelo: false,
  contem_amendoim: false, contem_mel: false, contem_soja: false, contem_pimenta: false,
  contem_oleaginosas: false, contem_carne_suina: false, contem_frutos_do_mar: false,
}
const cardapio: CardapioApi = {
  id: 7, campus_id: 2, data: '2026-09-30', tipo_refeicao: 'almoco',
  fonte_pdf_url: 'https://ru.unb.br/cardapio.pdf', itens: [item],
}

test('filtro ovolacto inclui a classe vegetariana estrita e mantém as demais classes fora', () => {
  const filtros: FiltrosAlimentares = { vegetariano: true, vegetarianoEstrito: false, alergenos: [] }
  assert.equal(dietaCompativelComFiltros('comum', filtros), false)
  assert.equal(dietaCompativelComFiltros('padrao', filtros), false)
  assert.equal(dietaCompativelComFiltros('ovolactovegetariano', filtros), true)
  assert.equal(dietaCompativelComFiltros('vegetariano_estrito', filtros), true)
})

test('filtro vegetariano estrito permanece exato e ausência de dieta selecionada inclui tudo', () => {
  const estrito: FiltrosAlimentares = { vegetariano: false, vegetarianoEstrito: true, alergenos: [] }
  const semDieta: FiltrosAlimentares = { vegetariano: false, vegetarianoEstrito: false, alergenos: [] }
  assert.equal(dietaCompativelComFiltros('ovolactovegetariano', estrito), false)
  assert.equal(dietaCompativelComFiltros('vegetariano_estrito', estrito), true)
  assert.equal(dietaCompativelComFiltros('comum', semDieta), true)
})

test('não mistura duas semanas que tenham o mesmo dia da semana', () => {
  const semana = montarSemana([cardapio, { ...cardapio, id: 8, data: '2026-10-07' }], '2026-09-27')
  assert.equal(semana[3].almoco.id, 7)
  assert.equal(semana[3].almoco.data, '2026-09-30')
  assert.equal(semana.flatMap(dia => Object.values(dia)).some(refeicao => refeicao.id === 8), false)
})

test('mapeia café da manhã sem criar almoço ou jantar fictícios', () => {
  const semana = montarSemana([{ ...cardapio, tipo_refeicao: 'cafe_da_manha' }], '2026-09-27')
  assert.equal(semana[3].cafe.id, 7)
  assert.deepEqual(semana[3].almoco.itensApi, [])
  assert.equal(semana[3].almoco.id, undefined)
  assert.deepEqual(montarSemana([], '2026-09-27')[0].jantar.itensApi, [])
})

test('preserva todos os itens, categorias, dietas e origem sem deduzir ingredientes', () => {
  const itens = [
    item,
    { ...item, id: 2, categoria: 'sopa', tipo_dieta: 'vegetariano_estrito', nome: 'Sopa' },
    { ...item, id: 3, categoria: 'torrada', nome: 'Torrada de trigo' },
    { ...item, id: 4, categoria: 'opcao_extra', nome: 'Outro item' },
  ]
  const resultado = adaptarCardapio({ ...cardapio, itens })
  assert.deepEqual(resultado.itensApi, itens)
  assert.equal(resultado.fontePdfUrl, cardapio.fonte_pdf_url)
  assert.deepEqual(alergenosDoItem(itens[2]), [])
})

test('traduz somente marcadores positivos da API para os filtros da interface', () => {
  assert.deepEqual(alergenosDoItem({ ...item, contem_gluten: true, contem_oleaginosas: true, contem_carne_suina: true }), ['trigo', 'oleaginosa', 'suino'])
  assert.deepEqual(alergenosDoItem(item), [])
})

test('intervalo semanal atravessa mês e ano sem deslocar a data local', () => {
  assert.equal(inicioSemana(new Date('2027-01-01T12:00:00')), '2026-12-27')
  assert.equal(dataDaSemana('2026-12-27', 6), '2027-01-02')
})

test('apresenta a última importação no fuso de Brasília', () => {
  assert.equal(
    formatarInstanteImportacao('2026-10-24T18:45:00Z'),
    '24/10/2026 às 15:45',
  )
})
