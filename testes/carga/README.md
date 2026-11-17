# Teste de carga do cardápio (RNF01)

Mede quanto tempo a API de cardápio leva para responder quando 50 pessoas consultam ao mesmo tempo (RNF01, CA-RNF01-01 e CA-RNF01-02). Mede só a API, não o carregamento das telas.

- `gerar_massa.py`: cria os dados falsos (4 semanas, 5 campi, 3 refeições por dia e 10 itens por refeição) e salva `massa.json`.
- `cardapio.js`: o teste do k6.

## O que o teste faz

- 1 minuto de aquecimento (não conta no resultado) e depois 5 minutos de medição, com 50 usuários.
- Cada usuário faz uma consulta, espera 1 segundo e repete, alternando entre três tipos:
  - `semanal`: o cardápio da semana de um campus;
  - `dieta`: o mesmo, filtrando por dieta;
  - `exclusao`: o mesmo, excluindo um alérgeno.
- Uma consulta conta como falha se der erro, demorar mais de 10 s, não voltar 200 ou vier com conteúdo errado (por exemplo, um item com o alérgeno que devia ter sido excluído).
- **Passa** se o p95 de cada tipo for de até 2 segundos e se menos de 1% das consultas falhar.

## Como rodar

Precisa de Docker, [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) e Python 3.

```bash
# 1. Subir a API com PostgreSQL (defina IMPORTACAO_TOKEN no backend/.env)
docker compose up -d --build db backend
docker compose exec backend alembic upgrade head

# 2. Criar os dados falsos (mesmo token do backend/.env)
cd testes/carga
IMPORTACAO_TOKEN=seu-token python gerar_massa.py

# 3. Rodar o teste (leva uns 6 minutos)
k6 run cardapio.js
```

No PowerShell, troque o passo 2 por `$env:IMPORTACAO_TOKEN = "seu-token"` e depois `python gerar_massa.py`.

No fim, o k6 mostra um ✓ ou ✗ em cada limite, o p95 e a quantidade de consultas de cada tipo, e a porcentagem de checks que passaram. Para apagar os dados falsos, use `docker compose down -v`, que apaga o banco local.

Para só conferir se o script funciona, dá para rodar mais rápido com `VUS=5 AQUECIMENTO=5s MEDICAO=20s k6 run cardapio.js`. Isso **não** vale como medição.

## Relatório

Salve o resultado em `docs/evidencias/carga-rnf01-AAAA-MM-DD.md` com:

- data e commit testado;
- máquina (CPU, memória, sistema) e onde o k6 rodou;
- versões do k6, do PostgreSQL e do Docker;
- estado do cache (a API não tem cache; dizer se o banco foi reiniciado antes);
- quantidade de consultas e p95 de cada tipo, e a taxa de falhas;
- se passou ou não. Se não passou, anote o resultado como ficou e a causa provável.
