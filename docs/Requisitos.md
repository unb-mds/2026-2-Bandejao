# Documento de Requisitos — Bandejão

**Versão:** 1.1 — proposta de revisão em 28/09/2026

**Situação:** em revisão pela equipe. Janela de avaliação e separação das notas por campus/data/refeição acordadas com o responsável pelos requisitos nesta revisão; demais propostas ainda não homologadas.

## 1. Objetivo e origem

Especificar o comportamento esperado do Bandejão, suas regras de negócio e critérios verificáveis, em resposta à pré-avaliação da professora.

Fontes: [documento de visão](documento_de_visao.md), requisitos v1.0, [Sprint 02](scrum/sprint02.md) e [contrato de importação](handoff_banco_e_importacao.md). O código foi consultado para identificar lacunas, não para considerar funcionalidades automaticamente aceitas. Esta revisão não inclui novas entrevistas nem validação do Figma.

**Release acadêmica e prioridade do produto são diferentes:** a Release 1 avalia definição e organização; a Release 2 avalia implementação. As antigas divisões por release passam a ser chamadas de **núcleo** (RF01–RF05 e RF08) e **evolução** (RF06–RF07), preservando a prioridade. O compromisso de implementação depende do planejamento da equipe.

Os IDs RF01–RF08 e RNF01–RNF05 foram preservados. RN identifica regra de negócio; CA identifica critério de aceitação. Os critérios são expectativas, não testes já executados. Decisões novas ou incompletas estão na seção 7.

## 2. Vocabulário e limites

| Termo | Significado |
|---|---|
| Campus | Darcy Ribeiro, Ceilândia, Gama, Planaltina ou Fazenda Água Limpa. |
| Refeição | Oferta identificada por campus + data + tipo (café da manhã, almoço ou jantar), não um prato isolado. |
| Item | Preparação ou alimento de uma refeição, com categoria, dieta e marcações da fonte. |
| Semana | Segunda-feira a domingo que contém a data selecionada; convenção proposta em D01. |
| Avaliação | Nota da refeição, com comentário opcional. |
| Reclamação | Relato sobre uma refeição, independente de nota. |
| Planejamento | Intenção de comparecer; não confirma presença nem representa reserva. |
| Estimativa de movimento | Agregação de intenções; não mede fila real nem tempo de espera. |

Não estão incluídos reserva, pagamento, controle de acesso ao RU ou garantia de resposta institucional às reclamações. O check-in foi substituído por planejamento na Sprint 02 e não é pré-condição para avaliar.

## 3. Requisitos funcionais

### RF01 — Exibir o cardápio semanal

**Requisito:** O sistema deve exibir o cardápio semanal do campus selecionado, organizado por data e tipo de refeição, com seus itens.

**Prioridade:** núcleo. **Regras:** RN01, RN02. **Dependência:** dados importados do RU.

- **CA-RF01-01:** Dado um campus com cardápio disponível, quando uma semana for consultada, então serão exibidas somente suas refeições naquele intervalo, com data, tipo, categoria e nome dos itens correspondentes à fonte importada.
- **CA-RF01-02:** Dada uma semana sem dados, quando for consultada, então o sistema informará a indisponibilidade, sem apresentar outra semana como atual nem afirmar que o RU está fechado.
- **CA-RF01-03:** Dado um cardápio com origem registrada, quando for exibido, então o usuário poderá consultar o link da fonte e a data/hora da última importação bem-sucedida. Uma falha de atualização não alterará essa data.

### RF02 — Selecionar o campus

**Requisito:** O sistema deve permitir selecionar o campus para consultar seu cardápio.

**Prioridade:** núcleo. **Regras:** RN01, RN02. **Dependência:** RF01.

- **CA-RF02-01:** Dada a seleção de campus, quando as opções forem abertas, então os cinco campi estarão disponíveis, inclusive os temporariamente sem cardápio.
- **CA-RF02-02:** Dada uma semana selecionada, quando o campus for alterado, então o nome do campus ativo e as refeições serão atualizados, preservando a semana e sem misturar dados dos campi.
- **CA-RF02-03:** Dado um campus sem dados, quando selecionado, então o sistema manterá a seleção e informará a indisponibilidade, permitindo escolher outro campus.

