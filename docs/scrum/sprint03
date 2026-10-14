# Sprint 03 — Decisões e Base de Entrega

**Período:** 14/10/2026 a 21/10/2026

**Objetivo da sprint:** transformar as decisões D01 a D08 do [Documento de Requisitos](../Requisitos.md) (v1.2, seção 7) em base de código, configuração e documentação, para servir de base à implementação dos requisitos.

Esta sprint trata **apenas** das decisões. Os requisitos funcionais que dependem delas não fazem parte dela.

## Decisões e o que esta sprint entrega

| Decisão | Resumo | Entrega na Sprint 03 |
|---|---|---|
| D01 | Semana de segunda a domingo, fuso `America/Sao_Paulo`. | Utilitário de tempo no backend. |
| D02 | Filtro de dieta inclusivo e aviso de "sem marcação". | Filtro ajustado no backend e aviso nas telas. |
| D03 | Horários fixos por refeição, em tabela de configuração; sem "suspenso". | Tabela de horários e função de elegibilidade, com testes de limite. |
| D04 | Identidade anônima por navegador, sem login. | Identidade no backend e no frontend, mais o ajuste de CORS. |
| D05 | Estimativa de intenções, amostra mínima de 10, dados simulados identificados. | Apenas a constante de configuração. |
| D06 | Reclamações com 4 categorias, sem foto e sem lista pública. | Nada nesta sprint. |
| D07 | Verificação e metas (k6, sincronização, PDFs, SAST, checagem). | Apenas o SAST (item d). |
| D08 | Token na importação. | Token na importação e na sincronização. |

## Issues da sprint

| # | Issue | Decisão | Área |
|---|---|---|---|
| 1 | Incorporar o Requisitos v1.2 ao repositório e registrar as decisões D01 a D08 | D01 a D08 | Docs |
| 2 | Utilitário de tempo: fuso `America/Sao_Paulo` e início/fim da semana (segunda a domingo) | D01 | Back |
| 3 | Filtro de dieta inclusivo na API e aviso "sem marcação = não marcado na fonte" nas telas | D02 | Back + Front |
| 4 | Configuração das decisões: tabela de horários por refeição, função que informa se a avaliação está aberta e constante de amostra mínima (10) | D03, D05 | Back |
| 5 | Identidade anônima por navegador (backend, migração, CORS e frontend) | D04 | Back + Front |
| 6 | Token na importação e na sincronização; remover ou proteger a rota `/checkin` | D08 | Back + Dados |
| 7 | SAST no CI: bandit (Python) e CodeQL (JS/TS), bloqueando achados altos e críticos | D07d | DevOps |
| 8 | Documento da Sprint 03, entrada no `mkdocs.yml` e registro no `changelog.md` | — | Docs |

## Critérios de aceitação

1. **Requisitos v1.2:** `docs/Requisitos.md` atualizado na `main` e o site compilando com `mkdocs build --strict`.
2. **Tempo (D01):** dada qualquer data, a função devolve a segunda-feira e o domingo da semana; testes cobrem semana que cruza mês e ano; o fuso é explícito, sem depender do relógio do servidor.
3. **Dieta (D02):** `ovolactovegetariano` retorna também itens `vegetariano_estrito`; as demais dietas continuam exatas; testes cobrem os quatro casos; as telas mostram o aviso.
4. **Configuração (D03, D05):** a função de elegibilidade tem testes nos limites: antes do início (fechada), no início (aberta), um instante antes de 00h do dia seguinte (aberta) e às 00h (fechada); refeição sem horário configurado permanece fechada; a amostra mínima fica em um único lugar da configuração.
5. **Identidade (D04):** cabeçalho `X-Identidade` ausente ou inválido retorna 400; a primeira avaliação retorna 201 e a seguinte, da mesma identidade, atualiza (200) sem criar outra linha; a resposta nunca contém o código; o navegador consegue enviar POST (CORS).
6. **Token (D08):** importação sem token ou com token inválido retorna 401 ou 403 e não grava nada; a sincronização funciona com o token vindo de variável de ambiente; o repositório não contém o token real; `/checkin` removido ou protegido.
7. **SAST (D07d):** o CI roda bandit e CodeQL em cada PR; falha ou achado alto/crítico impede a integração; o relatório registra ferramenta, versão, linguagens cobertas e a equivalência de severidades (o bandit não tem "crítico").
8. **Documentação:** o documento da sprint e a entrada no `mkdocs.yml` publicados; o `changelog.md` atualizado.

## Fora do escopo desta sprint

Decisões cuja implementação não faz parte desta sprint:

- D06: reclamações (RF08).
- D05: estimativa de intenções (RF06 e RF07) e os dados simulados.
- D03: aplicação da janela de horário nas rotas de avaliação.
- D07: teste de carga com k6, sincronização a cada 6 horas, PDFs de referência e checagem a cada 5 minutos.
