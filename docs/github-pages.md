# GitHub Pages: publicação e manutenção

## Objetivo e endereço

A página reúne os documentos para avaliação e acompanhamento do Bandejão: visão, requisitos, arquitetura C4, dados, protótipos, sprints e instruções de execução.

Endereço previsto: <https://unb-mds.github.io/2026-2-Bandejao/>. A publicação depende da configuração abaixo e de uma execução bem-sucedida do workflow.

## Configuração inicial no GitHub

Uma pessoa com permissão de administração/manutenção deve abrir **Settings → Pages → Build and deployment → Source** e selecionar **GitHub Actions**. Se estiver configurado `gh-pages`, mudar a origem para GitHub Actions: esta versão publica o artefato diretamente e não cria commits de deploy.

Após integrar as mudanças na `main`, acompanhar **Actions → Validar e publicar documentação**. Também é possível executar **Run workflow** selecionando `main`. A etapa `deploy` deve terminar com sucesso e informar a URL publicada. Confirmar a página em um navegador, incluindo navegação, busca, links e diagramas C4.

## Validação e prévia local

Requer Python 3.12. Na raiz do repositório:

```bash
python -m venv .venv
```

Ative o ambiente no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Ou no Linux/macOS:

```bash
source .venv/bin/activate
```

Instale e valide:

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
python -m mkdocs serve
```

A prévia abre em <http://127.0.0.1:8000>. Se a API já usar essa porta, execute `python -m mkdocs serve -a 127.0.0.1:8001`. O diretório `site/` é gerado e ignorado pelo Git.

## Funcionamento do workflow

- Pull requests que alteram documentação, configuração ou dependências executam o build estrito, sem publicar.
- Pushes correspondentes na `main` e execução manual na `main` geram e publicam o site.
- O deploy depende do build aprovado; avisos do MkDocs impedem a publicação.
- O build tem leitura do repositório. Somente o deploy recebe `pages: write` e `id-token: write`.
- Uma fila de deploy evita publicações simultâneas.

## Atualizar e preservar rastreabilidade

Edite os arquivos em `docs/`, inclua páginas novas em `mkdocs.yml`, valide o build e registre mudanças em [Histórico de mudanças](changelog.md) e na sprint pertinente. Requisitos, arquitetura e protótipos continuam sob revisão dos respectivos responsáveis. Registre atas somente quando houver reunião real, com data, participantes, decisões e vínculos para issues; não preencha reuniões retroativamente sem evidência.

## Limites da validação

O build verifica geração e referências locais do Markdown. Ele não testa disponibilidade de links externos, comportamento da API nem execução de diagramas Mermaid no navegador. A avaliação visual e o acesso público precisam ser conferidos após o deploy. Se `configure-pages` falhar, confira a origem de publicação e as permissões do repositório.

## Referências

- [Workflow oficial do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- [Configurar origem de publicação](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- [Comandos e modo estrito do MkDocs](https://www.mkdocs.org/user-guide/cli/).
