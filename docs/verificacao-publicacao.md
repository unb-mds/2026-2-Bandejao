# Preparação e verificação da publicação HTTPS

**Issue:** [55](https://github.com/unb-mds/2026-2-Bandejao/issues/55). **Data:** 27/10/2026. **Estado:** publicação real pendente de ativação no Render.

## Trabalho existente e autoria

O [PR 71](https://github.com/unb-mds/2026-2-Bandejao/pull/71), aberto por Gabrieldualp, prepara frontend estático, API e PostgreSQL no Render e exposição da versão em `/version` e no rodapé. Seus três commits, atribuídos a Yue, permanecem com a autoria original. Este complemento de Arthur Pitanga acrescenta verificação reproduzível e registra o estado efetivamente observado; não recria nem reatribui a configuração da equipe.

## Resultado observado

As URLs propostas `https://bandejao-unb-g12.onrender.com` e `https://bandejao-unb-g12-api.onrender.com` retornaram HTTP 404 nesta verificação, inclusive `/health`, `/version` e consultas públicas. O [registro JSON](evidencias/dados/publicacao-https-2026-10-27.json) contém instante UTC, SHA esperado do PR e cada resultado. Um endereço terminar em `onrender.com` não comprova que o ambiente foi criado.

Não há acesso à conta Render nesta sessão. O Blueprint, os testes e o código de versão não substituem a ativação de serviços/banco, as migrações e a navegação externa exigidas por CA-RNF04-01. A issue deve permanecer aberta até essa evidência existir. O protótipo Vercel continua uma referência visual separada.

## Verificador somente leitura

Com Python, na raiz do repositório, use as URLs reais e o SHA completo que deveria estar publicado:

```powershell
python scripts/verificar_publicacao.py --frontend https://bandejao-unb-g12.onrender.com --api https://bandejao-unb-g12-api.onrender.com --commit 0142b725fb9152310693cb2106e90e713e4c5ee9 --saida publicacao-verificada.json
```

Esse SHA identifica a revisão do PR 71 inspecionada nesta entrega; depois de um novo deploy, informe o SHA efetivamente esperado em vez de reutilizar o exemplo.

A ferramenta aceita URLs HTTPS sem credenciais, consulta cinco grupos de evidência e retorna código 0 quando todos passam ou 1 quando algum falha:

| Checagem | Verificação |
|---|---|
| Interface | HTTPS e HTML com o contêiner da aplicação. Não executa JavaScript. |
| API | `/health` responde `status: ok`. |
| Versão | `/version` devolve `version` igual ao SHA completo esperado, conforme o contrato do PR 71. |
| Dados | Campi e refeições não vazios, itens presentes e vínculo válido de campus. |
| CORS | GET com origem do frontend e OPTIONS para POST com Content-Type e X-Identidade. |

São enviados apenas GET e OPTIONS; não há importação, avaliação, reclamação ou alteração de banco. Não forneça token, senha ou segredo. Falhas de conexão/certificado e formato inválido são registradas como falha, sem converter o resultado em aprovação. A saída identifica os limites da checagem. Vinte e um testes do verificador passaram e fazem parte da CI. Redirecionamentos para HTTP são recusados antes de seguir, inclusive cadeias que tentem voltar a HTTPS; erros de protocolo e timeout viram falhas sem divulgar detalhes locais.

## Ativação pelo responsável do Render

1. Concluir a revisão do PR 71 e selecionar a branch de publicação conscientemente. Para acompanhar a `main`, criar o Blueprint após a integração ou ajustar explicitamente a branch dos serviços. Se `branch` for omitida, o Render acompanha a branch do Blueprint; não presumir uma troca automática para `main`.
2. Criar os serviços e o PostgreSQL; armazenar senha e tokens nas variáveis da plataforma, sem colocá-los no Git. Aplicar migrações e conferir CORS com a origem real do frontend.
3. Fixar uma versão Python compatível com a CI. O Render pode escolher outra versão padrão conforme a criação do serviço; conferir esse valor antes de ativar.
4. O seed previsto no PR cria um almoço de exemplo de Gama na data da execução inicial. Anotar a data e selecionar essa semana/almoço na interface se a avaliação ocorrer depois. Não repetir o seed em base com dados a preservar: ele remove o campus Gama e dependências antes de recriar a massa.
5. Configurar a sincronização corrigida da issue 54 no ambiente apropriado. O Blueprint atual do PR 71 não inclui o sincronizador. Confirmar os limites do plano e manter os segredos restritos à API/rotina.
6. Executar o verificador com URLs reais/SHA esperado e guardar o JSON. Abrir a interface em navegador limpo, fora da máquina de desenvolvimento, conferir o rodapé e comparar com `/version`.
7. Consultar um campus, semana e refeição conhecidos. Validar carregamento, filtros, PDF e última importação; em massa de avaliação autorizada, enviar feedback e verificar a persistência após recarga. Separar claramente dados reais, seed e telas demonstrativas.
8. Registrar data, responsável, URLs, commit, capturas e resultado por critério antes de encerrar a issue 55. A janela de checagens a cada cinco minutos pertence a CA-RNF04-02 e requer evidência própria.

## Referências da plataforma

- [Branch dos serviços no Blueprint](https://render.com/docs/blueprint-spec#branch).
- [Versão Python](https://render.com/docs/python-version).
- [Integração com CI](https://render.com/docs/deploys#integrating-with-ci): o Render aceita `success`, `neutral` e `skipped`; não publica quando nenhum check é detectado ou quando algum falha. Essa opção não substitui o ruleset da `main`.

As referências foram consultadas em 27/10/2026; limitações e planos da hospedagem devem ser conferidos novamente na ativação.
