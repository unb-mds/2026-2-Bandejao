# Histórico de mudanças da documentação

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
