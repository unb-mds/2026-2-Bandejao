# contexto.md — Contexto do Projeto Bandejão

Este arquivo dá contexto para ferramentas de IA (Claude Code e similares) trabalharem neste repositório. Mantenha atualizado conforme o projeto evolui.

## Visão geral

**Bandejão** é uma aplicação que centraliza o cardápio semanal dos Restaurantes Universitários (RU) da UnB, abrangendo todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), permite filtrar refeições por restrição alimentar, avaliar refeições, registrar reclamações e salvar intenções de refeição para a semana. A API também apresenta estimativas por campus, data e refeição, conforme D05.

Projeto acadêmico, desenvolvido por uma equipe de 7 integrantes.

## Escopo por release

- **Release 1:** cardápio da semana, filtros alimentares (vegetariano, alergias), avaliação de refeições e registro independente de reclamações.
- **Release 2:** planejamento semanal persistido pela API e estimativa de intenções por dia, refeição e campus, sem previsão de horário de chegada ou tempo de fila. Dados simulados são consultados separadamente e identificados.

## Decisões D01–D08 (Requisitos v1.2, 14/10/2026)

Decisões tomadas pela equipe em `docs/Requisitos.md` (seção 7). O estado da implementação foi revisado em 10/11/2026; o histórico das entregas da Release 2 está em `docs/scrum/sprint05.md`.

- **D01:** semana de segunda a domingo, fuso `America/Sao_Paulo`.
- **D02:** filtro de dieta inclusivo — selecionar "ovolactovegetariano" também retorna itens "vegetariano estrito". As demais dietas continuam exatas. Implementado na API e na interface, com aviso sobre as limitações das marcações da fonte.
- **D03:** horários de início de cada refeição vêm de uma tabela de configuração versionada (sem horário cadastrado, a avaliação fica fechada). Sem recurso de "serviço suspenso" — limitação conhecida.
- **D04:** **sem cadastro nem login.** Identidade anônima por navegador (código aleatório gerado no cliente). Uma avaliação por identidade por refeição; novo envio atualiza a anterior em vez de duplicar. Não identifica pessoa: outro navegador, ou limpar os dados, gera outra identidade.
- **D05:** RF07 estima **demanda por refeição** (sem horário de chegada), com amostra mínima de 10 intenções ativas (constante de configuração). Dados de demonstração devem ser identificados como simulados.
- **D06:** reclamações com 4 categorias (qualidade, higiene, atendimento, outros), até 1.000 caracteres, sem foto, sem nome, sem lista pública. A decisão prevê acesso do autor e da equipe; o código atual oferece confirmação do envio ao autor e leitura interna por token, sem consulta posterior pelo autor.
- **D07:** metas de verificação — carga com k6 (50 usuários, local), sincronização a cada 6h, 4–6 PDFs de referência, SAST com bandit + CodeQL (bloqueia alto/crítico), checagem de 10s a cada 5min em janela curta.
- **D08 (novo, RNF06):** a rota de importação do cardápio exige um token secreto (`IMPORTACAO_TOKEN`), usado também pela rotina de sincronização. Sem segredo válido, a API recusa a escrita.

## Arquitetura

O sistema é dividido em camadas:

1. **Extração de dados** (`/extracao`) — lê o cardápio publicado pelo RU em PDF ou imagem e estrutura essa informação (parsing de texto ou OCR, dependendo do formato). Componente isolado por ser o ponto mais frágil do sistema: mudanças no formato do RU exigem ajuste apenas aqui.
2. **Backend / API** (`/backend`) — recebe os dados extraídos, aplica regras de negócio (filtros, avaliações) e expõe endpoints para o frontend. Endpoints já implementados (`backend/app/api/routes/`):
   - `GET /campi/`, `GET /campi/{campus_id}`
   - `GET /cardapios/` (filtros: `campus_id`, `data_inicio`/`data_fim`, `tipo_refeicao`, `tipo_dieta`, `excluir_alergenos` — implementa o filtro por restrição alimentar do RF03), `GET /cardapios/{cardapio_id}`
   - `GET /cardapios/{cardapio_id}/avaliacoes`, `POST /cardapios/{cardapio_id}/avaliacoes` (RF04/RF05)
   - `POST /cardapios/{cardapio_id}/reclamacoes/` (RF08) e `GET /equipe/reclamacoes/` (leitura interna por token da equipe).
   - `PUT`, `GET` e `DELETE /cardapios/{cardapio_id}/intencao/`, além de `GET /intencoes/` (RF06).
   - `GET /estimativas/` (RF07); exige campus e período e usa o mínimo configurado de 10 intenções ativas. `dados_simulados=true` consulta somente os dados simulados.
   - As rotas HTTP de check-in legado foram retiradas na Sprint 03; a tabela permanece como legado.
3. **Banco de dados** — armazena cardápios, avaliações, reclamações e intenções. `Intencao` registra uma identidade anônima por refeição, com estado ativo/cancelado e marcador de simulação. `CheckIn` é legado. Os demais modelos SQLAlchemy são `Campus`, `Cardapio`, `ItemCardapio`, `Avaliacao` e `Reclamacao`, além dos enums `TipoRefeicao`, `Categoria`, `TipoDieta` e `CategoriaReclamacao`. Migrações são gerenciadas por Alembic (`backend/alembic/`).
4. **Frontend** (`/frontend`) — usa React 19, Vite 8, TypeScript e Tailwind v4, incorporando as telas de `marilluantunes/frontend-react`. Campi, cardápios, avaliações, reclamações, planejamento e estimativas usam a API. As estimativas simuladas são identificadas na tela. A lotação continua demonstrativa, sem consulta a dados reais. O aviso de privacidade pode ser relido no rodapé. Veja `frontend/README.md` para estrutura e limites.

