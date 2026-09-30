# Histórico de mudanças da documentação

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
