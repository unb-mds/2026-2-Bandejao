# Histórico de mudanças da documentação

## 27/10/2026 — Agendamento da sincronização a cada seis horas

- Workflow do GitHub Actions executa a extração/importação às 00:23, 06:23, 12:23 e 18:23 UTC, ou manualmente.
- URL da API vem de variável e token vem de secret; configuração ausente ou URL sem HTTPS falha antes do acesso à fonte.
- Concorrência impede ciclos sobrepostos, e cada execução preserva logs e metadados por 30 dias.
- Pull requests executam somente os testes do sincronizador e a regressão offline dos cinco PDFs oficiais.
- A ativação operacional depende da publicação da API e da configuração dos valores protegidos; atrasos do agendador continuam documentados.

## 27/10/2026 — Revisão de consistência após o PR 72

- README, contexto, arquitetura, requisitos, desenvolvimento e protótipos passam a registrar avaliações e reclamações como fluxos integrados à API, com persistência; planejamento e lotação continuam demonstrativos.
- Diagrama e tabela do banco incluem `Reclamacao`; interfaces documentam envio e leitura interna por token. A confirmação ao autor não equivale a uma consulta posterior implementada.
- Corrigidas referências antigas à última importação, ao lint do frontend e à proteção da `main`. Visão e página inicial passam a seguir D05: intenções por refeição, com mínimo de 10, sem previsão de horário.
- Sprints preservam os registros históricos e apontam para a situação consolidada. Plano de execução registra a entrega remota concluída e as pendências operacionais de sincronização e hospedagem.

## 27/10/2026 — Verificação da publicação HTTPS

- Issue 55: acrescentado verificador somente leitura de HTTPS, HTML, healthcheck, versão, dados públicos e CORS/preflight, com testes na CI.
- Inspeção do PR 71 preserva os três commits da equipe; registra cuidados com branch do Blueprint, versão Python, seed por data e ausência do sincronizador nessa configuração.
- URLs propostas responderam 404. Sem acesso Render, a publicação continua pendente; código/configuração aprovados não são evidência de ambiente ativo. Veja [roteiro e registro](verificacao-publicacao.md).

## 27/10/2026 — Aviso de privacidade

- Issue 53: aviso acessível na primeira visita, confirmação versionada por navegador e releitura no rodapé. Armazenamento bloqueado não impede o uso.
- Texto explica identificador aleatório, limpeza dos dados, persistência de envios, comentários públicos e reclamações privadas; a confirmação registra leitura, sem alegar consentimento legal.
- Vinte e sete testes, lint, TypeScript e build aprovados. Teclado, foco, Escape, persistência e layout mobile conferidos no Chrome com API simulada. Veja [texto e evidências](privacidade.md).

## 27/10/2026 — Correção da sincronização dos PDFs oficiais

- Issue 54: descoberta de arquivos com revisão numérica, decodificação JPEG e isolamento de falhas inesperadas por campus.
- Importações concluídas registram fonte e instante sem divulgar tokens. O agendamento do Compose permanece em seis horas.
- Cinco PDFs reais produziram 84 refeições e 757 itens. Duas importações em SQLite isolado preservaram IDs, cinco avaliações e cinco reclamações. Extração e backend passaram em 54 e 94 testes, respectivamente; cobertura de 100% e Ruff aprovados.
- A operação contínua na hospedagem permanece dependente de ativação. Veja a [evidência da issue 54](evidencias/sincronizacao-issue-54.md).

## 24/10/2026 — Avaliações integradas à API

**Escopo:** implementação da issue 51 e dos critérios de RF04/RF05.

- O formulário envia nota geral e comentário com a identidade anônima do navegador e apresenta os erros devolvidos pela API.
- O histórico consulta o ID exato da refeição, apresenta data/hora no fuso de Brasília e mantém a ordem do registro mais recente para o mais antigo.
- Refeições sem registros exibem "sem avaliações", sem preencher notas fictícias; os dados permanecem após recarregar a página.
- Campos demonstrativos que não pertenciam ao contrato persistido foram retirados da avaliação.

**Verificação local:** 92 testes do backend passaram com 100% de cobertura; 19 testes do frontend e TypeScript aprovados.

## 24/10/2026 — Última importação bem-sucedida por campus

**Escopo:** implementação da issue 50, CA-RF01-03 e CA-RNF02-03.

- O campus passa a guardar, de forma atômica, o instante em UTC e a URL da fonte da última importação confirmada.
- A API devolve os metadados nas consultas de campus e na resposta da importação.
- A tela do cardápio apresenta data/hora no fuso de Brasília junto ao link da fonte.
- Requisições inválidas e falhas anteriores à confirmação preservam o último sucesso conhecido.
- Uma migração reversível adiciona as duas colunas sem inventar valores para dados anteriores.

**Verificação local:** 93 testes do backend passaram com 100% de cobertura; 17 testes do frontend, Ruff e TypeScript aprovados.


## 18/10/2026 — Filtro de dieta inclusivo

**Escopo:** implementação da decisão D02 e dos critérios de RF03.

- A seleção ovolactovegetariana inclui itens vegetarianos estritos na API e na interface; comum, padrão e vegetariano estrito permanecem exatos.
- O painel de filtros e o cardápio avisam que “sem marcação” significa “não marcado na fonte”, não “livre de”.
- Testes cobrem as quatro classes de dieta e a combinação usada pelo filtro local.

