# 🍽️ Bandejão

Projeto acadêmico — Universidade de Brasília (UnB).

---

## 📌 Sobre

Aplicação para consulta ao cardápio semanal dos Restaurantes Universitários (RU) da UnB, abrangendo todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa). O sistema conta com filtros alimentares, avaliação e registo de reclamações sobre refeições e, numa segunda etapa, planeamento semanal de idas ao RU e estimativa de horário de pico da fila.

---

## 👥 Equipe

* Arthur Pitanga Lopes Costa e Lima
* Gabriel Sousa Silva
* João Victor Tavares de Souza
* Gustavo Alves Bonfim
* Fábio Abelha Castro Gomes
* Maria Luiza Antunes de Oliveira
* João Pedro da Motta Laude

---

## 🚀 Status

🚧 **Em desenvolvimento** — Sprint 01

---

## ⚙️ Como rodar o projeto

### Pré-requisitos
* **Docker** e **Docker Compose** instalados na máquina.

### Subindo o projeto (Recomendado)

1. Clone o repositório:
   ```bash
   git clone [https://github.com/unb-mds/G12-2026-2.git](https://github.com/unb-mds/G12-2026-2.git)
   cd G12-2026-2
Copie o ficheiro de variáveis de ambiente do backend:

Bash
cp backend/.env.example backend/.env
Suba os serviços (banco de dados, backend e frontend):

Bash
docker-compose up --build
Noutro terminal, aplique as migrações do banco de dados:

Bash
docker-compose exec backend alembic upgrade head
Acesse:

Backend (API): http://localhost:8000 (documentação interativa em http://localhost:8000/docs)

Frontend: http://localhost:5173

(Opcional) Popule o banco com dados de exemplo para testar o backend e o frontend sem depender da extração real:

Bash
docker-compose exec backend python -m app.db.seed
Nota: Pode ser rodado quantas vezes for preciso — os dados de seed anteriores são removidos antes de inserir de novo.

Rodando sem Docker (Alternativa de Desenvolvimento)
Backend
Bash
cd backend
python -m venv venv
# Windows: venv\Scripts\Activate.ps1  |  Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajuste DATABASE_URL para o seu PostgreSQL local
alembic upgrade head
python -m app.db.seed  # opcional: popula o banco com dados de exemplo
uvicorn app.main:app --reload
Frontend
Bash
cd frontend
npm install
npm run dev
🧪 Rodando os Testes Automatizados
Testes do Backend:

Bash
cd backend
pytest
Testes do Extrator:

Bash
cd extracao
pytest
🔄 Sincronizando o Cardápio Real
Com o backend em execução, a extração pode baixar os PDFs atuais e importá-los na API:

Bash
cd extracao
python -m extracao.sincronizar --backend-url http://localhost:8000
Para deixá-la em execução periódica, informe o intervalo desejado em segundos; por exemplo, a cada seis horas:

Bash
python -m extracao.sincronizar --backend-url http://localhost:8000 --intervalo-segundos 21600
Dica: Antes de importar, certifique-se de que aplicou as migrações mais recentes no backend (alembic upgrade head).
