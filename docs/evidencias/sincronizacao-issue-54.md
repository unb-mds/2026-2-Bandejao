# Validação da sincronização da issue 54

**Data:** 27/10/2026. **Base:** `299d9f4`. **Responsável pela entrega:** Arthur Pitanga (`pithzin`).

## Problema reproduzido

Na publicação oficial de 26/10 a 01/11, quatro arquivos tinham revisão numérica (`-1` ou `-2`) antes de `.pdf`; a descoberta só reconhecia Fazenda Água Limpa. O PDF reconhecido continha ícones JPEG e encerrava a extração com `ValueError: not enough image data`. `run()` não isolava essa exceção.

Os testes de regressão foram executados antes da correção: cinco falharam e dois passaram. As falhas reproduziam as revisões de nome, a decodificação JPEG e a interrupção dos demais campi.

## Correções

- A regex aceita sufixos numéricos e mantém suporte aos nomes anteriores.
- Streams JPEG são decodificados pelo Pillow antes da conversão para RGB; streams RGB crus continuam no caminho anterior.
- Exceções inesperadas de um PDF tornam-se falha daquele campus; `KeyboardInterrupt` e `SystemExit` não são engolidos.
- Importações bem-sucedidas registram JSON com campus, URL do PDF, instante UTC e instante devolvido pela API, sem registrar o token.
- O serviço opcional do Compose mantém execução imediata e repetição a cada 21.600 segundos, com autenticação por variável de ambiente e sem sobrepor ciclos.
- O workflow `Sincronizar cardápios` agenda execuções únicas a cada seis horas, usa variável/secret do GitHub e preserva logs e metadados por 30 dias.

## Fonte real

Os cinco PDFs foram baixados da [página oficial](https://ru.unb.br/cardapio-refeitorio/), processados individualmente e convertidos ao contrato de importação:

| Campus | Refeições | Itens | Fonte |
|---|---:|---:|---|
| Darcy Ribeiro | 21 | 191 | [PDF](https://ru.unb.br/wp-content/uploads/2026/10/Darcy-Ribeiro-Semana-02-26-10-a-01-11-2.pdf) |
| Ceilândia | 17 | 154 | [PDF](https://ru.unb.br/wp-content/uploads/2026/10/Ceilandia-Semana-02-26-10-a-01-11-1.pdf) |
| Gama | 15 | 138 | [PDF](https://ru.unb.br/wp-content/uploads/2026/10/Gama-Semana-02-26-10-a-01-11-1.pdf) |
| Planaltina | 21 | 191 | [PDF](https://ru.unb.br/wp-content/uploads/2026/10/Planaltina-Semana-02-26-10-a-01-11-1.pdf) |
| Fazenda Água Limpa | 10 | 83 | [PDF](https://ru.unb.br/wp-content/uploads/2026/10/Fazenda-Semana-02-26-10-a-01-11.pdf) |
| Total | 84 | 757 | Cinco campi |

As datas abrangem 26/10 a 01/11 conforme cada publicação; nenhum dia/refeição ausente foi inventado. Os hashes SHA-256, URLs, tamanhos, datas e contagens estão no [registro JSON](dados/sincronizacao-2026-10-27.json). Os cinco PDFs, os links observados e a saída esperada foram versionados em `extracao/tests/fixtures/publicacao-2026-10-27/` e são reprocessados sem rede na regressão. A linha de base não substitui auditoria nutricional de cada marcador.

## Isolamento e reimportação

Com os PDFs reais desta publicação em cache, foi introduzida uma falha de decoder apenas em Gama. Os outros quatro campi concluíram a extração. Essa execução complementa o teste sintético; a fonte original não foi modificada.

Os payloads reais dos cinco campi foram enviados duas vezes à API por `TestClient`, com SQLite isolado em memória e relógio controlado. Resultado: cinco campi, 84 refeições, 757 itens e os mesmos IDs de refeições após a segunda passagem. Cinco avaliações e cinco reclamações criadas entre as passagens foram preservadas. Nenhuma base operacional foi alterada. Esse ensaio não comprova comportamento específico de PostgreSQL ou migrações em produção.

## Verificação local

- Extração: 54 testes, 100% de cobertura, Ruff aprovado.
- Backend: 94 testes, 100% de cobertura, Ruff aprovado; teste de reimportação ampliado para preservar avaliações e reclamações após duas passagens.
- Agendamento: testes de relógio simulado conferem 21.600 segundos entre inícios, repetição após falha, execução única e ciclos sem sobreposição. Não foi necessário aguardar seis horas.

## Agendamento pelo GitHub Actions

O arquivo `.github/workflows/sincronizacao.yml` usa o cron `23 */6 * * *`, equivalente a quatro tentativas por dia em UTC. Também permite execução manual. Cada disparo executa o extrator uma única vez; a próxima periodicidade pertence ao agendador, evitando um processo ocioso por seis horas. O grupo de concorrência não cancela nem sobrepõe ciclos.

A URL da API vem da variável `BACKEND_URL` e precisa começar por `https://`. O token vem exclusivamente do secret `IMPORTACAO_TOKEN`. Configuração ausente encerra o job antes do acesso ao RU. O job guarda `inicio_utc`, `fim_utc`, ID, commit, código de saída e o log por campus em um artefato de 30 dias. O conteúdo não inclui o valor do token.

Em pull requests, o workflow não importa dados: executa somente os testes do sincronizador e a regressão dos cinco PDFs reais. Disparos agendados só passam a existir quando o arquivo estiver na branch padrão.

## Operação e limites

O Docker Compose continua como alternativa para host próprio, conforme [Desenvolvimento](../desenvolvimento.md). O GitHub Actions remove a necessidade de manter esse host ligado, mas ainda depende de uma API publicada e do mesmo segredo configurado nas duas pontas.

Não há API pública ativa nem `BACKEND_URL`/`IMPORTACAO_TOKEN` configurados no repositório nesta entrega, portanto nenhuma importação operacional foi disparada. Após a publicação, a primeira execução manual deve ser verificada antes de confiar no cron. Eventos `schedule` podem atrasar ou ser descartados sob carga, conforme a [documentação oficial do GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule); não representam garantia de horário exato. O aceite integral de RNF02 exige guardar execuções bem-sucedidas dentro da janela de 24 horas.
