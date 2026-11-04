# Publicação da aplicação

## Ambiente de avaliação

O Blueprint `render.yaml` descreve uma implantação completa no Render:

- **interface:** <https://bandejao-unb-g12.onrender.com>;
- **API:** <https://bandejao-unb-g12-api.onrender.com>;
- **versão da API:** <https://bandejao-unb-g12-api.onrender.com/version>;
- **documentação OpenAPI:** <https://bandejao-unb-g12-api.onrender.com/docs>.

O acesso público não exige conta. O rodapé da interface mostra os 12 primeiros caracteres do commit publicado, enquanto `/version` devolve o SHA completo. As URLs `onrender.com` usam HTTPS administrado pela plataforma.

## O que a versão demonstra

| Classificação | Conteúdo |
|---|---|
| Função integrada | Consulta de campi e cardápios, filtros alimentares, fonte e última importação, avaliações e reclamações usam a API e o PostgreSQL. |
| Dados de exemplo | Na primeira implantação, o gancho inicial executa `python -m app.db.seed` e cria uma refeição do campus Gama para permitir a navegação. Esses registros não representam o cardápio atual do RU. |
| Demonstração de interface | Planejamento e lotação continuam identificados na tela como demonstrações ou exemplos, sem estimativa operacional persistida. |
| Protótipo externo | A antiga publicação Vercel é uma referência visual separada e não comprova a integração desta versão. |

A rotina de sincronização real não faz parte deste Blueprint. A importação permanece protegida por token e pode substituir os dados de exemplo quando for operada em um ambiente autorizado.

## Componentes e segredos

O Blueprint cria um site estático, um serviço web FastAPI e um PostgreSQL 16. A URL interna do banco é injetada em `DATABASE_URL`; a aplicação seleciona o driver `psycopg`. A URL pública do site alimenta `FRONTEND_URL` para o CORS, e a URL da API alimenta `VITE_API_BASE_URL` durante o build do frontend.

`IMPORTACAO_TOKEN` e `EQUIPE_TOKEN` usam `generateValue: true`. A senha do banco é administrada pelo Render e chega ao backend pela referência `fromDatabase`. Nenhum desses valores é registrado no Git. Variáveis `VITE_*` ficam no JavaScript entregue ao navegador e, portanto, nunca devem receber segredos.

## Criar ou reconstruir o ambiente

1. No painel do Render, escolha **New → Blueprint** e conecte o repositório `unb-mds/2026-2-Bandejao`.
2. Selecione a branch que contém `render.yaml` e confirme os três recursos propostos.
3. Aguarde a API responder em `/health` e a implantação inicial terminar. As migrações Alembic são aplicadas antes de iniciar o servidor, e o seed de exemplo roda uma vez após o primeiro deploy bem-sucedido.
4. Abra a interface em uma sessão anônima, consulte o campus Gama e compare a versão do rodapé com `/version`.

Depois da integração na `main`, `autoDeployTrigger: checksPass` só inicia uma nova publicação quando os checks do commit terminam com sucesso.

## Limites do plano de avaliação

O plano gratuito pode suspender a API após inatividade, causando demora na primeira abertura. O PostgreSQL gratuito expira 30 dias após a criação, conforme a [documentação do Render](https://render.com/docs/your-first-deploy). Antes da avaliação, a equipe deve confirmar a data de expiração e aquecer o serviço; a checagem periódica de CA-RNF04-02 deve ser registrada separadamente durante a janela acordada.

O endpoint `/health` confirma que o processo da API está ativo. Ele não substitui a consulta de um cardápio nem comprova, sozinho, a persistência no banco.