**Verificação local:** 50 testes do backend passaram com 100% de cobertura; 16 testes do frontend, Ruff, lint, TypeScript e build Vite aprovados.

## 15/10/2026 — Ativação do SAST na `main`

**Escopo:** conclusão operacional de RNF05 e D07d.

- Bandit e CodeQL confirmados em Pull Request real, com os dois jobs aprovados.
- Artefatos das duas análises baixados e inspecionados; nenhum achado alto ou crítico.
- Ruleset ativo na `main`, sem bypass, exige os dois checks e branch atualizada antes do merge.
- Links, SHAs, resultados e comandos de reprodução registrados na evidência da issue 60.

## 15/10/2026 — Horários e janela de avaliação

**Escopo:** base de negócio das decisões D03 e D05.

- Horários de início de café da manhã, almoço e jantar centralizados na configuração, com referência à página oficial do RU.
- Função de elegibilidade criada com a janela entre o início do serviço e antes de 00h do dia seguinte, no fuso de Brasília; refeição sem horário permanece fechada.
- Amostra mínima da estimativa centralizada com o valor 10.
- Testes cobrem os quatro limites da janela, conversão de fuso e ausência de configuração.

**Verificação local:** 40 testes do backend passaram com 100% de cobertura; Ruff aprovado.

## 14/10/2026 — Base de infraestrutura da Sprint 03

**Escopo:** SAST, sincronização periódica, proteção da importação e documentação operacional; sem implementação de tempo, dieta, identidade anônima, reclamações ou planejamento.

- Importação protegida por Bearer token compartilhado entre backend e sincronizador; sem configuração válida, a escrita é recusada.
- Rotas HTTP de check-in legado retiradas, preservando modelo e banco para migração futura.
- Serviço opcional do Docker Compose executa a sincronização ao iniciar e a cada seis horas, sem sobrepor ciclos.
- Workflow SAST adiciona Bandit para Python e CodeQL para JavaScript/TypeScript, com gate para achados altos/críticos e relatórios como artefatos.
- Sprint 03 diferencia a proposta de votação das decisões efetivamente registradas na ata e delimita o recorte implementado nesta branch.

**Verificação local:** 22 testes do backend, 41 da extração e 10 do gate SAST passaram; backend e extração mantiveram 100% de cobertura. Ruff, `docker compose config --quiet`, `git diff --check`, Bandit sobre os arquivos Python rastreados e `mkdocs build --strict` passaram. Os SHAs das Actions foram conferidos nos repositórios oficiais.

**Limites:** o daemon Docker não estava disponível, portanto os containers não foram iniciados nem houve importação real. CodeQL precisa executar no GitHub Actions, e a obrigatoriedade dos checks depende da proteção/ruleset da `main`.

## 01/10/2026 — Alinhamento do frontend com as telas da equipe

**Escopo:** integração do frontend da equipe ao repositório principal e alinhamento da documentação. A publicação da aplicação e a atualização do Vercel externo não fazem parte desta entrega.

- Stack alinhada com o trabalho da equipe: React 19, Vite 8, TypeScript e Tailwind v4, incorporando `marilluantunes/frontend-react` na revisão `c1833a3`.
- README, contexto, arquitetura, desenvolvimento, protótipos e Sprint 02 descrevem a consulta integrada e os limites das demonstrações. RNF05 passa a mencionar TypeScript entre as linguagens a analisar; isso não comprova execução de SAST.
- Cliente HTTP tipado e adaptação dos dados substituem cardápios/avaliações fictícios da consulta. Seleção semanal, origem PDF, falhas e marcadores alimentares são tratados na interface.
- D01/D02 permanecem pendentes; não foi registrada aprovação das convenções do protótipo nem aceite de requisitos de persistência.

**Verificação local:** nove testes do cliente/adaptação passaram; lint sem avisos; TypeScript e build Vite passaram; MkDocs compilou com `--strict`. Navegador Chrome em desktop e mobile foi conferido com respostas simuladas da API, incluindo navegação, categorias, filtros, erro/nova tentativa e falta de registros/campi. As capturas locais não comprovam operação com PostgreSQL/API reais, publicação remota ou aceite da equipe.

## 30/09/2026 — Organização da GitHub Page

**Escopo:** documentação e infraestrutura de publicação; sem alterações no código da aplicação.

- URL canônica do site configurada e navegação ampliada para estudos, desenvolvimento, protótipos e manutenção.
- Instruções de execução acessíveis pela página; endereço de clone corrigido no README.
- Links existentes de Figma e protótipo reunidos, com roteiro relacionado aos requisitos e pendências explícitas.
- Workflow substituído por build estrito em PRs e publicação de artefato pela integração oficial do GitHub Pages na `main`, sem commits automáticos de deploy.
- Versões principais das dependências do site fixadas em `requirements-docs.txt`.
- Registro na Sprint 02 e contexto do repositório atualizados.

**Verificação realizada:** `python -m mkdocs build --strict` concluído com sucesso em Python 3.12; 22 páginas HTML geradas e 874 referências locais a páginas/arquivos conferidas, sem destinos ausentes. `git diff --check` sem erros de whitespace. A conferência local não verificou âncoras, links externos ou renderização de Mermaid no navegador. Publicação remota depende da integração na `main`, da seleção de GitHub Actions em Settings → Pages e da aprovação do workflow.

Os registros anteriores permanecem no histórico Git e nas páginas das sprints. Esta mudança não certifica aceitação dos requisitos nem substitui atas e evidências dos responsáveis.
