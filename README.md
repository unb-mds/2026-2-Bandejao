# Bandejão

Projeto acadêmico — Universidade de Brasília (UnB).

## Sobre

Aplicação para consulta ao cardápio semanal dos Restaurantes Universitários (RU) da UnB, abrangendo todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), com filtros alimentares, avaliação e registro de reclamações sobre refeições e, em uma segunda etapa, planejamento semanal de idas ao RU e estimativa de intenções por refeição.

## Equipe

- Arthur Pitanga Lopes Costa e Lima
- Gabriel Sousa Silva
- João Victor Tavares de Souza
- Gustavo Alves Bonfim
- Fábio Abelha Castro Gomes
- Maria Luiza Antunes de Oliveira
- João Pedro da Motta Laude

## Links úteis

- [Documentação no GitHub Pages](https://unb-mds.github.io/2026-2-Bandejao/)
- [Aplicação integrada em HTTPS](https://bandejao-unb-g12.onrender.com)
- [API e versão publicada](https://bandejao-unb-g12-api.onrender.com/version)
- [Figma](https://www.figma.com/board/61OYJuLeyE3m3jwzSzfZ1W/Bandejao-2026-2?t=kVJg4rR4m3kIYsj7-0)
- [Publicação e manutenção da GH Page](docs/github-pages.md)
- [Publicação da aplicação no Render](docs/publicacao.md)

## Status

🚧 Em desenvolvimento — situação revisada em 27/10/2026

- **Protótipo Vercel:** [Aceder ao Protótipo](https://frontend-react-tan-gamma.vercel.app)
- O frontend local usa React 19, Vite 8, TypeScript e Tailwind v4, incorporando as telas da equipe de [marilluantunes/frontend-react](https://github.com/marilluantunes/frontend-react). Campi, cardápios e histórico de avaliações vêm da API; os filtros usam as marcações dos itens. Avaliações e reclamações são enviadas à API e persistidas no banco. Planejamento e lotação continuam como demonstrações sem persistência integrada.
- Consulte [estrutura, execução e limites do frontend](frontend/README.md). O protótipo Vercel externo é uma publicação separada.


## Publicação da aplicação

A preparação para HTTPS está no [PR 71](https://github.com/unb-mds/2026-2-Bandejao/pull/71), da equipe. As URLs propostas retornaram 404 em 27/10/2026; a hospedagem integrada ainda depende de ativação e validação externa. Consulte [verificação da publicação](docs/verificacao-publicacao.md) para comandos, evidências e critérios pendentes da issue 55.

## Como rodar o projeto

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados

### Subindo o projeto (recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/unb-mds/2026-2-Bandejao.git
   cd 2026-2-Bandejao
   ```

2. Copie o arquivo de variáveis de ambiente do backend:
   ```bash
   cp backend/.env.example backend/.env
   ```
   No PowerShell, use `Copy-Item backend/.env.example backend/.env`.

   Defina `IMPORTACAO_TOKEN` em `backend/.env` com um segredo aleatório exclusivo do ambiente (por exemplo, gerado com `python -c "import secrets; print(secrets.token_urlsafe(32))"`). Não publique o valor. Backend e sincronizador usarão o mesmo arquivo; sem o token, a importação fica indisponível. O frontend não recebe esse segredo.

   Para personalizar a URL da API usada pelo frontend no Docker Compose, defina `VITE_API_BASE_URL` no arquivo `.env` da raiz (o padrão local é `http://localhost:8000`). Para executar o frontend fora do Docker, copie `frontend/.env.example` para `frontend/.env`.

3. Suba os serviços (banco de dados, backend e frontend):
   ```bash
   docker-compose up --build
   ```

4. Em outro terminal, aplique as migrações do banco de dados:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. Acesse:
   - **Backend (API):** http://localhost:8000 — documentação interativa em http://localhost:8000/docs
   - **Frontend:** http://localhost:5173

6. (Opcional) Popule o banco com dados de exemplo, para testar backend e frontend sem depender da extração real:
   ```bash
   docker-compose exec backend python -m app.db.seed
   ```
   Pode ser rodado quantas vezes for preciso — os dados de seed anteriores são removidos antes de inserir de novo.

### Rodando sem Docker (alternativa)

**Backend**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\Activate.ps1  |  Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajuste DATABASE_URL para seu PostgreSQL local
alembic upgrade head
python -m app.db.seed  # opcional: popula o banco com dados de exemplo
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Rodando os testes

```bash
# Backend
cd backend
pytest

# Extração
cd extracao
pytest

# Frontend
cd ../frontend
npm test
npm run lint
npm run build
```

### Sincronizando o cardápio real

#### GitHub Actions (ambiente publicado)

O workflow `Sincronizar cardápios` executa às 00:23, 06:23, 12:23 e 18:23 UTC, além de permitir execução manual. Antes de ativá-lo na `main`, configure em **Settings → Secrets and variables → Actions**:

- variável `BACKEND_URL`: URL HTTPS pública da API, sem token na URL;
- secret `IMPORTACAO_TOKEN`: o mesmo valor configurado no backend publicado.

Cada execução roda uma única sincronização, guarda por 30 dias os logs e metadados como artefato e impede sobreposição com `concurrency`. Agendamentos do GitHub Actions podem começar depois do horário previsto. Confira o [roteiro operacional](docs/desenvolvimento.md) e a [evidência da issue 54](docs/evidencias/sincronizacao-issue-54.md).

#### Docker Compose (host próprio)

Depois de configurar `IMPORTACAO_TOKEN`, iniciar a API e aplicar `alembic upgrade head`, ative o serviço opcional:

```bash
docker compose --profile sincronizacao up -d --build sincronizador
docker compose logs --tail=100 sincronizador
```

Ele consulta a fonte ao iniciar e repete a sincronização a cada seis horas enquanto o host e o Docker estiverem ativos. O serviço usa `http://backend:8000` na rede do Compose e autentica cada importação com Bearer token. Reinicie/recrie os serviços após trocar o segredo no ambiente. Para interromper só a rotina:

```bash
docker compose --profile sincronizacao stop sincronizador
```

Fora do Docker, exporte `IMPORTACAO_TOKEN` no processo da extração com o mesmo valor configurado no backend (o extrator não carrega automaticamente `backend/.env`). Então, com as dependências de `extracao/requirements.txt` instaladas:

```bash
cd extracao
python -m extracao.sincronizar --backend-url http://localhost:8000
# Opcional: manter a rotina periódica nesta sessão
python -m extracao.sincronizar --backend-url http://localhost:8000 --intervalo-segundos 21600
```

O modo periódico registra campus, URL da fonte e instante de cada importação concluída e continua após falhas externas. A API persiste o instante do último sucesso por campus; falhas preservam esse valor. Uma execução isolada com falhas retorna código diferente de zero. Consulte o [roteiro de operação](docs/desenvolvimento.md) e o [contrato de importação](docs/handoff_banco_e_importacao.md).

### Segurança estática no CI

O workflow `.github/workflows/sast.yml` analisa Python com Bandit e JavaScript/TypeScript com CodeQL em cada PR. Achados altos/críticos e falhas de análise reprovam os checks; relatórios são guardados como artefatos. O ruleset ativo da `main` exige os dois checks, sem bypass, conforme a [evidência de ativação](docs/evidencias/sast-issue-60.md). Veja nomes, comandos e política de severidade em [SAST](scripts/security/POLICY.md).

## Documentação e GitHub Pages

A GH Page reúne visão do produto, requisitos, arquitetura C4, dados, protótipos, sprints e estudos. É um site de documentação; API, banco e aplicação exigem ambiente próprio.

Com Python 3.12 e um ambiente virtual ativo, na raiz:

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
python -m mkdocs serve
```

A prévia usa `http://127.0.0.1:8000`; com a API nessa porta, use `python -m mkdocs serve -a 127.0.0.1:8001`.

O workflow valida alterações da documentação em pull requests e publica a partir da `main`. Em **Settings → Pages**, a origem deve ser **GitHub Actions**. Consulte [instruções completas](docs/github-pages.md) e [histórico das mudanças](docs/changelog.md).