## Stack técnica

- Documentação/GitHub Pages: MkDocs Material, configuração em `mkdocs.yml`, dependências em `requirements-docs.txt`. O workflow `.github/workflows/docs.yml` valida PRs com build estrito e publica artefatos na `main`; requer origem **GitHub Actions** em Settings → Pages. Manutenção e histórico em `docs/github-pages.md` e `docs/changelog.md`.

- Extração de dados: Python (requests + BeautifulSoup para navegar a página do RU, pdfplumber para tabelas e Pillow para os ícones dos PDFs).
- Backend: Python + FastAPI, SQLAlchemy como ORM.
- Banco de dados: PostgreSQL.
- Frontend: React 19 + Vite 8, TypeScript e Tailwind v4.
- Orquestração local: Docker Compose (`docker-compose.yml` sobe banco, backend e frontend; o perfil opcional `sincronizacao` adiciona a rotina a cada seis horas).
- Testes: pytest (backend e extração) com cobertura via pytest-cov.
- Segurança estática: Bandit para Python e CodeQL para JavaScript/TypeScript, conforme RNF05; ambos são obrigatórios no ruleset ativo da `main`, sem bypass.
- Lint: Ruff (Python), Oxlint via `npm run lint` (frontend).

## Pendências em 10/11/2026

- A apresentação semanal ainda usa domingo a sábado, embora D01 defina segunda a domingo.
- A sincronização agendada não importou cardápios na última execução consultada: `BACKEND_URL` estava configurada, mas `IMPORTACAO_TOKEN` não estava disponível ao workflow. Veja a [execução de 10/11](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/42889503183).
- A disponibilidade atual do site e da API no Render não foi verificada. O histórico da publicação e os comandos de conferência estão em `docs/verificacao-publicacao.md`.
- As issues de dados #81 e #82 continuam abertas; a #82 já tem cinco PDFs válidos e resultados esperados, mas ainda falta o caso de falha exigido.

## Convenções do projeto

- Branches: uma branch por tarefa/issue (ex: `docs/83-arquivos-organizacao`), sem commits diretos na `main`. Convenção completa em [CONTRIBUTING.md](CONTRIBUTING.md).
- Pull Requests: obrigatórios para revisão antes de mesclar na `main`, com template em [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).
- Issues: cada tarefa (organizacional ou técnica) deve ter uma issue própria, vinculada a um milestone (Release 1 ou Release 2) e, quando aplicável, atribuída a um responsável. Templates em [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/).

## Comandos úteis

Com Docker (recomendado — sobe banco, backend e frontend juntos):

```
cp backend/.env.example backend/.env
docker compose up --build
```

Em outro terminal, aplique as migrações do banco de dados:

```
docker compose exec backend alembic upgrade head
```

- Backend (FastAPI): http://localhost:8000 — docs automáticas em `/docs`.
- Frontend (Vite): http://localhost:5173.

Sem Docker, rodando cada camada localmente:

```
# Backend
cd backend
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # ajuste DATABASE_URL para seu PostgreSQL local
alembic upgrade head
uvicorn app.main:app --reload

# Extração
cd extracao
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m extracao.main

# Frontend
cd frontend
npm install
npm run dev
```

Testes:

```
cd backend && pytest
cd extracao && pytest
```

## Fonte de dados do cardápio

- Página oficial: `https://ru.unb.br/cardapio-refeitorio/`
- Lista o cardápio de todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina, Fazenda Água Limpa); o projeto abrange **todos os campi**.
- Cada campus tem um link para um PDF hospedado em `ru.unb.br/wp-content/uploads/...`, com nome de arquivo seguindo um padrão (ex: `Gama-Semana-02-31-8-a-6-9.pdf`), mas **o link muda toda semana** — a extração deve percorrer a página HTML, identificar o link de cada campus e baixar/processar o PDF correspondente a cada um. Não fixar a URL do PDF no código.
- Não há API oficial.
- O cardápio identifica pratos que contêm leite, ovos, glúten, cogumelo, mel, soja, pimenta, oleaginosas, carne suína e frutos do mar, além de oferecer opções ovolactovegetariana e vegetariana estrita — essa informação da fonte viabiliza os filtros alimentares do projeto.

## Pontos de atenção

- O cardápio do RU não possui API oficial e é publicado apenas em PDF — o processo de extração é sensível a mudanças no formato de publicação. O site do RU avisa que o cardápio está sujeito a alterações sem aviso prévio.
- A estimativa de intenções (Release 2) depende de volume suficiente de planejamentos registrados por dia, refeição e campus; nas fases iniciais os dados podem ser insuficientes. Não representa medição da fila real.
- A abordagem de check-in no momento da refeição foi substituída pelo planejamento antecipado para reduzir a fricção de uso: o usuário registra suas intenções uma vez por semana, em vez de precisar lembrar de fazer check-in diariamente.
