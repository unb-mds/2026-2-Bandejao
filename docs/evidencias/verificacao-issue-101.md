# Correções da verificação — issue #101

Data: 19/11/2026. Base: `17397beb184a708fdf5ab9991a6e51801ecf514b`.
Implementação verificada: `304cd88`; regressões em `4e29fcd`, `8a30550` e `b3bb83a`.
Nenhum recurso novo foi acrescentado após o congelamento de 19/11.

## Rastreabilidade da verificação

As “issues 1 a 7” do planejamento correspondem a #94–#99, incluindo #96
(carga) e #98 (roteiro manual), além do registro de requisitos em #100.
Foram consultados os testes e registros integrados dessas entregas. O teste
manual publicado continua sem execução completa documentada; uma tentativa
bloqueada não foi convertida em aprovação.

| Bug | Antes | Correção | Regressão |
|---|---|---|---|
| [#112](https://github.com/unb-mds/2026-2-Bandejao/issues/112) | Semana de domingo a sábado | Segunda a domingo; índices e rótulos consistentes | `frontend/tests/cardapios.test.ts`: domingo, virada do ano e montagem dos sete dias |
| [#113](https://github.com/unb-mds/2026-2-Bandejao/issues/113) | Datas e prazo de intenção no fuso do dispositivo | Data corrente, início da semana, refeição atual, cabeçalhos e prazo em Brasília | `cardapios.test.ts` e `utils.test.ts`: meia-noite de Brasília, limites do serviço e instantes UTC |
| [#114](https://github.com/unb-mds/2026-2-Bandejao/issues/114) | Estimativa antiga após falha ou mudança de intenção | Resultado vinculado ao campus/semana/revisão; nova consulta após escrita; erro visível | `frontend/tests/estimativas.test.ts`: atualização, preferência real/simulada, falhas e recorte consultado |

## Resultados locais

Ambiente: Windows, Python 3.12.14, Node do runtime local; dependências do
frontend instaladas com `npm ci`, usando `package-lock.json`.

| Verificação | Resultado |
|---|---|
| Backend em SQLite | 206 aprovados, 3 exclusivos de PostgreSQL ignorados; cobertura 100% |
| Extração e sincronização | 59 aprovados; cobertura 100% |
| Frontend | 45 aprovados em UTC e em `Pacific/Auckland` |
| TypeScript, Oxlint e build Vite | Aprovados |
| Verificador da publicação e gate de segurança | 30 aprovados; 3 casos ignorados conforme plataforma |
| Ruff do backend e da extração | Aprovado |

Para reproduzir, executar os comandos do README. No Windows, quando a pasta
temporária de outra sessão estiver inacessível, passar ao pytest um
`--basetemp` novo dentro de `.venv/`. O CI mantém a execução real em
PostgreSQL 16 e verifica as datas em UTC e `Pacific/Auckland`.

## Interface com API simulada

Chrome sem interface gráfica, contexto novo, viewport 390 × 844 e fuso
`Pacific/Auckland`. Relógio em `2026-11-19T13:00:00Z`, equivalente a 10h em
Brasília. A API foi interceptada apenas nesse navegador, sem banco real.

- Semana inicial `16/11` a `22/11`, segunda a domingo.
- Marcar intenção antes do almoço: contagem passou de 10 para 11.
- Desmarcar: contagem voltou de 11 para 10.
- Trocar campus com a API de estimativas respondendo 503: mensagem de erro
  exibida e contagem anterior removida.
- Nenhum erro JavaScript observado nesses passos.

Esta execução prova os fluxos corrigidos com respostas controladas. Não
substitui o roteiro completo em celular físico, persistência real ou teste de
carga. A medição k6 de RNF01 continua sem relatório disponível.

## Ajustes após revisão

O README agora afirma explicitamente que o frontend segue D01. A revisão
também identificou que uma falha exclusiva da consulta simulada descartava
uma estimativa real válida. Dois testes novos reproduziram a falha antes da
correção. A simulação passou a ser opcional: a resposta real atual é mantida,
inclusive `dados_insuficientes` sem contagem. Falhas da consulta real e
cancelamentos continuam sendo propagados.

Após a correção: 48 testes frontend aprovados; TypeScript, Oxlint e build
Vite aprovados. O resultado de 45 testes acima descreve a execução anterior.
