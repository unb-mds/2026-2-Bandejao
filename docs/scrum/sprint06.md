# Sprint 06 — Verificação e fechamento da Release 2

Registro atualizado em **19/11/2026**. Ciclo posterior à Sprint 05, encerrada
em 11/11. Datas de reuniões, participantes e aceite final não foram fornecidos;
não são presumidos neste documento.

## Objetivo

Verificar os fluxos integrados, corrigir regressões e preparar a Release 2 com
resultados e limitações rastreáveis. Congelamento do código em 19/11/2026:
somente correções, testes e documentação, sem novos recursos.

## Entregas e evidências

| Issue | Entrega | Situação verificada |
|---|---|---|
| [#94](https://github.com/unb-mds/2026-2-Bandejao/issues/94) | Backend em PostgreSQL 16 no CI | Serviço e execução configurados; teste de migrações versionado |
| [#95](https://github.com/unb-mds/2026-2-Bandejao/issues/95) | Concorrência da mesma identidade/refeição | Regressões e tratamento de conflito de avaliação integrados |
| [#96](https://github.com/unb-mds/2026-2-Bandejao/issues/96) | Carga sintética | Scripts em `testes/carga/`; sem relatório de medição disponível |
| [#97](https://github.com/unb-mds/2026-2-Bandejao/issues/97) | Falhas de sincronização | [Quatro cenários](../evidencias/falhas-sincronizacao-2026-11-17.md) preservam dados |
| [#98](https://github.com/unb-mds/2026-2-Bandejao/issues/98) | Roteiro manual | [Tentativa registrada](../evidencias/roteiro-ponta-a-ponta-2026-11-17.md); execução completa em celular físico ainda sem evidência |
| [#99](https://github.com/unb-mds/2026-2-Bandejao/issues/99) | Privacidade | Testes de sucesso, erro e leitura interna integrados |
| [#100](https://github.com/unb-mds/2026-2-Bandejao/issues/100) | Rastreabilidade | [Matriz de requisitos](../Requisitos.md) com evidências e pendências |
| [#101](https://github.com/unb-mds/2026-2-Bandejao/issues/101) | Correções | [PR #115](https://github.com/unb-mds/2026-2-Bandejao/pull/115), bugs #112–#114 e [regressões](../evidencias/verificacao-issue-101.md) |
| [#102](https://github.com/unb-mds/2026-2-Bandejao/issues/102) | Release e sprint | Este documento, notas da versão, changelog e preparação de tag/GitHub Release |

## Resultado técnico

Na base `17397be` com as correções da #101: 206 testes backend aprovados em
SQLite, 3 exclusivos de PostgreSQL ignorados localmente, 59 da extração e 45
do frontend. Backend e extração com cobertura de 100%. TypeScript, Oxlint,
Vite e Ruff aprovados. O CI executa PostgreSQL 16, SAST e regressões de datas
em UTC e `Pacific/Auckland`.

A verificação da interface com API simulada cobriu segunda–domingo, o prazo
em Brasília, marcar/desmarcar e erro da estimativa em viewport de celular.
Não representa execução em aparelho físico nem persistência em produção.

## Publicação e fechamento

Em 19/11 a interface respondeu por HTTPS. A primeira consulta de saúde falhou
por conexão/TLS; a repetição respondeu 200 com `status: ok`. `/version`
respondeu `b5b345d7690c8b543dac44f7929a315925da0911`, anterior à base
`17397be`. Consultas públicas retornaram cinco campi, 84 refeições e 751
itens. O [registro bruto](../evidencias/dados/publicacao-release2-2026-11-19.json)
preserva os resultados, inclusive a falha inicial.

O código preparado e a versão em produção são estados diferentes. As
[notas da Release 2](../release-2.md) descrevem o conteúdo e os limites. A
publicação final requer revisão de outro integrante, integração dos PRs e
tag apontando para o commit efetivamente publicado. Não há aceite global
dos requisitos, comprovação de RNF01 ou comprovação de disponibilidade na
janela inteira de RNF04.

## Reuniões e retrospectiva

Sem ata de reuniões deste ciclo disponível. O grupo deve registrar datas,
participantes, decisões e aceite reais. Os principais riscos observados são
a diferença entre commits da fonte e da hospedagem, a falta de relatório k6
e a ausência de evidência completa do roteiro manual. Esses limites ficam
visíveis na release em vez de serem tratados como testes aprovados.
