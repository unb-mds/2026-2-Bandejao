# Sprint 06 — Verificação e fechamento da Release 2

Ciclo posterior à Sprint 05, encerrada em 11/11. Congelamento de código em
19/11/2026 (só correções, testes e documentação); publicação final em
25/11/2026.

## Objetivo

Verificar os fluxos integrados, corrigir regressões encontradas e publicar a
Release 2.

## O que foi entregue

| Issue | Entrega |
|---|---|
| [#94](https://github.com/unb-mds/2026-2-Bandejao/issues/94) | Backend testado em PostgreSQL 16 no CI, além do SQLite local |
| [#95](https://github.com/unb-mds/2026-2-Bandejao/issues/95) | Tratamento de concorrência: mesma identidade avaliando ou marcando intenção ao mesmo tempo |
| [#97](https://github.com/unb-mds/2026-2-Bandejao/issues/97) | Quatro cenários de falha da sincronização, com dados preservados ([evidência](../evidencias/falhas-sincronizacao-2026-11-17.md)) |
| [#99](https://github.com/unb-mds/2026-2-Bandejao/issues/99) | Privacidade da identidade confirmada em sucesso, erro e leitura interna |
| [#100](https://github.com/unb-mds/2026-2-Bandejao/issues/100) | Matriz de rastreabilidade de requisitos, com evidência por RF/RNF ([Requisitos](../Requisitos.md)) |
| [#101](https://github.com/unb-mds/2026-2-Bandejao/issues/101) | Bugs encontrados na verificação corrigidos ([PR #115](https://github.com/unb-mds/2026-2-Bandejao/pull/115)) |
| [#102](https://github.com/unb-mds/2026-2-Bandejao/issues/102) | Este documento, changelog e preparação da Release 2 |
| [#117](https://github.com/unb-mds/2026-2-Bandejao/issues/117) | Publicação do commit final da Release 2 na hospedagem |

## Resultado técnico

206 testes de backend aprovados (100% de cobertura), 59 da extração e 48 do
frontend. TypeScript, Oxlint, Vite, Ruff, Bandit e CodeQL aprovados no CI,
incluindo execução em PostgreSQL 16. Checks do [PR #115](https://github.com/unb-mds/2026-2-Bandejao/pull/115):
[backend/frontend](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/44628607610),
[SAST](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/44628607327) e
[documentação](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/44628607331).

## Publicação

A aplicação está publicada em HTTPS: <https://bandejao-unb-g12.onrender.com>
e <https://bandejao-unb-g12-api.onrender.com>. Em 25/11/2026 a hospedagem foi
atualizada para o commit final da Release 2, confirmado em `/version`. Os
cinco campi têm cardápio real, sincronizado automaticamente a partir do site
oficial do RU; a estimativa de intenções por refeição está ativa, com dados
simulados identificados como tal quando usados para demonstração.

## Limitações conhecidas

Dois itens de verificação não têm evidência registrada: a medição de carga
com k6 (RNF01) e a execução completa do roteiro manual em um aparelho físico
(#98). O restante dos requisitos descritos na visão do produto foi entregue,
testado e publicado.

## Reuniões

Sem ata de reuniões deste ciclo disponível; datas e participantes não foram
registrados.
