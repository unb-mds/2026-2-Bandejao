# Bandejão

Projeto acadêmico — Universidade de Brasília (UnB).

## Sobre

Aplicação para consulta ao cardápio semanal dos Restaurantes Universitários (RU) da UnB, abrangendo todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), com filtros alimentares, avaliação de refeições e, em uma segunda etapa, previsão de horário de pico da fila.

## Equipe

- Arthur Pitanga Lopes Costa e Lima
- Gabriel Sousa Silva
- João Victor Tavares de Souza
- Gustavo Alves Bonfim
- Fábio Abelha Castro Gomes
- Maria Luiza Antunes de Oliveira
- João Pedro da Motta Laude

## Status

🚧 Em desenvolvimento — Sprint 01

## Como rodar o projeto

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados

### Subindo o projeto (recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/unb-mds/G12-2026-2.git
   cd G12-2026-2
   ```

2. Copie o arquivo de variáveis de ambiente do backend:
   ```bash
   cp backend/.env.example backend/.env
   ```

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

### Rodando sem Docker (alternativa)

**Backend**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\Activate.ps1  |  Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajuste DATABASE_URL para seu PostgreSQL local
alembic upgrade head
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
```