### RF03 — Filtrar itens por dieta e restrições alimentares

**Requisito:** O sistema deve permitir filtrar os itens por tipo de dieta e excluir os itens marcados com as restrições alimentares selecionadas.

**Prioridade:** núcleo. **Regras:** RN03, RN04. **Dependências:** RF01, RF02. **Decisão pendente:** D02.

- **CA-RF03-01:** Dados itens de dietas diferentes, quando uma dieta for selecionada, então serão exibidos apenas itens dessa classificação, conforme RN03, mantendo a identificação da refeição.
- **CA-RF03-02:** Dados itens marcados com leite, soja ou ambos, quando leite e soja forem excluídos, então nenhum item com qualquer uma dessas marcações será exibido. Com dieta e restrições selecionadas, cada item deverá atender a todos os filtros.
- **CA-RF03-03:** Dada uma refeição sem itens após a filtragem, quando o resultado for exibido, então será informado que nenhum item corresponde aos filtros. Ao limpar os filtros, todos os itens da consulta original voltarão a aparecer.
- **CA-RF03-04:** Dado um resultado filtrado, quando exibido, então ficará explícito que o filtro usa as marcações publicadas pelo RU e não certifica ausência de ingredientes ou contaminação cruzada. Informação desconhecida não será apresentada como ausência confirmada.

### RF04 — Registrar uma avaliação de refeição

**Requisito:** O sistema deve permitir registrar uma nota para uma refeição do dia, a partir do início do serviço até antes de 00h do dia seguinte no horário de Brasília, com comentário opcional.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN06. **Dependência:** RF01. **Decisões pendentes:** D03, D04.

- **CA-RF04-01:** Dada uma refeição elegível pela RN05, quando uma nota inteira de 1 a 5 for enviada, com comentário ausente ou de até 500 caracteres, então a avaliação será persistida e confirmada, vinculada à refeição e ao instante do envio.
- **CA-RF04-02:** Dada uma nota ausente, fracionária ou fora de 1 a 5, ou comentário acima de 500 caracteres, quando houver envio, então o sistema informará o campo inválido e não gravará a avaliação.
- **CA-RF04-03:** Dada uma refeição inexistente ou tentativa anterior ao início do serviço ou a partir de 00h do dia seguinte, quando houver envio, então o sistema recusará a avaliação e explicará o motivo. Verificar os limites: antes do início (recusar), no início (permitir), antes de 00h (permitir) e exatamente às 00h do dia seguinte (recusar), no fuso `America/Sao_Paulo`. Não será exigido check-in ou planejamento prévio; a janela não comprova consumo da refeição.

### RF05 — Consultar o histórico de avaliações

**Requisito:** O sistema deve permitir consultar o histórico de avaliações vinculadas a uma refeição.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN06, RN07. **Dependência:** RF04.

- **CA-RF05-01:** Dada uma refeição com avaliações, quando seu histórico for consultado, então serão exibidos nota, comentário quando existente e data/hora do registro, do mais recente ao mais antigo, sem avaliações de outras refeições.
- **CA-RF05-02:** Dada uma refeição sem avaliações, quando consultada, então será informada a ausência de avaliações, sem notas ou médias fictícias.
- **CA-RF05-03:** Dada uma avaliação registrada, quando a página for recarregada, o prazo de avaliação terminar ou a fonte da mesma refeição for reimportada, então a avaliação continuará disponível no histórico e vinculada à mesma refeição.
- **CA-RF05-04:** Dados os mesmos pratos ofertados em outra data ou campus, quando o histórico da nova refeição for consultado, então não serão reutilizadas as avaliações anteriores. Sem avaliações próprias, será exibido “sem avaliações”, conforme CA-RF05-02. Uma eventual média deve considerar apenas notas da mesma combinação campus + data + tipo de refeição; média histórica por prato fica fora deste escopo.

### RF06 — Registrar o planejamento de refeições

**Requisito:** O sistema deve permitir marcar e desmarcar as refeições futuras em que o usuário pretende comparecer ao RU.

