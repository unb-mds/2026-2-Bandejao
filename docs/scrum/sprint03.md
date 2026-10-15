# Sprint 03 — Decisões e Base de Entrega

**Período:** 14/10/2026 a 21/10/2026

**Objetivo:** preparar as decisões e a infraestrutura necessárias às próximas sprints: SAST no CI, sincronização a cada seis horas e proteção da importação, além das bases de tempo, dieta e identidade previstas no planejamento.

## Fonte das decisões e escopo desta entrega

A [ata de 12/10](atas-reunioes/ata-sprint03.md) e o [Documento de Requisitos v1.2](../Requisitos.md) registram as decisões D01–D08. O texto de votação é a proposta anterior à ata. Não houve nova votação nesta entrega.

| Ponto | Proposta para votação | Decisão registrada na ata |
|---|---|---|
| D02 — Dieta | Correspondência exata | Ovolactovegetariano também inclui vegetariano estrito. |
| D03 — Horários | Cadastro por campus/refeição e campo de serviço suspenso | Tabela de horários; suspensão fora do escopo. Fonte e valores dos horários ainda precisam ser preenchidos. |
| D04 — Identidade | Login com e-mail e senha | Sem login; código anônimo por navegador. |
| D05 — Movimento | Mínimo de 20 intenções | Mínimo de 10; estimativa por refeição, sem horário de chegada. |

Esta branch, `feature/sprint03-base-entrega`, concentra **SAST, sincronização e documentação**, conforme o escopo solicitado. Inclui D08 porque a rotina de sincronização precisa autenticar a importação. O agendamento de seis horas, anteriormente listado para uma sprint posterior, entra nesta entrega. Tempo, dieta, identidade e funcionalidades das próximas sprints continuam pendentes.

A infraestrutura pode ser desenvolvida sem concluir os RFs futuros. Sua operação depende de API e banco disponíveis, migrações aplicadas, token configurado e uma máquina mantendo o Docker em execução. O bloqueio de merge depende também da configuração dos checks obrigatórios no GitHub.

## Decisões e entregas

| Decisão | Entrega planejada | Estado nesta branch |
|---|---|---|
| D01 | Utilitário de semana segunda–domingo e fuso de Brasília | Fora do recorte desta branch; permanece no planejamento da sprint. |
| D02 | Filtro inclusivo na API e aviso sobre marcações da fonte | Fora do recorte desta branch. |
| D03 | Configuração de horários e função de elegibilidade | Fora do recorte desta branch; horários/fonte ainda pendentes. |
| D04 | Identidade anônima no backend/frontend e CORS para envio | Fora do recorte desta branch. |
| D05 | Constante de amostra mínima de 10 | Fora do recorte desta branch; estimativa e planejamento ficam para depois. |
| D06 | Reclamações privadas, quatro categorias, sem foto/nome | Implementação nas próximas sprints. |
| D07b | Sincronização a cada seis horas | Serviço opcional no Docker Compose; iniciar após configuração e migrações. |
| D07d | Bandit para Python e CodeQL para JS/TS | Workflow e verificações de severidade; execução no GitHub e checks obrigatórios precisam ser confirmados após publicação da branch. |
| D08 | Token na importação e na sincronização | Importação autenticada e rotas HTTP de check-in legado retiradas; modelos e dados legados preservados. |

## Itens de trabalho

Os números abaixo são identificadores desta lista, não números de issues do GitHub. Vincular os links reais quando as issues forem criadas; nenhum responsável ou número externo foi presumido.

| Item | Trabalho | Decisão | Área |
|---|---|---|---|
| S03-01 | Incorporar os requisitos v1.2 e registrar decisões | D01–D08 | Documentação |
| S03-02 | Utilitário de tempo e testes de mudança de mês/ano | D01 | Backend |
| S03-03 | Filtro inclusivo e aviso sobre informação alimentar | D02 | Backend + frontend |
| S03-04 | Horários, elegibilidade e constante de amostra mínima | D03, D05 | Backend |
| S03-05 | Identidade anônima, migração e CORS | D04 | Backend + frontend |
| S03-06 | Token na importação e retirada de rotas legadas de check-in | D08 | Backend + dados |
| S03-07 | SAST, relatórios e bloqueio de achados altos/críticos | D07d | CI |
| S03-08 | Serviço de sincronização a cada seis horas | D07b | Dados + infraestrutura |
| S03-09 | Roteiro de operação, evidências e atualização da sprint | — | Documentação |

