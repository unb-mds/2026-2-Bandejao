# Frontend Bandejão

Interface em **React 19 + Vite 8 + TypeScript + Tailwind CSS v4**, incorporada do trabalho da equipe em [marilluantunes/frontend-react](https://github.com/marilluantunes/frontend-react), revisão `c1833a3b7175765574e258c6574973b88a04c361` (27/09/2026). A estrutura de componentes, navegação, tema e recursos de acessibilidade desse frontend são a base da aplicação local. O repositório principal mantém sua configuração de API, Docker e CI.

## Como rodar

Pré-requisito: **Node 22.12+**. Com API e banco em execução, na pasta `frontend`:

```powershell
Copy-Item .env.example .env
npm ci
npm run dev
```

Em Linux/macOS, use `cp .env.example .env`. Abra <http://localhost:5173>. `VITE_API_BASE_URL` define a URL acessível pelo navegador; o padrão é `http://localhost:8000`. Configure `CORS_ORIGINS` no backend para permitir a origem do frontend. No Compose, a URL é recebida durante o build; alterá-la exige reconstruir a imagem.

## Estrutura

- `src/App.tsx`: estado das telas, carregamento dos campi/cardápios e ações do protótipo.
- `src/screens/`: Hoje, Cardápio, Avaliação e Lotação.
- `src/components/`: cabeçalho, navegação, acessibilidade e componentes das telas.
- `src/api.ts`: cliente tipado para `GET /campi/` e `GET /cardapios/`; erros HTTP e cancelamento de consultas.
- `src/cardapios.ts`: adaptação do contrato da API, datas e organização semanal, preservando todos os itens.
- `src/data.ts`: constantes visuais e exemplos de lotação; não fornece cardápios ou avaliações para a consulta.
- `src/index.css`: Tailwind v4, tokens do tema e estilos de acessibilidade. O plugin está em `vite.config.ts`.

## Integração e limites

| Fluxo | Estado |
|---|---|
| Campus e cardápio | Consulta a API. A semana inicial é a atual, de domingo a sábado; é possível escolher outra semana. Os dias e refeições são selecionados na interface. |
| Origem e indisponibilidade | Link para o PDF, carregamento, erro com nova tentativa e mensagens sem inferir fechamento do RU. |
| Dieta e alérgenos | Filtros locais sobre os itens retornados, usando `tipo_dieta` e os marcadores `contem_*`. A seleção ovolactovegetariana e a estrita correspondem literalmente aos tipos publicados; D02 continua pendente de validação do produto. |
| Avaliações e reclamações | Telas do protótipo; registros somente no estado do React, perdidos ao recarregar. Não são enviados à API nem ao RU. A API de avaliação existente ainda precisa de adaptação ao formulário. |
| Planejamento | Demonstração por campus e data, apenas nesta sessão; sem persistência ou previsão. |
| Lotação | Exemplos visuais e relatos desta sessão; sem consulta a dados reais nem estimativa operacional. |

A convenção de domingo a sábado é uma escolha de apresentação da integração, não uma resolução de D01. O backend não informa horário de funcionamento nem instante de atualização/importação. A tela Hoje escolhe a refeição por faixas horárias do protótipo, sem afirmar que o restaurante está aberto.

Os filtros usam apenas as marcações recebidas; não inferem ingredientes pelo nome. A ausência de marcação não comprova ausência de ingrediente. A legenda dos PDFs validada em 30/09/2026 não tem símbolo separado para frutos do mar. Confira a fonte oficial. D01/D02 e os critérios de aceitação permanecem em [Requisitos](../docs/Requisitos.md).

## Verificação local

```bash
npm test
npm run lint
npm run typecheck
npm run build
```

`npm test` usa `tsx` e o runner do Node para testar o cliente e a adaptação do contrato. `npm run build` verifica tipos antes de compilar com Vite. A CI mantém instalação por `npm ci`, testes, lint e build. Esses checks não substituem validação com banco/API reais, revisão visual ou aceite do produto. A migração local não publica nem altera o protótipo Vercel externo.