**Prioridade:** evolução. **Regras:** RN01, RN07, RN08. **Dependências:** RF01, RF02. **Decisões pendentes:** D03, D04, D05.

- **CA-RF06-01:** Dada uma refeição futura disponível, quando marcada, então a intenção será salva com campus, data e tipo, reaparecendo ao reabrir o planejamento com a mesma identidade definida em D04.
- **CA-RF06-02:** Dada uma intenção já registrada, quando a mesma marcação for reenviada pela mesma identidade, então continuará existindo apenas uma intenção ativa para aquela refeição.
- **CA-RF06-03:** Dada uma intenção ativa, quando desmarcada, então deixará de compor as contagens. Tentativas de marcar uma refeição cujo início seja menor ou igual ao instante da tentativa serão recusadas. Verificar tentativas antes, no instante exato e depois do início, conforme os horários a validar em D03.

### RF07 — Estimar o período de maior movimento

**Requisito:** O sistema deve apresentar uma estimativa de maior movimento por campus, data e refeição com base nas intenções registradas.

**Prioridade:** evolução. **Regras:** RN08, RN09. **Dependência:** RF06. **Decisão bloqueante:** D05.

**Lacuna:** a v1.0 prometia estimar um horário, mas RF06 coleta apenas dia e refeição. Isso permite comparar demanda entre refeições, mas não horários dentro de uma delas. A equipe precisa escolher entre coletar faixa de chegada em RF06 ou limitar RF07 à demanda por refeição. A alteração de “horário” para “período” é uma proposta sujeita a D05.

- **CA-RF07-01:** Dado um conjunto controlado de intenções ativas, quando calculada a estimativa, então a contagem corresponderá às intenções do campus, data e refeição selecionados, excluindo cancelamentos e duplicações da mesma identidade.
- **CA-RF07-02:** Dado um total inferior à amostra mínima definida em D05, quando consultado, então o sistema informará dados insuficientes, sem afirmar um pico. O limiar e seus testes de limite precisam ser registrados antes da implementação.
- **CA-RF07-03:** Dada uma amostra suficiente, quando exibido o resultado, então serão apresentados contagem, período comparado e instante do cálculo, identificando-o como estimativa de intenções. Empates mostrarão todos os períodos empatados. Horários só serão apresentados se faixas de chegada tiverem sido coletadas e aprovadas em D05.

### RF08 — Registrar uma reclamação sobre a refeição

**Requisito:** O sistema deve permitir registrar uma reclamação sobre uma refeição já servida, independentemente de avaliação por nota.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN07, RN10. **Dependência:** RF01. **Decisões pendentes:** D03, D04, D06.

- **CA-RF08-01:** Dada uma refeição elegível, quando enviada uma categoria válida e descrição entre 1 e 1.000 caracteres após remover espaços nas extremidades, então a reclamação será persistida com a refeição e o instante do envio, e confirmada sem exigir nota ou avaliação anterior.
- **CA-RF08-02:** Dada uma categoria inválida, descrição vazia/acima do limite ou refeição inexistente/não elegível, quando houver envio, então o sistema informará o motivo e não gravará a reclamação.
- **CA-RF08-03:** Dado um registro concluído, quando apresentada a confirmação, então ela não afirmará encaminhamento ao RU, resposta institucional ou publicação pública. Esses fluxos dependem de D06.

## 4. Regras de negócio

A origem distingue regras já documentadas ou presentes no código das propostas desta revisão. Existência no código não significa homologação.

