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
- `src/api.ts`: cliente tipado para campi, cardápios e avaliações; erros HTTP, validações da API e cancelamento de consultas.
- `src/avaliacoes.ts`: ordenação e apresentação do histórico persistido no fuso de Brasília.
- `src/cardapios.ts`: adaptação do contrato da API, datas e organização semanal, preservando todos os itens.
- `src/data.ts`: constantes visuais e exemplos de lotação; não fornece cardápios ou avaliações para a consulta.
- `src/index.css`: Tailwind v4, tokens do tema e estilos de acessibilidade. O plugin está em `vite.config.ts`.

## Integração e limites

| Fluxo | Estado |
|---|---|
| Campus e cardápio | Consulta a API. A semana inicial é a atual, de domingo a sábado; é possível escolher outra semana. Os dias e refeições são selecionados na interface. |
| Origem e indisponibilidade | Link para o PDF, data/hora da última importação bem-sucedida do campus, carregamento, erro com nova tentativa e mensagens sem inferir fechamento do RU. |
| Dieta e alérgenos | Filtros locais sobre os itens retornados, usando `tipo_dieta` e os marcadores `contem_*`. O filtro ovolactovegetariano inclui também itens vegetarianos estritos; as demais classes permanecem exatas, conforme D02. |
| Avaliações | Nota geral e comentário são enviados à API com a identidade anônima do navegador. O histórico consulta somente a refeição selecionada, mostra data/hora em Brasília e permanece após recarregar a página. |
| Reclamações | A tela envia categoria e descrição à API com identidade anônima. Há confirmação de sucesso/erro; não existe lista pública nem encaminhamento automático ao RU. |
| Planejamento | Demonstração por campus e data, apenas nesta sessão; sem persistência ou previsão. |
| Lotação | Exemplos visuais e relatos desta sessão; sem consulta a dados reais nem estimativa operacional. |

A convenção de domingo a sábado é uma escolha de apresentação da integração, não uma resolução de D01. O backend informa a última importação bem-sucedida, mas não o horário de funcionamento. A tela Hoje escolhe a refeição por faixas horárias do protótipo, sem afirmar que o restaurante está aberto.

Os filtros usam apenas as marcações recebidas; não inferem ingredientes pelo nome. “Sem marcação” significa “não marcado na fonte”, não “livre de”. A legenda dos PDFs validada em 30/09/2026 não tem símbolo separado para frutos do mar. Confira a fonte oficial e os critérios de aceitação em [Requisitos](../docs/Requisitos.md).

## Aviso de privacidade

Na primeira visita, um diálogo explica o código anônimo salvo no navegador, a persistência de avaliações e reclamações na API e o cuidado com dados pessoais em textos livres. **Entendi** registra a leitura na chave versionada `bandejao.privacidade.v1`; não representa consentimento para coleta. Sem armazenamento local, a confirmação vale nesta página e o aviso pode reaparecer ao recarregar. **Escape** fecha sem registrar a leitura. O botão **Privacidade**, no rodapé, permite reler o conteúdo.

Limpar os dados do site e reabrir a página faz o próximo envio gerar outro código, sem apagar registros já enviados ao backend. O texto integral e os limites estão em [Aviso de privacidade](../docs/privacidade.md). A lógica de armazenamento está em `src/privacidade.ts` e o diálogo acessível em `src/components/AvisoPrivacidade.tsx`.

## Verificação local

```bash
npm test
npm run lint
npm run typecheck
npm run build
```

`npm test` usa `tsx` e o runner do Node para testar o cliente e a adaptação do contrato. `npm run build` verifica tipos antes de compilar com Vite. A CI mantém instalação por `npm ci`, testes, lint e build. Esses checks não substituem validação com banco/API reais, revisão visual ou aceite do produto. A migração local não publica nem altera o protótipo Vercel externo.
