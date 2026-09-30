# Sprint 02 — Núcleo Funcional

**Objetivo da sprint:** sair da estruturação (Sprint 01) para um sistema com dados reais fluindo: extração do cardápio, API consumindo o banco e definição do produto para as telas.

Além do que estava planejado, a sprint incluiu a reformulação dos requisitos e a etapa de produto (story map, personas e protótipo).

## O que foi feito

### Dados e extração
- Extração do cardápio implementada em Python (`requests`, `BeautifulSoup`, `pdfplumber`), substituindo o esqueleto da Sprint 01
- Localização dinâmica do PDF de cada campus na página do RU (o link muda toda semana)
- Extração de categoria, tipo de dieta e alérgenos, com tratamento independente por campus: a falha em um campus não interrompe os demais
- Rotina de sincronização (`extracao/sincronizar.py`) que envia os cardápios extraídos ao backend, com opção de execução periódica
- Testes automatizados da extração e da sincronização

### Banco de dados
- Nova migração adicionando o alérgeno amendoim (`contem_amendoim`) em `item_cardapio`, pois o ícone aparece nos PDFs do RU
- Script de seed com dados de exemplo, permitindo testar backend e frontend sem depender da extração real
- Documento `docs/handoff_banco_e_importacao.md` registrando a migração pendente e o contrato de importação

### Backend
- Schemas Pydantic criados para as entidades
- Rotas de campus, cardápio e avaliação implementadas
- Testes automatizados da API, do seed e da sessão de banco

### Requisitos (reformulação)
- Motivo: incerteza sobre a adesão dos usuários ao check-in no momento da refeição
- **RF06 e RF07 reescritos:** o check-in deu lugar ao planejamento semanal, em que o usuário marca, ao ver o cardápio da semana, os dias e refeições em que pretende ir ao RU; a estimativa de horário de pico passa a usar o volume de planejamentos
- **RF08 adicionado:** registro de reclamações sobre a refeição, separado da avaliação por nota
- Requisitos não funcionais revisados

### Produto (Figma)
- **Story map** com épicos, funcionalidades e histórias de usuário no formato "Eu quero… para…"
- **Personas** (aluna e servidor) conectadas às necessidades dos requisitos
- **DoR e DoD** (Definition of Ready e Definition of Done) definidos
- **Protótipo das telas do frontend** (seleção de campus, cardápio com filtros e avaliação)

### Documentação e gestão
- Documento de visão (`docs/documento_de_visao.md`)
- README atualizado: seed, sincronização do cardápio real, link do Figma e escopo com reclamações e planejamento semanal
- Roteiro de apresentação da Release 1
- Reorganização da divisão de papéis do grupo

## Planejado × entregue

| Item planejado | Situação |
|---|---|
| Script de seed | ✅ Concluído |
| Extração real do cardápio | ✅ Implementada; validação contra os PDFs atuais dos 5 campi ainda pendente |
| Schemas Pydantic | ✅ Concluído |
| Endpoints de campus, cardápio e avaliação | ✅ Concluído, com testes |
| Telas do frontend | 🔲 Protótipo pronto no Figma; implementação em React pendente |

## Pendências e próximos passos

- Validar a extração contra os PDFs reais de todos os campi e rodar a sincronização com o backend
- Implementar as telas do frontend a partir do protótipo e integrá-las à API
- Adequar o backend e o modelo de dados à mudança dos requisitos: entidade de planejamento semanal (no lugar de check-in) e reclamações
- Configurar pipeline de CI (GitHub Actions) e definir a estratégia de deploy
- Criar as Release Notes da Release 1
- Conferir o status do README a cada mudança de sprint (atualmente indica Sprint 02)

## Atualização da GitHub Page — 30/09/2026

- Navegação ampliada para todos os estudos, protótipos, execução local e manutenção da documentação.
- Página inicial com roteiro de consulta dos documentos para avaliação da Release 1, distinguindo escopo planejado de implementação.
- Endereço do clone corrigido no README e URL canônica do site configurada.
- Build estrito em pull requests e deploy por artefato na `main`, sem commits automáticos de publicação.
- Dependências principais do site fixadas e mudanças registradas em [Histórico](../changelog.md).
- Configuração necessária no repositório: **Settings → Pages → Source → GitHub Actions**; acompanhar o workflow e conferir a URL após a publicação.

Esta atualização cobre a GH Page. Não altera requisitos, regras de negócio ou código da aplicação e não constitui ata de reunião.