| ID | Regra | Aplicação | Origem / situação |
|---|---|---|---|
| RN01 | Identificar cada refeição por campus, data e tipo. Avaliações, reclamações e intenções referenciam a refeição, não apenas o nome do prato. | RF01, RF02, RF04–RF08 | Contrato de importação e modelo atual. |
| RN02 | Exibir dias e refeições publicados para o campus. Ausência de dados não comprova ausência de serviço. Adotar semana de segunda a domingo e horário de Brasília nas regras temporais. | RF01, RF02 | Fonte por campus já prevista; convenções temporais propostas em D01. |
| RN03 | As dietas são comum, padrão, ovolactovegetariano e vegetariano estrito. A seleção corresponde à classificação exata, sem incluir automaticamente outras classes. | RF03 | API atual; validar inclusão dos itens comuns em D02. |
| RN04 | Aplicar exclusões cumulativamente pelas marcações da fonte. Vocabulário: leite, ovo, glúten, cogumelo, amendoim, mel, soja, pimenta, oleaginosas, carne suína e frutos do mar. A lista mistura alérgenos e outras restrições. Ausência de marcação não certifica segurança alimentar. | RF03 | Vocabulário do contrato; informação desconhecida a tratar em D02. |
| RN05 | Aceitar avaliações desde o início do serviço, inclusive, até antes de 00h do dia seguinte à data da refeição, no fuso `America/Sao_Paulo`. Após o prazo, manter o histórico consultável. Não exigir check-in ou planejamento nem afirmar comprovação de consumo. Sem horário validado, não presumir elegibilidade. Para reclamações, permanece a proposta de liberação no início do serviço, com prazo final ainda a definir em D03/D06. | RF04, RF08 | Janela de avaliação acordada com o responsável pelos requisitos nesta revisão; horários reais e política de reclamações pendentes. |
| RN06 | Aceitar nota inteira de 1 a 5 e comentário opcional de até 500 caracteres. Registrar o instante do envio separadamente da data da refeição, sem alterar esta última. | RF04, RF05 | Limites e campos do schema atual. |
| RN07 | Reimportar a mesma refeição deve atualizar itens sem duplicar a refeição ou apagar avaliações, reclamações e intenções associadas; preservar também o estado ativo/cancelado das intenções. | RF05, RF06, RF08 | Avaliações: contrato de importação. Extensão proposta para reclamações e intenções; validar em D04/D06. |
| RN08 | Cada identidade mantém no máximo uma intenção ativa por refeição futura; cancelamento remove sua contribuição da estimativa. Intenção não é presença nem reserva. | RF06, RF07 | Planejamento previsto; identidade e unicidade propostas em D04. |
| RN09 | Calcular movimento com intenções ativas do recorte informado e amostra mínima validada. Não converter contagem por refeição em horário de chegada ou tempo de espera. | RF07 | Dependência de dados já prevista; método e limiar pendentes em D05. |
| RN10 | Exigir categoria (qualidade, higiene, atendimento ou outros) e descrição de 1 a 1.000 caracteres na reclamação, sem exigir nota. Registro não equivale a encaminhamento oficial ao RU. | RF08 | Independência prevista; categorias, limites e destino propostos em D06. |

## 5. Requisitos não funcionais

As metas numéricas são **propostas para aprovação em D07**, não resultados medidos nem exigências atribuídas à professora. Registrar ambiente, versão, massa de dados, ferramenta, resultado e evidência em cada verificação.

### RNF01 — Atender às consultas com desempenho mensurável

**Requisito:** O sistema deve responder às consultas da API de cardápio em até 2 segundos no percentil 95, no cenário abaixo. **Relacionados:** RF01–RF03.

- **CA-RNF01-01:** Em homologação, executar 50 usuários virtuais simultâneos por 5 minutos, após 1 minuto de aquecimento, com pausa de 1 segundo entre consultas por usuário. Usar 4 semanas, 5 campi, 3 refeições por dia e 10 itens por refeição; são dados sintéticos, não uma afirmação de funcionamento do RU. Distribuir igualmente consultas semanais sem filtro, por dieta e por exclusão alimentar. Exigir p95 menor ou igual a 2 segundos em cada grupo e taxa total de falhas menor que 1% (timeouts, erros de transporte, respostas não 2xx ou conteúdo inválido para a consulta).
- **CA-RNF01-02:** O relatório deve informar recursos do servidor, localização do gerador de carga, versões, estado do cache, quantidade de requisições, p95 e falhas. Medição da API não será apresentada como tempo de carregamento da interface.

**Verificação:** versionar script de carga, gerador da massa, parâmetros de dieta/exclusão, distribuição das marcações e preparação do cache, junto ao relatório na issue. Ainda não executado.

### RNF02 — Manter os cardápios sincronizados

