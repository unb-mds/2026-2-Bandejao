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

Antes de iniciar, preencha `IMPORTACAO_TOKEN` em `backend/.env` com um segredo aleatório exclusivo do ambiente. Backend e sincronizador compartilham esse valor; o frontend não o utiliza. Não publique o arquivo `.env`.

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

O Compose padroniza o ambiente e inicia banco, backend e frontend. O frontend usa uma prévia do build estático. O perfil opcional `sincronizacao` adiciona a extração periódica, ativada separadamente após as migrações. O volume `db_data` preserva o banco entre reinícios.

Para encerrar os serviços preservando esse volume:

```bash
docker compose down
```

## Sincronização a cada seis horas

Após as migrações e a configuração do token, na raiz do repositório:

```bash
docker compose --profile sincronizacao up -d --build sincronizador
docker compose logs --tail=100 sincronizador
```

O serviço aguarda a API responder ao endpoint de saúde, executa imediatamente e usa 21.600 segundos entre os inícios dos ciclos, descontando o tempo de execução. Um ciclo que exceda seis horas não dispara outra instância em paralelo; o próximo começa assim que o anterior termina. Falhas da fonte/API são registradas e não encerram o laço. O reinício do container inicia uma nova execução; isso é seguro para a chave de reimportação, mas não significa garantia de execução quando o host estiver desligado.

O serviço compartilha `backend/.env`, usa `BACKEND_URL=http://backend:8000` e não acessa diretamente o banco. Aplique as migrações antes de ativá-lo. Logs informam instante UTC, campus e status; para diagnóstico, confira também os logs do backend. Não registre credenciais nem o cabeçalho de autorização em logs.

```bash
# Parar apenas o sincronizador
docker compose --profile sincronizacao stop sincronizador
# Recriar após alterar o token em backend/.env
docker compose up -d --force-recreate backend
docker compose --profile sincronizacao up -d --force-recreate sincronizador
```

A política `unless-stopped` reinicia o serviço após falhas/reinício do Docker, exceto quando ele foi parado explicitamente. A rotina exige token antes de acessar a fonte. Uma falha de configuração deve ser corrigida antes de tentar novamente. Para execução manual fora do Docker, exporte `IMPORTACAO_TOKEN` com o mesmo valor da API; o extrator não lê o arquivo `.env` automaticamente. Os comandos estão no README.

A cadência implementada não certifica disponibilidade contínua, publicação do RU dentro de prazo ou exibição de última atualização na interface. O modelo atual ainda não registra esse último instante.

## SAST e proteção da branch

O workflow `SAST` executa Bandit sobre o código Python do backend/extração e CodeQL sobre JavaScript/TypeScript. A política em `scripts/security/POLICY.md` no repositório define severidades, arquivos analisados e comandos locais. Relatórios e versões dos scanners devem ser consultados nos artefatos da execução, mesmo quando o check falha.

No GitHub, um administrador deve configurar os checks de SAST como obrigatórios na proteção/ruleset da `main`, depois que o workflow executar. Sem essa configuração, uma falha de check pode ser ignorada por quem tiver permissão de merge. Esta mudança não altera permissões ou regras remotas automaticamente. Consultar os nomes exatos na política do repositório.

## Testes e execução alternativa

As instruções de execução sem Docker, testes com pytest e sincronização estão no [README do repositório](https://github.com/unb-mds/2026-2-Bandejao/blob/main/README.md). Os testes da aplicação verificam backend e extração; a validação do site verifica a geração da documentação. Consulte o [estado da arquitetura](Arquitetura.md) para distinguir implementação de funcionalidades planejadas.

## Frontend fora do Docker

Com Node 22.12+ e API/banco em execução, entre em `frontend/`, copie `.env.example` para `.env`, execute `npm ci` e `npm run dev`. Acesse <http://localhost:5173>. Configure `VITE_API_BASE_URL` e autorize a origem em `CORS_ORIGINS` no backend.

O frontend usa React 19, Vite 8, TypeScript e Tailwind v4, incorporando as telas da equipe. `npm test`, `npm run lint` e `npm run build` são os checks da CI; o build inclui checagem de tipos. Campi/cardápios usam a API; os filtros operam sobre os itens carregados. Avaliações, reclamações, planejamento e lotação permanecem demonstrações locais; recarregar apaga os registros da sessão. A integração não atualiza automaticamente a publicação Vercel externa.
