# Frontend Bandejão

Interface em React 19 e Vite 8 para consultar os cardápios que a API já tem cadastrados. A tela carrega campi e refeições da API, permite filtrar por período e tipo de refeição e apresenta a origem do PDF.

## Como rodar

Pré-requisito: **Node 22+** (npm incluso). Com a API e o banco em execução, configure o endereço da API:

```powershell
Copy-Item .env.example .env
npm ci
npm run dev
```

Em Linux/macOS, use `cp .env.example .env`. Abra <http://localhost:5173>. A variável `VITE_API_BASE_URL` define a URL usada pelo navegador; o padrão local é `http://localhost:8000`. Para Docker Compose, ajuste `VITE_API_BASE_URL` no `.env` da raiz antes de executar o build.

O endpoint de campi retorna apenas os campi já registrados por importação ou seed. Os filtros de dieta/alérgenos ficam fora da interface enquanto as decisões de produto e a cobertura dos dados não forem validadas. Avaliações, reclamações e planejamento ainda não estão integrados.

## Verificação

```bash
npm test
npm run lint
npm run build
```
