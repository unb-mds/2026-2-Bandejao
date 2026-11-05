# Sprint 05 — Planejamento persistido, estimativa e organização

**Período:** 28/10/2026 a 11/11/2026

**Objetivo da sprint:** entregar a Release 2 de ponta a ponta: o
usuário marca e desmarca a intenção de ir a uma refeição e essa
marcação fica salva na API, e a tela mostra a estimativa de intenções
por campus, data e refeição. Em paralelo, completar a organização do
repositório e deixar a documentação da disciplina organizada.

Os requisitos citados estão no [Documento de Requisitos](../Requisitos.md).

> **Registro:** as atas e os resultados das reuniões de acompanhamento
> desta sprint **não foram registrados pelo grupo**. As seções de
> reunião marcadas como "a registrar" deverão ser preenchidas quando
> as reuniões acontecerem. As entregas abaixo são apenas o que está
> comprovado no código, nos commits e nos pull requests.

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
| 82 | Conjunto de PDFs de referência | Dados | Pendente (parcial: 5 PDFs e regressão offline já existem) |
| 83 | Arquivos de organização do repositório | Docs | Entregue (PR #89) |
| 84 | Documento da Sprint 05 | Docs | Em andamento |

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

## Reuniões de acompanhamento

- Reunião de abertura da sprint: **a registrar pelo grupo**.
- Revisões semanais: **a registrar pelo grupo**.
- Retrospectiva e encerramento: **a registrar pelo grupo**.

Os resultados e decisões dessas reuniões serão acrescentados aqui
e na ata correspondente quando forem registrados pelo grupo.

## Limites conhecidos

- A semana exibida pelo frontend continua de domingo a sábado, uma
  escolha de apresentação da integração, e não a resolução da D01;
  os horários de início das refeições seguem duplicados no frontend
  (tabela local) e no backend (`HORARIOS_INICIO_REFEICAO`).
- A tela de lotação continua com exemplos e relatos desta sessão,
  sem consulta a dados reais; os números fictícios de lotação
  permanecem rotulados como exemplos.
- A sincronização automática a cada seis horas depende de a
  variável `BACKEND_URL` e do secret `IMPORTACAO_TOKEN` estarem
  configurados no repositório, e a publicação em HTTPS depende da
  ativação do ambiente no Render (issues 54 e 55).
- A documentação geral (README, `contexto.md`, `docs/index.md`,
  `docs/Arquitetura.md`) ainda descreve RF06/RF07 como pendentes e
  será atualizada na próxima revisão de consistência.
