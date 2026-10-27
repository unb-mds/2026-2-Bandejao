# Plano de execução das issues abertas do Bandejão

**Objetivo:** corrigir #54, implementar #53 e concluir a preparação verificável de #55, preservando autoria e evidências.

**Base:** main 299d9f4. **Tecnologias:** FastAPI, PostgreSQL, extrator Python, React 19, Vite 8, TypeScript e Tailwind v4.

## Restrições

- Um commit de Arthur Pitanga, e-mail GitHub 240395397+pithzin@users.noreply.github.com, por issue trabalhada.
- Preservar os commits da equipe e os componentes existentes. O PR #71 já contém preparação de HTTPS de Gabrieldualp e não será reatribuído.
- Não registrar segredos em arquivos, logs ou relatórios.
- Validar a extração com os cinco PDFs oficiais atuais e registrar hashes, contagens, datas e fontes.
- Nenhuma gravação em banco real durante testes; reimportação usa banco descartável e verifica avaliações/reclamações.
- A #55 depende de acesso à hospedagem, indisponível nesta sessão. Configuração e CI não comprovam publicação HTTPS.
- O ruleset ativo da main exige SAST aprovado. A integração respeitará os checks, sem bypass.

## Issue 54

- [x] Criar testes de regressão em extracao/tests/test_regressoes_publicacao.py para nomes com revisão numérica, imagem JPEG e erro inesperado isolado por campus.
- [x] Confirmar falhas antes da correção com pytest.
- [x] Corrigir PADRAO_PERIODO, _imagem_do_stream e a fronteira de erro de run em extracao/extracao/main.py.
- [x] Registrar campus, fonte e horário em cada resultado da sincronização, sem imprimir exceções com credenciais.
- [x] Validar idempotência e preservação de avaliações/reclamações pelo contrato existente e por integração descartável.
- [x] Executar pytest/Ruff, extração real e documentação; registrar evidência em docs/evidencias/sincronizacao-issue-54.md.
- [x] Commit fix: corrige sincronizacao dos PDFs oficiais do RU (#54).

## Issue 53

- [x] Aviso acessível na primeira visita, confirmação versionada no armazenamento e releitura no rodapé.
- [x] Texto preciso sobre identificador, avaliações, comentários e reclamações; limpeza do navegador cria outra identidade. Sem alegação de anonimato absoluto ou certificação legal.
- [x] Testes de persistência, falha de armazenamento e comportamento no navegador.
- [x] Documentar texto em docs/privacidade.md e incluir no MkDocs.
- [x] Commit feat: apresenta aviso de privacidade e releitura (#53).

## Issue 55

- [x] Revisar PR #71, requisitos da plataforma e disponibilidade das URLs propostas.
- [x] Preparar contribuição complementar verificável sem reescrever autoria da equipe.
- [x] Registrar o procedimento de validação HTTPS, versão, dados conhecidos e limites da hospedagem.
- [x] Commit específico #55 com melhorias e evidência exata do que está pronto e do que depende do Render.
- [x] Manter aceite de publicação pendente enquanto não houver ambiente real acessível.

## Entrega

- [x] SAST e suítes no GitHub após a revisão local aprovada.
- [x] Publicar os commits com a conta pithzin, vinculando as issues e respeitando a proteção da main.
- [x] Gerar documento completo com antes/depois, arquivos, commits, execução, critérios e limitações reais.

## Registro da execução local

- Issue 54: commit `00d8fcc`; 54 testes de extração e 94 de backend, ambos com 100% de cobertura. PDFs versionados e dados reais reimportados em banco descartável. Execução contínua no host permanece pendente.
- Issue 53: commit `6a22a51`; 27 testes do frontend, lint/build e validação de diálogo/armazenamento no Chrome desktop/mobile aprovados.
- Issue 55: verificador somente leitura e roteiro de ativação preparados; 21 testes aprovados. As URLs propostas deram 404. Sem acesso Render, a publicação não pode ser declarada concluída.
- Revisão local independente: sem achados críticos/importantes pendentes após correções de redirecionamento HTTPS e erros de protocolo no verificador.

O relatório final identifica o resultado remoto e a situação das issues. Itens de ativação não serão marcados como aceitos apenas por compilação/configuração.

## Publicação no repositório

O [PR 72](https://github.com/unb-mds/2026-2-Bandejao/pull/72) integrou os três commits na `main` em `b38cba0`: `00d8fcc` (#54), `6a22a51` (#53) e `0407165` (#55), com autoria e committer de Arthur Pitanga e associação à conta `pithzin`. CI da aplicação, SAST e documentação foram aprovados nesse commit de integração. A issue 53 foi encerrada; 54 e 55 permanecem abertas para as evidências operacionais descritas acima.

O relatório da entrega foi disponibilizado em Markdown e PDF. Uma revisão posterior de consistência alinhou README, contexto, arquitetura, requisitos, desenvolvimento, visão e protótipos ao código integrado e identificou os registros antigos das sprints como históricos.