**Requisito:** O sistema deve verificar a fonte pelo menos uma vez a cada 24 horas e incorporar uma publicação válida até 24 horas após ficar acessível à rotina, enquanto fonte e infraestrutura estiverem disponíveis. **Relacionados:** RF01, RF02; RN01, RN02, RN07.

- **CA-RNF02-01:** Dada nova publicação válida em fonte de teste com instante conhecido, quando a rotina agendada operar, então seus cardápios serão importados em até 24 horas, com campus, URL e instante de sucesso registrados. Incluir publicação imediatamente após uma consulta da rotina e medir até a conclusão da importação seguinte; o intervalo de consulta deve deixar margem para o processamento dentro das 24 horas.
- **CA-RNF02-02:** Dada a mesma publicação processada duas vezes, quando terminar a segunda execução, então não haverá refeições duplicadas nem perda de avaliações, reclamações ou intenções associadas, preservando o estado ativo/cancelado destas. Os vínculos ainda não implementados deverão integrar o cenário de teste quando forem desenvolvidos.
- **CA-RNF02-03:** Dada fonte indisponível, quando houver falha, então ela será registrada por campus, preservando dados e data da última importação bem-sucedida, sem anunciar atualização concluída.

**Verificação:** integração com fonte controlada e registros de agendamento/importação. O prazo é proposta; publicação semanal não implica dia fixo de publicação.

### RNF03 — Preservar dados diante de variações e falhas de extração

**Requisito:** O extrator deve tolerar as variações de PDF do conjunto de referência e isolar falhas por campus, preservando a última importação válida. **Relacionados:** RF01–RF03; RN02, RN04, RN07.

- **CA-RNF03-01:** Dado um conjunto versionado de PDFs com resultados esperados revisados pela equipe, incluindo quebra de linha em nomes, espaços adicionais e repetição de cabeçalho, a extração deverá corresponder integralmente à saída esperada: mesmas chaves, quantidades de registros e valores de campus, data, refeição, item, dieta e marcações alimentares, sem omissões, registros extras ou duplicações. Registrar origem, variação e normalizações permitidas de cada arquivo de teste antes da execução; não ajustar o resultado esperado para ocultar divergências.
- **CA-RNF03-02:** Dado PDF ilegível, vazio ou de estrutura não reconhecida em um campus e PDFs válidos nos demais, quando a rotina executar, então os demais serão processados, a falha será identificada por campus e os dados anteriores do campus afetado não serão substituídos por resultado incompleto.
- **CA-RNF03-03:** Dada correção para formato antes não suportado, quando proposta sua integração, então o PDF que reproduz a falha e o resultado esperado deverão compor a regressão, e todo o conjunto deverá passar.

**Verificação:** comparação com arquivos de referência revisados e simulação de falha isolada. “Pequenas variações” fica limitado aos casos declarados; outros formatos exigem análise, sem promessa de ajuste em prazo indefinido.

### RNF04 — Disponibilizar uma versão para avaliação

**Requisito:** O sistema deve disponibilizar uma versão de avaliação por URL HTTPS, com instruções de acesso e identificação da versão. **Relacionados:** RFs incluídos na demonstração.

- **CA-RNF04-01:** Em sessão de navegador limpa e externa à máquina de desenvolvimento, a URL deverá abrir sem erro de certificado ou instalação de ferramentas locais; credenciais de demonstração, se necessárias, deverão constar nas instruções.
- **CA-RNF04-02:** Durante a janela de avaliação acordada e registrada, uma checagem a cada 5 minutos deverá acessar a interface e consultar um cardápio. Cada checagem deverá renderizar a interface e o cardápio em até 10 segundos no total, exibindo campus, semana e itens correspondentes a uma massa conhecida e versionada. Todas deverão passar; registrar início, fim, duração e resultado de cada checagem. O limite de 10 segundos é proposta sujeita a D07. Isso não constitui promessa de disponibilidade contínua fora da janela.
- **CA-RNF04-03:** O roteiro deverá distinguir protótipo, dados de exemplo e funções integradas. Página estática não comprova atendimento dos RFs de persistência.

**Verificação:** roteiro, commit publicado e relatório das checagens. URL e janela a registrar em D07.

