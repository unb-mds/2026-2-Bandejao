# Contribuindo para o Bandejão

O Bandejão é um projeto acadêmico desenvolvido pela equipe da disciplina
MDS 2026/2 (UnB). Este documento descreve como o grupo trabalha no
repositório. Todas as tarefas são acompanhadas de uma issue no GitHub e
vinculadas a um milestone (Release 1 ou Release 2).

## Fluxo de trabalho

1. **Uma branch por tarefa.** Cada issue gera uma branch a partir da
   `main` atualizada, com nome no padrão `tipo/numero-descricao`
   (ex.: `feature/58-configuracao-horarios`, `docs/84-sprint05`,
   `fix/61-janela-avaliacao`).
2. **Sem commits diretos na `main`.** Todo trabalho entra na `main`
   por Pull Request. A `main` é protegida: o SAST (Bandit para Python e
   CodeQL para JavaScript/TypeScript) precisa estar aprovado e a branch
   atualizada antes do merge.
3. **Revisão por outra pessoa.** O PR deve ser revisado por um integrante
   diferente do autor antes do merge. A revisão técnica do autor não
   substitui a revisão do colega.
4. **Issues vinculadas.** Todo PR referencia a issue que atende
   (`Closes #41` ou `Refs #41`). Cada commit também cita a issue
   solicitada (`(#41)` no fim da mensagem).
5. **Dependências entre PRs.** Quando uma entrega depende de outra,
   o PR indica a dependência e a ordem de integração. Não empilhe
   implementações de issues diferentes numa mesma branch.

## Mensagens de commit

Seguimos o padrão `tipo: descrição`, sempre em português e sem acento:

| Tipo       | Uso                                                     |
|------------|---------------------------------------------------------|
| `feat`     | Nova funcionalidade ou entrega de requisito              |
| `fix`      | Correção de comportamento existente                     |
| `docs`     | Documentação (docs/, README, changelog)                 |
| `chore`    | Configuração, CI, ferramentas, organização do repo      |
| `refactor` | Reorganização de código sem mudar comportamento         |
| `test`     | Apenas testes                                           |

Exemplos reais do projeto: `feat: avaliações integradas à API`,
`docs: sincronização automática a cada seis horas`,
`fix: corrige sincronização dos PDFs oficiais do RU`.

Inclua o número da issue quando a entrega estiver ligada a ela:
`feat: implementa intenções de refeição (#76)`.

## Desenvolvendo

- **Backend**: siga o contrato documentado em `backend/README.md` e os
  padrões dos módulos existentes em `backend/app/` (rotas em
  `app/api/routes/`, modelos SQLAlchemy em `app/models/`, schemas em
  `app/schemas/`). Rode `pytest` e `ruff check` antes de abrir o PR.
- **Frontend**: React 19 + Vite + TypeScript + Tailwind v4. Rode
  `npm test`, `npm run lint` e `npm run build` antes de abrir o PR.
- **Extração**: qualquer mudança de formato no PDF do RU é ajustada só
  em `extracao/`. Rode `pytest` e confira a regressão com os PDFs de
  referência.

## Documentação

- Decisões de produto e requisitos ficam em `docs/Requisitos.md`
  (seção 7: decisões D01–D08).
- O contexto rápido do projeto está em `contexto.md` — mantenha
  atualizado quando mudar decisões, arquitetura ou stack.
- Mudanças de comportamento e de documentação devem ser registradas em
  `docs/changelog.md`.
- O site de documentação (MkDocs) só aceita `mkdocs build --strict`
  sem erros: confirme localmente antes do PR.

## Como rodar o projeto

Veja o [README](README.md): Docker Compose sobe banco, backend e
frontend; depois aplique `alembic upgrade head` e, se quiser, rode o
seed de exemplo.

Também leia o [Código de Conduta](CODE_OF_CONDUCT.md) e a
[Licença](LICENSE) do projeto.