## Critérios de aceitação deste recorte

1. **Importação:** ausência de token ou token inválido recebe 401/403, sem gravação; configuração sem segredo recusa a operação. Token correto permite importar/reimportar, preservando as garantias do contrato. O segredo vem do ambiente, não do código, argumentos da linha de comando ou logs.
2. **Rotas legadas:** `/campi/{id}/checkins/` deixa de aceitar chamadas HTTP; as tabelas existentes não são apagadas. As consultas públicas de campus/cardápio continuam funcionando.
3. **Agendamento:** ao iniciar o serviço configurado, ocorre uma execução imediata; os próximos ciclos usam intervalo de 21.600 segundos. Falha da fonte ou de um campus é registrada sem divulgar credenciais e não encerra o agendamento. Não iniciar uma segunda execução enquanto a anterior está ativa.
4. **SAST:** cada PR executa Bandit em Python e CodeQL em JavaScript/TypeScript. Achados altos/críticos, falha do scanner ou relatório inválido fazem o check falhar; resultados baixos/médios permanecem no relatório sem bloquear por severidade. Bandit possui LOW/MEDIUM/HIGH, sem categoria CRITICAL; HIGH é bloqueante. CodeQL usa a severidade de segurança do relatório.
5. **Evidências:** guardar relatórios dos scanners com versão/commit e resultados dos testes. Testes com relógio e rede simulados validam o agendamento sem aguardar seis horas nem alterar dados reais do RU.
6. **GitHub:** tornar os checks SAST obrigatórios na proteção/ruleset da `main`. Um workflow com falha, sozinho, não garante bloqueio de merge. A configuração remota é uma etapa de ativação a verificar pelo administrador.
7. **Documentação:** roteiro de início/parada e configuração de segredo disponível; links locais e build estrito do MkDocs válidos. Disponibilizar código nesta branch não comprova serviço ativo ou publicação no site.

## Ativação e evidências

O [roteiro de desenvolvimento](../desenvolvimento.md) descreve como configurar o token, aplicar migrações e iniciar/parar a sincronização. O [contrato de importação](../handoff_banco_e_importacao.md) documenta a autenticação. A política e os comandos de SAST ficam em `scripts/security/POLICY.md` no repositório.

A validação desta branch deve distinguir:

- **Código/testes locais:** autenticação, isolamento por campus, repetição do agendamento, tratamento dos relatórios de segurança e configuração do Compose.
- **Execução no GitHub:** CodeQL, upload de relatórios e configuração dos checks obrigatórios, após publicar a branch.
- **Operação:** execução real com banco migrado e fonte disponível, em máquina continuamente ligada. Se o host estiver suspenso ou desligado, a rotina não executa; ao voltar, começa um novo ciclo.

### Evidências locais desta branch

- Backend: 22 testes aprovados, 100% de cobertura e Ruff aprovado.
- Extração/sincronização: 41 testes aprovados, 100% de cobertura e Ruff aprovado.
- Gate SAST: 10 testes aprovados; Bandit analisou os arquivos Python rastreados sem achados altos.
- Configuração/documentação: `docker compose config --quiet`, validação do YAML, `git diff --check` e `mkdocs build --strict` aprovados.
- Actions: SHAs de checkout, setup-python, upload-artifact e CodeQL conferidos nas fontes oficiais. A execução real do CodeQL permanece pendente do GitHub Actions.

O instante da última importação bem-sucedida ainda não é persistido no modelo `Cardapio`. O agendamento e os logs não representam atendimento completo de RNF02 nem do critério de exibição de atualização em RF01.

## Pendências e próximos passos

- Confirmar a fonte oficial e preencher horários por campus/refeição, sem inventar valores.
- Implementar S03-02 a S03-05 em mudanças próprias e vinculadas às decisões da ata.
- Registrar participantes e responsáveis reais na ata e vincular as issues/PRs da sprint.
- Ativar o serviço no ambiente escolhido e configurar os checks obrigatórios no GitHub.
- Manter para as próximas sprints: reclamações, aplicação da janela nas rotas de avaliação, planejamento, estimativa, teste de carga, corpus de PDFs, checagem de disponibilidade e deploy da aplicação.