### RNF05 — Verificar a segurança estática do código

**Requisito:** O projeto deve executar análise estática de segurança e não manter achados altos ou críticos em aberto na versão aceita. **Relacionados:** todos os RFs implementados.

- **CA-RNF05-01:** Cada proposta de integração de código deverá executar SAST sobre o código próprio em Python e JavaScript, com ferramenta, versão e regras registradas. Falha de execução ou linguagem não analisada não contará como aprovação.
- **CA-RNF05-02:** O relatório da versão candidata deverá apresentar zero achados altos ou críticos em aberto. Falso positivo só poderá ser encerrado com justificativa rastreável e revisão por outro integrante; ocultar ou desativar regra sem justificativa não atende ao critério.
- **CA-RNF05-03:** A evidência deverá identificar commit, arquivos/linguagens cobertos e exclusões justificadas. A verificação deverá impedir integração enquanto houver falha ou achado bloqueante.

**Verificação:** pipeline e relatório. Ferramenta e equivalência de severidades pendentes em D07. SAST não comprova sozinho a segurança completa do produto.

## 6. Rastreabilidade e evidências

Os caminhos abaixo são pontos de inspeção na versão-base `717d960`, não comprovação de aceitação de ponta a ponta.

| Requisito | Origem | Evidência existente / ponto de inspeção | Lacuna para aceitação |
|---|---|---|---|
| RF01 | Visão: consultar cardápio | `backend/app/api/routes/cardapio.py`; `backend/tests/test_cardapio_api.py` | Interface integrada, origem/atualização visíveis e indisponibilidade. |
| RF02 | Visão: consultar por campus | `backend/app/api/routes/campus.py`; filtros em `cardapio.py` | Seleção dos cinco campi e troca na interface. |
| RF03 | Visão: restrições alimentares | Filtros em `cardapio.py`; contrato de importação | Semântica das dietas; booleanos atuais não distinguem desconhecido de ausência. |
| RF04 | Visão: avaliar refeições | `backend/app/api/routes/avaliacao.py`; `backend/app/schemas/avaliacao.py` | API atual não verifica horário de elegibilidade; D03/D04 pendentes. |
| RF05 | Visão: consultar avaliações | Listagem em `avaliacao.py`; contrato de reimportação | Verificar persistência e histórico na interface. |
| RF06 | Sprint 02: substituir check-in | `scrum/sprint02.md` | Planejamento pendente; definir identidade e dados coletados. |
| RF07 | Visão: estimar movimento | Dependência de RF06 documentada | Resolver D05 antes de prometer horário de pico. |
| RF08 | Sprint 02: reclamações independentes | Visão e Sprint 02 | Validar política e implementar fluxo independente. |
| RNF01 | v1.0: desempenho no pico | Critério agora quantificado | Aprovar cenário e executar medição. |
| RNF02 | v1.0: atualização semanal | `extracao/extracao/sincronizar.py`; `extracao/tests/test_sincronizar.py` | Evidenciar agendamento, prazo e última atualização. |
| RNF03 | v1.0: resiliência | `extracao/tests/test_main.py`; `extracao/tests/test_cobertura_total.py` | Revisar conjunto de referência e verificar cenários propostos. |
| RNF04 | v1.0: acesso para avaliação | Link de protótipo no README | Validar versão integrada e janela de avaliação. |
| RNF05 | v1.0: SAST | Pipeline pendente na Sprint 02 | Configurar ferramenta/bloqueio e guardar relatório. |

### Registro de validação

A issue de cada requisito deverá citar ID, RNs e CAs e a tela específica do protótipo, quando aplicável. O board geral não substitui a identificação do fluxo. Preencher após a execução:

| Campo | Conteúdo |
|---|---|
| Requisito e critérios | Ex.: RF04; CA-RF04-01 a CA-RF04-03. |
| Rastreabilidade | Links reais da issue, tela/fluxo do protótipo, PR e sprint. |
| Versão e ambiente | Commit, ambiente/URL, ferramenta e massa de dados. |
| Execução | Data, responsável, passos e resultado esperado/observado por CA. |
| Evidência | Relatório, teste ou captura verificável. |
| Revisão | Revisor, decisão (aceito/reprovado/bloqueado) e pendências. |

