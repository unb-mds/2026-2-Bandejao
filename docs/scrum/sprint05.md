# Sprint 05 — Planejamento persistido, estimativa e organização

**Período:** 28/10/2026 a 11/11/2026

**Objetivo da sprint:** entregar a Release 2 de ponta a ponta: o
usuário marca e desmarca a intenção de ir a uma refeição e essa
marcação fica salva na API, e a tela mostra a estimativa de intenções
por campus, data e refeição. Em paralelo, completar a organização do
repositório e deixar a documentação da disciplina organizada.

Os requisitos citados estão no [Documento de Requisitos](../Requisitos.md).

> **Natureza deste documento:** é o planejamento da sprint. As
> reuniões de acompanhamento ainda não foram realizadas/registradas;
> a seção "Reuniões de acompanhamento" registra o que **está
> planejado** para as reuniões, sem inventar decisões ou resultados.
> As entregas abaixo são apenas o que está comprovado no código,
> nos commits e nos pull requests.

## O que a sprint entrega

| Área | Entrega | Requisitos |
|---|---|---|
| Backend | Intenções de refeição: modelo, migração, rotas de marcar e desmarcar e consulta pessoal | RF06; D03; D04; D05 |
| Backend | Estimativa por campus, data e refeição, com amostra mínima de 10 intenções | RF07; D05 |
| Backend | Dados simulados para demonstração, com comando explícito de criação e remoção | D05 |
| Frontend | Planejamento semanal ligado à API, com a identidade anônima do navegador | RF06 |
| Frontend | Tela de estimativa ligada à API, com rótulos de intenções e de dados simulados | RF07; CA-RF07-03; CA-RF07-04 |
| Organização | Arquivos padrão do repositório colaborativo | — |

## Issues da sprint

| # | Issue | Área | Estado |
|---|---|---|---|
| 76 | Intenções de refeição | Back | Entregue (PR #85) |
| 77 | Estimativa de intenções por campus, data e refeição | Back | Entregue (PR #86) |
| 78 | Dados simulados para a demonstração | Back | Entregue (PR #87) |
| 79 | Planejamento semanal e tela de estimativa ligados à API | Front | Entregue (commit `fffe558`, 04/11) |
| 80 | Rótulos "intenções" e "dados simulados" | Front | Entregue (commit `fffe558`, 04/11) |
| 81 | Revisão das marcações de alérgenos com PDFs reais | Dados | Pendente |
| 82 | Conjunto de PDFs de referência | Dados | Pendente (parcial: 5 PDFs válidos com resultados esperados; falta o PDF de falha) |
| 83 | Arquivos de organização do repositório | Docs | Entregue (PR #89) |
| 84 | Documento da Sprint 05 | Docs | Entregue (PR #90) |

## Critérios de aceitação

1. **Intenções (RF06, D03, D04):** marcar só antes do início do
   serviço da refeição, no fuso de Brasília; marcar de novo a mesma
   refeição com a mesma identidade não duplica a intenção; desmarcar
   remove a contribuição da estimativa, inclusive após o início;
   refeição inexistente é recusada com mensagem explicativa; o
   cabeçalho `X-Identidade` ausente ou inválido retorna 400; a
   resposta nunca expõe o código da identidade.
2. **Estimativa (RF07, D05):** a rota devolve a contagem por campus,
   data e refeição; abaixo de 10 intenções ativas devolve
   `dados_insuficientes` sem o número; com 10 ou mais devolve a
   contagem; refeição sem nenhuma intenção também retorna
   `dados_insuficientes`; a resposta identifica se os dados são
   simulados ou reais; nada de horário de chegada, fila ou tempo de
   espera.
3. **Dados simulados (D05):** gerador só por comando explícito, com
   cada registro marcado como simulado no banco e na resposta da
   API; comando de remoção que não toca os dados reais; nenhum dado
   simulado é gerado automaticamente em produção.
4. **Planejamento na tela (RF06):** marcar e desmarcar refeições na
   semana com a identidade do navegador; a marcação persiste ao
   recarregar a página; refeição já iniciada bloqueia a marcação e
   explica o motivo; erros da API aparecem com mensagem clara.
5. **Estimativa na tela (RF07, CA-RF07-03, CA-RF07-04):** a contagem
   exibida vem da API; abaixo de 10 intenções a tela mostra
   "dados insuficientes"; a tela diz que o número é uma estimativa
   de intenções, e não a fila real; todo dado simulado aparece como
   simulado, na tela de estimativa e no planejamento.
6. **Organização (issue 83):** licença, guia de contribuição com
   branch por tarefa e PR revisado por outra pessoa, código de
   conduta, template de PR e templates de issue; README apontando
   para eles.

## Plano de acompanhamento

O grupo acompanhará a sprint nas reuniões semanais previstas no
planejamento da disciplina. As decisões e resultados dessas
reuniões serão registrados aqui e na ata correspondente quando
ocorrerem, com data e participantes reais indicados pelo grupo.

A agenda prevista para o ciclo de acompanhamento é:

1. **Abertura da sprint:** confirmar o escopo (issues 76 a 84) e a
   ordem de entrega: backend das intenções e da estimativa primeiro
   (76, 77, 78), depois a integração do frontend (79, 80), em
   paralelo os dados (81, 82) e a organização (83, 84).
2. **Telefonemas de verificação:** conferir se as entregas de
   backend (76–78) estão na `main` e se há testes e migração, antes
   de começar o frontend (79, 80).
3. **Fechamento:** verificar quais critérios de aceitação foram
   atingidos, quais issues restam pendentes (81, 82) e quais
   pendências operacionais continuam fora do repositório (token da
   sincronização e ativação no Render).

## Limites conhecidos

- A semana exibida pelo frontend continua de domingo a sábado, uma
  escolha de apresentação da integração, e não a resolução da D01;
  os horários de início das refeições seguem duplicados no frontend
  (tabela local) e no backend (`HORARIOS_INICIO_REFEICAO`).
- A tela de lotação continua com exemplos e relatos desta sessão,
  sem consulta a dados reais; os números fictícios de lotação
  permanecem rotulados como exemplos.
- Na execução consultada em 10/11/2026, `BACKEND_URL` estava
  configurada, mas `IMPORTACAO_TOKEN` não estava disponível ao workflow.
  A validação parou antes de extrair e importar os cardápios. A próxima
  execução depende de o mesmo token estar configurado na API e no GitHub.
- O Blueprint de hospedagem HTTPS foi integrado no PR 71. A
  disponibilidade atual do site e da API não foi verificada nesta revisão;
  o registro em `docs/verificacao-publicacao.md` contém a verificação de
  27/10/2026.
- README, `contexto.md`, `docs/index.md`, `docs/Arquitetura.md` e
  `docs/Requisitos.md` foram alinhados ao estado implementado de RF06/RF07.
