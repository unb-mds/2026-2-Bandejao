# Histórico de mudanças da documentação

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