Não foram inventados links de issues, atas, entrevistas ou aprovações nesta revisão. Acrescentar esses registros conforme ocorrerem.

## 7. Decisões pendentes

As propostas sem decisão registrada não são políticas já acordadas. D03 registra o acordo feito nesta conversa com o responsável pelos requisitos sobre a janela de avaliação; isso não representa homologação por toda a equipe. Os demais itens dependentes permanecem em revisão até registrar decisão, data, participantes e justificativa em issue ou ata.

| ID | Decisão necessária / proposta | Impacto |
|---|---|---|
| D01 | Confirmar semana de segunda a domingo e fuso `America/Sao_Paulo`. Não presumir todas as refeições diariamente em todos os campi. | RF01, RF02; RN02. |
| D02 | Confirmar dieta exata ou inclusão de itens comuns; definir informação alimentar desconhecida e revisar cobertura das marcações com PDFs reais. | RF03; RN03, RN04; extração e banco. |
| D03 | Janela de avaliação definida nesta revisão: início do serviço até antes de 00h do dia seguinte, em Brasília, sem check-in. Permanecem pendentes a fonte de horários por campus/refeição, o tratamento de cancelamento do serviço e a janela de reclamações (D06). | RF04, RF06, RF08; RN05, RN08. |
| D04 | Definir identidade (conta, sessão ou outro mecanismo), persistência entre acessos, preservação de intenções na reimportação (RN07) e política de repetição de avaliações/reclamações. Não alegar uma intenção por pessoa sem mecanismo que a sustente. | RF04, RF06–RF08. |
| D05 | Escolher demanda por refeição ou coleta de faixas de chegada em RF06. Definir faixas, amostra mínima e cálculo; incluir testes com total mínimo−1, mínimo e mínimo+1. | Bloqueia RF07 e pode alterar RF06. |
| D06 | Validar categorias e limite de 1.000 caracteres; definir acesso, retenção, preservação na reimportação (RN07), moderação e eventual encaminhamento de reclamações. Proposta: sem publicação pública nem encaminhamento automático. | RF08; RN10; não presumir participação institucional do RU. |
| D07 | Aprovar ou ajustar carga, prazo de sincronização, conjunto de PDFs, janela de avaliação, limite de 10 segundos por checagem e ferramenta/regras de SAST. | RNF01–RNF05. |

### Condições propostas para iniciar e concluir um requisito

Estas condições não são uma transcrição do DoR/DoD citado no Figma. A equipe deve conciliá-las com o material existente.

- **Pronto para desenvolvimento:** descrição/prioridade revisadas; CAs e RNs vinculados; decisões bloqueantes resolvidas; dependências, protótipo aplicável e issue identificados.
- **Pronto para aceitação:** CAs executados com evidência; desvios corrigidos ou requisito formalmente revisto; PR revisado por outro integrante; documentação e rastreabilidade atualizadas. Requisito bloqueado não deve ser marcado como aceito.

## 8. Restrições e histórico

- O projeto depende dos PDFs e da disponibilidade da fonte do RU; links e formato podem mudar. A origem está descrita na visão e no contrato de importação.
- Dias, horários, completude das marcações e alterações do cardápio precisam ser conferidos na fonte, não deduzidos da ausência de registros.
- Estimativa depende da adesão e não representa medição da fila real.
- Esta versão especifica expectativas para revisão; não certifica atendimento pelo produto.

| Versão | Data | Alteração | Validação |
|---|---|---|---|
| 1.0 | Não registrada no documento original | Oito RFs, cinco RNFs e restrições; planejamento substitui check-in. | Consultar histórico Git e Sprint 02. |
| 1.1 | 28/09/2026 | Preserva IDs; adiciona CAs, RNs, metas propostas, rastreabilidade e decisões; distingue releases acadêmicas de prioridades do produto. Após revisão, registra acordo com o responsável pelos requisitos: avaliações apenas do início do serviço ao fim do dia e notas separadas por campus/data/refeição, sem média histórica por prato. | Revisão da equipe pendente. |
