# CLAUDE.md — Contexto do Projeto Bandejão

Este arquivo dá contexto para ferramentas de IA (Claude Code e similares) trabalharem neste repositório. Mantenha atualizado conforme o projeto evolui.

## Visão geral

**Bandejão** é uma aplicação que centraliza o cardápio semanal dos Restaurantes Universitários (RU) da UnB, abrangendo todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), permite filtrar refeições por restrição alimentar, permite avaliação de refeições pelos usuários e, em uma segunda etapa, estima horários de pico de fila com base em histórico de check-ins.

Projeto acadêmico, desenvolvido por uma equipe de 7 integrantes.

## Escopo por release

- **Release 1:** cardápio da semana, filtros alimentares (vegetariano, alergias), avaliação de refeições.
- **Release 2:** previsão de horário de pico de fila, a partir do histórico de check-ins dos usuários.

## Arquitetura

O sistema é dividido em camadas:

1. **Extração de dados** (`/extracao` — ajustar caminho quando definido) — lê o cardápio publicado pelo RU em PDF ou imagem e estrutura essa informação (parsing de texto ou OCR, dependendo do formato). Componente isolado por ser o ponto mais frágil do sistema: mudanças no formato do RU exigem ajuste apenas aqui.
2. **Backend / API** (`/backend` — ajustar caminho quando definido) — recebe os dados extraídos, aplica regras de negócio (filtros, avaliações) e expõe endpoints para o frontend.
3. **Banco de dados** — armazena cardápio, avaliações e (Release 2) histórico de check-ins.
4. **Frontend** (`/frontend` — ajustar caminho quando definido) — consome a API e exibe cardápio, filtros e interface de avaliação para o usuário.

## Stack técnica

> A completar assim que o grupo definir linguagens, frameworks e ferramentas de cada camada.

- Extração de dados:
- Backend:
- Banco de dados:
- Frontend:

## Convenções do projeto

> A completar conforme o grupo definir. Sugestões:

- Branches: uma branch por tarefa/issue (ex: `feature/extracao-cardapio`), sem commits diretos na `main`.
- Pull Requests: obrigatórios para revisão antes de mesclar na `main`.
- Issues: cada tarefa (organizacional ou técnica) deve ter uma issue própria, vinculada a um milestone (Release 1 ou Release 2) e, quando aplicável, atribuída a um responsável.

## Comandos úteis

> A completar assim que o setup do projeto estiver definido (ex: como instalar dependências, rodar o backend, rodar o frontend, rodar o script de extração).

## Fonte de dados do cardápio

- Página oficial: `https://ru.unb.br/cardapio-refeitorio/`
- Lista o cardápio de todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina, Fazenda Água Limpa); o projeto abrange **todos os campi**.
- Cada campus tem um link para um PDF hospedado em `ru.unb.br/wp-content/uploads/...`, com nome de arquivo seguindo um padrão (ex: `Gama-Semana-02-31-8-a-6-9.pdf`), mas **o link muda toda semana** — a extração deve percorrer a página HTML, identificar o link de cada campus e baixar/processar o PDF correspondente a cada um. Não fixar a URL do PDF no código.
- Não há API oficial.
- O cardápio identifica pratos que contêm leite, ovos, glúten, cogumelo, mel, soja, pimenta, oleaginosas, carne suína e frutos do mar, além de oferecer opções ovolactovegetariana e vegetariana estrita — essa informação da fonte viabiliza os filtros alimentares do projeto.

## Pontos de atenção

- O cardápio do RU não possui API oficial e é publicado apenas em PDF — o processo de extração é sensível a mudanças no formato de publicação. O site do RU avisa que o cardápio está sujeito a alterações sem aviso prévio.
- A previsão de fila (Release 2) depende de volume suficiente de check-ins registrados; nas fases iniciais os dados podem ser insuficientes para gerar estimativas confiáveis.
