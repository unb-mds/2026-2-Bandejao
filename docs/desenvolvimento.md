# Executar o projeto

Este roteiro sobe o ambiente local. A GitHub Page publica somente a documentação; os serviços da aplicação precisam de ambiente próprio.

## Pré-requisitos

- Git para clonar o repositório.
- Docker com Docker Compose para executar PostgreSQL, API e frontend.
- Portas 5432, 8000 e 5173 disponíveis.

## Iniciar com Docker

```bash
git clone https://github.com/unb-mds/2026-2-Bandejao.git
cd 2026-2-Bandejao
```

Copie o arquivo de configuração antes de iniciar. Em Linux/macOS:

```bash
cp backend/.env.example backend/.env
```

No PowerShell:

```powershell
Copy-Item backend/.env.example backend/.env
```

Inicie os serviços:

```bash
docker compose up --build
```

Em outro terminal, na raiz do repositório, aplique as migrações:

```bash
docker compose exec backend alembic upgrade head
```

Acesse o frontend em <http://localhost:5173> e a documentação da API em <http://localhost:8000/docs>.

Para inserir dados de exemplo, execute:

```bash
docker compose exec backend python -m app.db.seed
```

O seed substitui seus dados de exemplo anteriores; não comprova atualização pela fonte oficial. Consulte [banco e importação](handoff_banco_e_importacao.md) antes de importar dados reais.

## Papel do Docker

O Compose padroniza o ambiente e inicia banco, backend e frontend. O frontend usa uma prévia do build estático. A extração não é iniciada nem agendada pelo Compose. O volume `db_data` preserva o banco entre reinícios.

Para encerrar os serviços preservando esse volume:

```bash
docker compose down
```

## Testes e execução alternativa

As instruções de execução sem Docker, testes com pytest e sincronização estão no [README do repositório](https://github.com/unb-mds/2026-2-Bandejao/blob/main/README.md). Os testes da aplicação verificam backend e extração; a validação do site verifica a geração da documentação. Consulte o [estado da arquitetura](Arquitetura.md) para distinguir implementação de funcionalidades planejadas.
