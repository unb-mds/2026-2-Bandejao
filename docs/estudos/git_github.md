# Git e GitHub — Estudo

## O que é Git

Git é um sistema de controle de versão. Ele registra o histórico de mudanças em um conjunto de arquivos ao longo do tempo, permitindo voltar a versões anteriores, comparar mudanças e trabalhar em paralelo com outras pessoas sem sobrescrever o trabalho alheio.

Diferente de simplesmente salvar cópias de uma pasta, o Git guarda "fotografias" (commits) do projeto em pontos específicos, com uma mensagem explicando o que mudou e quem mudou.

## O que é GitHub

GitHub é uma plataforma que hospeda repositórios Git na nuvem e adiciona ferramentas de colaboração em cima do Git puro: issues, pull requests, revisão de código, milestones, labels, etc. O Git funciona sem o GitHub (é possível usar Git só localmente), mas o GitHub é o que permite que várias pessoas trabalhem juntas no mesmo repositório remoto.

## Conceitos fundamentais

### Repositório (repo)
Uma pasta de projeto rastreada pelo Git. Contém todos os arquivos e todo o histórico de mudanças.

### Commit
Um "ponto de salvamento" no histórico do projeto. Cada commit tem um identificador único, uma mensagem descrevendo a mudança e um autor. Commits pequenos e com mensagens claras facilitam entender o histórico depois.

### Branch (ramificação)
Uma linha de desenvolvimento independente dentro do mesmo repositório. A branch principal costuma se chamar `main`. Ao criar uma nova branch (ex: `feature/extracao-pdf`), é possível trabalhar em uma funcionalidade sem afetar o código que já está estável na `main`.

### Merge
A ação de unir as mudanças de uma branch em outra — por exemplo, trazer o que foi feito em `feature/extracao-pdf` de volta para a `main`.

### Clone
Copiar um repositório remoto (do GitHub) para a máquina local, criando uma cópia completa com todo o histórico.

### Pull / Push
- **Pull**: trazer para a máquina local as mudanças que estão no repositório remoto.
- **Push**: enviar para o repositório remoto as mudanças feitas localmente.

## Fluxo de colaboração no GitHub

1. Criar uma branch a partir da `main` para a tarefa que será feita.
2. Fazer as alterações e registrar commits nessa branch.
3. Enviar (push) a branch para o GitHub.
4. Abrir um **Pull Request (PR)**: uma solicitação para que as mudanças da branch sejam incorporadas à `main`.
5. Outra pessoa do grupo revisa o PR (code review), comenta ou aprova.
6. Após aprovado, o PR é mesclado (merge) na `main`.

Esse fluxo evita que código sem revisão vá direto para a branch principal, e mantém um histórico organizado de quem fez o quê.

## Issues

Issues são unidades de tarefa ou problema dentro do repositório — usadas tanto para bugs quanto para funcionalidades a implementar ou tarefas organizacionais. Podem ser atribuídas a uma pessoa, associadas a um milestone (ex: uma sprint ou release) e marcadas com labels (categorias).

## Milestones e Labels

- **Milestone**: agrupa issues em torno de um objetivo com prazo (ex: "Release 1", "Sprint 00"), permitindo acompanhar o progresso geral daquele objetivo.
- **Label**: uma etiqueta usada para categorizar issues (ex: `bug`, `estudo`, `frontend`), facilitando filtrar e organizar o backlog.

## Boas práticas

- Mensagens de commit curtas e descritivas (ex: `docs: adiciona README inicial`).
- Uma branch por tarefa, não misturar várias mudanças não relacionadas em um único PR.
- Nunca commitar diretamente na `main` em um projeto colaborativo — sempre passar por PR e revisão.
- Fazer `pull` antes de começar a trabalhar, para garantir que a branch local está atualizada.

## Dúvidas em aberto

*(preencher conforme surgirem dúvidas durante o uso prático)*
