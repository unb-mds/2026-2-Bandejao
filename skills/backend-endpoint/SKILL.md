---
name: backend-endpoint
description: Use esta skill sempre que for criar ou modificar um endpoint da API do backend. Aciona em pedidos como "criar endpoint de listagem do cardápio", "adicionar rota de avaliação", "implementar filtro por restrição alimentar na API".
---

# Backend / API — Bandejão

## Stack

FastAPI + SQLAlchemy + PostgreSQL, na pasta `/backend`.

## Estrutura de pastas

```
backend/app/
├── api/routes/    → um arquivo por recurso (ex: cardapio.py, avaliacao.py)
├── core/          → configuração (config.py)
├── db/            → sessão do banco (session.py)
├── models/        → modelos SQLAlchemy (tabelas)
└── schemas/       → schemas Pydantic (validação de entrada/saída da API)
```

## Convenções ao criar um novo endpoint

1. Criar o modelo SQLAlchemy em `app/models/` (se ainda não existir).
2. Criar os schemas Pydantic em `app/schemas/` para request/response.
3. Criar a rota em `app/api/routes/nome_do_recurso.py`, usando `APIRouter` (seguir o padrão de `health.py`).
4. Registrar o novo router em `app/main.py` com `app.include_router(...)`.
5. Escrever um teste em `backend/tests/` usando `TestClient`, seguindo o padrão de `test_health.py`.

## Regras do projeto

- Toda rota nova precisa de pelo menos um teste cobrindo o caso de sucesso.
- Usar injeção de dependência do FastAPI (`Depends(get_db)`) para acessar o banco — nunca abrir sessão manualmente dentro da rota.
- Nomear rotas e recursos em português, alinhado ao domínio do projeto (ex: `/cardapio`, `/avaliacoes`, não `/menu`, `/reviews`).
- Cardápio é sempre associado a um campus — todo endpoint relacionado a cardápio deve considerar o filtro por campus.

