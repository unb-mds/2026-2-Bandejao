# Sprint 01 — Estruturação

**Objetivo da sprint:** sair do estudo conceitual (Sprint 00) e decidir/estruturar a base técnica do projeto — requisitos, arquitetura, stack e setup inicial do repositório de código.

## O que foi feito

### Documentação formalizada
- `docs/Requisitos.md` — requisitos funcionais (RF01-RF07) e não funcionais (RNF01-RNF06) documentados, cobrindo Release 1 e Release 2
- `docs/Arquitetura.md` — arquitetura em 4 camadas documentada (extração, backend, banco de dados, frontend) e fluxo de dados entre elas
- `README.md` — atualizado com seção "Como rodar o projeto" (setup via Docker e alternativa local)

### Stack técnica definida

| Camada | Tecnologia |
|---|---|
| Extração de dados | Python (requests, BeautifulSoup, pdfplumber) |
| Backend / API | Python + FastAPI |
| Banco de dados | PostgreSQL |
| Frontend | React + Vite |

### Modelagem do banco de dados
Entidades definidas: `Campus`, `Cardapio`, `ItemCardapio`, `Avaliacao`, `CheckIn` (Release 2). Modelagem revisada com base no cardápio real do RU (categorias como Salada, Prato Principal, Panificação etc., e classificação por tipo de dieta: padrão, ovolactovegetariano, vegetariano estrito).

### Setup do repositório de código
- Estrutura inicial criada: `/backend`, `/frontend`, `/extracao`
- Backend: FastAPI configurado, endpoint de teste `/health`, conexão com banco via SQLAlchemy
- Modelos de dados implementados em `backend/app/models/`, refletindo a modelagem definida
- Alembic configurado para migrações, com migração inicial gerada
- `docker-compose.yml` orquestrando banco, backend e frontend
- Skills de IA criadas (`skills/extracao-cardapio`, `skills/backend-endpoint`, `skills/frontend-componente`) para apoiar o uso de ferramentas de IA no padrão do projeto

## Papéis definidos até o momento

- **Gustavo** — Scrum Master + Banco de dados + Extração
- Demais papéis (Backend, Frontend)

## Pendências / próximos passos

- Validar que o ambiente sobe corretamente via `docker compose up --build` em uma máquina limpa
- Aplicar a migração inicial no banco de dados
- Garantir que todos os integrantes tenham acesso efetivo ao repositório (problema identificado: parte do grupo não está na organização do GitHub)
- Iniciar a extração real do cardápio (hoje a extração é um esqueleto, ainda sem implementação)
- Backend e Frontend seguem sem endpoints/telas reais implementadas — dependem da extração/modelagem já estarem prontas
