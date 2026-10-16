# Documento de Requisitos — Bandejão

**Versão:** 1.2 — proposta de revisão em 14/10/2026

**Situação:** a versão 1.2 incorpora as decisões D01–D08 do grupo, escolhidas para reduzir o atrito de uso e o esforço de implementação até a Release 2 (25/11/2026).

## 1. Objetivo e origem

Especificar o comportamento esperado do Bandejão, suas regras de negócio e critérios verificáveis, em resposta à pré-avaliação da professora.

Fontes: [documento de visão](documento_de_visao.md), requisitos v1.0, [Sprint 02](scrum/sprint02.md) e [contrato de importação](handoff_banco_e_importacao.md). O código foi consultado para identificar lacunas, não para considerar funcionalidades automaticamente aceitas. Esta revisão não inclui novas entrevistas nem validação do Figma.

**Release acadêmica e prioridade do produto são diferentes:** a Release 1 avalia definição e organização; a Release 2 avalia implementação. As antigas divisões por release passam a ser chamadas de **núcleo** (RF01–RF05 e RF08) e **evolução** (RF06–RF07), preservando a prioridade. O compromisso de implementação depende do planejamento da equipe.

Os IDs RF01–RF08 e RNF01–RNF05 foram preservados; o RNF06 foi acrescentado na v1.2. RN identifica regra de negócio; CA identifica critério de aceitação. Os critérios são expectativas, não testes já executados. Decisões novas ou incompletas estão na seção 7.

## 2. Vocabulário e limites

| Termo | Significado |
|---|---|
| Campus | Darcy Ribeiro, Ceilândia, Gama, Planaltina ou Fazenda Água Limpa. |
| Refeição | Oferta identificada por campus + data + tipo (café da manhã, almoço ou jantar), não um prato isolado. |
| Item | Preparação ou alimento de uma refeição, com categoria, dieta e marcações da fonte. |
| Semana | Segunda-feira a domingo que contém a data selecionada; convenção definida em D01. |
| Avaliação | Nota da refeição, com comentário opcional. |
| Reclamação | Relato sobre uma refeição, independente de nota. |
| Planejamento | Intenção de comparecer; não confirma presença nem representa reserva. |
| Estimativa de movimento | Agregação de intenções; não mede fila real nem tempo de espera. |
| Identidade | Código aleatório gerado pelo app no navegador do usuário (D04). Não é conta, não contém dado pessoal e não identifica uma pessoa: o mesmo usuário em outro navegador, ou após limpar os dados, terá outra identidade. |

Não estão incluídos reserva, pagamento, controle de acesso ao RU, garantia de resposta institucional às reclamações nem cadastro, login ou recuperação de senha (D04: identidade anônima por navegador). O check-in foi substituído por planejamento na Sprint 02 e não é pré-condição para avaliar.

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

**Prioridade:** núcleo. **Regras:** RN03, RN04. **Dependências:** RF01, RF02. **Decisão:** D02.

- **CA-RF03-01:** Dados itens de dietas diferentes, quando uma dieta for selecionada, então serão exibidos os itens compatíveis com essa dieta, conforme RN03 (a seleção ovolactovegetariano inclui também itens vegetarianos estritos), mantendo a identificação da refeição.
- **CA-RF03-02:** Dados itens marcados com leite, soja ou ambos, quando leite e soja forem excluídos, então nenhum item com qualquer uma dessas marcações será exibido. Com dieta e restrições selecionadas, cada item deverá atender a todos os filtros.
- **CA-RF03-03:** Dada uma refeição sem itens após a filtragem, quando o resultado for exibido, então será informado que nenhum item corresponde aos filtros. Ao limpar os filtros, todos os itens da consulta original voltarão a aparecer.
- **CA-RF03-04:** Dado um resultado filtrado, quando exibido, então ficará explícito que o filtro usa as marcações publicadas pelo RU e não certifica ausência de ingredientes ou contaminação cruzada. Informação desconhecida não será apresentada como ausência confirmada.

### RF04 — Registrar uma avaliação de refeição

**Requisito:** O sistema deve permitir registrar uma nota para uma refeição do dia, a partir do início do serviço até antes de 00h do dia seguinte no horário de Brasília, com comentário opcional.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN06. **Dependência:** RF01. **Decisões:** D03 e D04 (identidade anônima por navegador).

- **CA-RF04-01:** Dada uma refeição elegível pela RN05, quando uma nota inteira de 1 a 5 for enviada, com comentário ausente ou de até 500 caracteres, então a avaliação será persistida e confirmada, vinculada à refeição e ao instante do envio.
- **CA-RF04-02:** Dada uma nota ausente, fracionária ou fora de 1 a 5, ou comentário acima de 500 caracteres, quando houver envio, então o sistema informará o campo inválido e não gravará a avaliação.
- **CA-RF04-03:** Dada uma refeição inexistente ou tentativa anterior ao início do serviço ou a partir de 00h do dia seguinte, quando houver envio, então o sistema recusará a avaliação e explicará o motivo. Verificar os limites: antes do início (recusar), no início (permitir), antes de 00h (permitir) e exatamente às 00h do dia seguinte (recusar), no fuso `America/Sao_Paulo`. Não será exigido check-in ou planejamento prévio; a janela não comprova consumo da refeição.
- **CA-RF04-04:** Dada uma identidade que já avaliou uma refeição, quando enviar nova nota para a mesma refeição, então a avaliação anterior será atualizada, sem criar uma segunda (D04f). Sem login, isso limita duplicações acidentais, mas não impede quem trocar de navegador.

### RF05 — Consultar o histórico de avaliações

**Requisito:** O sistema deve permitir consultar o histórico de avaliações vinculadas a uma refeição.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN06, RN07. **Dependência:** RF04.

- **CA-RF05-01:** Dada uma refeição com avaliações, quando seu histórico for consultado, então serão exibidos nota, comentário quando existente e data/hora do registro, do mais recente ao mais antigo, sem avaliações de outras refeições.
- **CA-RF05-02:** Dada uma refeição sem avaliações, quando consultada, então será informada a ausência de avaliações, sem notas ou médias fictícias.
- **CA-RF05-03:** Dada uma avaliação registrada, quando a página for recarregada, o prazo de avaliação terminar ou a fonte da mesma refeição for reimportada, então a avaliação continuará disponível no histórico e vinculada à mesma refeição.
- **CA-RF05-04:** Dados os mesmos pratos ofertados em outra data ou campus, quando o histórico da nova refeição for consultado, então não serão reutilizadas as avaliações anteriores. Sem avaliações próprias, será exibido “sem avaliações”, conforme CA-RF05-02. Uma eventual média deve considerar apenas notas da mesma combinação campus + data + tipo de refeição; média histórica por prato fica fora deste escopo.

### RF06 — Registrar o planejamento de refeições

**Requisito:** O sistema deve permitir marcar e desmarcar as refeições futuras em que o usuário pretende comparecer ao RU.

**Prioridade:** evolução. **Regras:** RN01, RN07, RN08. **Dependências:** RF01, RF02. **Decisões:** D03, D04 (identidade anônima por navegador) e D05.

- **CA-RF06-01:** Dada uma refeição futura disponível, quando marcada, então a intenção será salva com campus, data e tipo, reaparecendo ao reabrir o planejamento com a mesma identidade (código anônimo do navegador, D04).
- **CA-RF06-02:** Dada uma intenção já registrada, quando a mesma marcação for reenviada pela mesma identidade, então continuará existindo apenas uma intenção ativa para aquela refeição.
- **CA-RF06-03:** Dada uma intenção ativa, quando desmarcada, então deixará de compor as contagens. Tentativas de marcar uma refeição cujo início seja menor ou igual ao instante da tentativa serão recusadas. Verificar tentativas antes, no instante exato e depois do início, conforme os horários a validar em D03.

### RF07 — Estimar o período de maior movimento

**Requisito:** O sistema deve apresentar uma estimativa de maior movimento por campus, data e refeição com base nas intenções registradas.

**Prioridade:** evolução. **Regras:** RN08, RN09. **Dependência:** RF06. **Decisão:** D05.

**Lacuna e proposta:** a v1.0 prometia estimar um horário, mas RF06 coleta apenas dia e refeição. Decisão D05: limitar RF07 à demanda (intenções) por refeição, sem horário de chegada. Coletar faixas de chegada fica fora do escopo da Release 2.

- **CA-RF07-01:** Dado um conjunto controlado de intenções ativas, quando calculada a estimativa, então a contagem corresponderá às intenções do campus, data e refeição selecionados, excluindo cancelamentos e duplicações da mesma identidade.
- **CA-RF07-02:** Dado um total inferior à amostra mínima definida em D05, quando consultado, então o sistema informará dados insuficientes, sem afirmar um pico. O limiar é de 10 intenções ativas por campus, data e refeição (D05b), definido como constante de configuração; os testes de limite (9, 10 e 11) precisam ser registrados antes da implementação.
- **CA-RF07-03:** Dada uma amostra suficiente, quando exibido o resultado, então serão apresentados contagem, período comparado e instante do cálculo, identificando-o como estimativa de intenções. Empates mostrarão todos os períodos empatados. Horários de chegada não serão apresentados nesta versão.
- **CA-RF07-04:** Dados simulados usados em demonstração serão identificados como tal na interface e na documentação, nunca apresentados como intenções de usuários reais (D05c).

### RF08 — Registrar uma reclamação sobre a refeição

**Requisito:** O sistema deve permitir registrar uma reclamação sobre uma refeição já servida, independentemente de avaliação por nota.

**Prioridade:** núcleo. **Regras:** RN01, RN05, RN07, RN10. **Dependência:** RF01. **Decisões:** D03, D04 (identidade anônima por navegador) e D06.

- **CA-RF08-01:** Dada uma refeição elegível, quando enviada uma categoria válida e descrição entre 1 e 1.000 caracteres após remover espaços nas extremidades, então a reclamação será persistida com a refeição e o instante do envio, e confirmada sem exigir nota ou avaliação anterior.
- **CA-RF08-02:** Dada uma categoria inválida, descrição vazia/acima do limite ou refeição inexistente/não elegível, quando houver envio, então o sistema informará o motivo e não gravará a reclamação.
- **CA-RF08-03:** Dado um registro concluído, quando apresentada a confirmação, então ela não afirmará encaminhamento ao RU, resposta institucional ou publicação pública. Esses fluxos dependem de D06.
- **CA-RF08-04:** Dada uma reclamação registrada, quando outra identidade usar o app, então ela não será exibida. O formulário não terá campo de nome nem anexo de foto, e não haverá lista pública. O acesso é restrito à identidade que a registrou e à equipe (leitura interna, por rota protegida por token ou diretamente no banco). As telas do protótipo (6 categorias, nome opcional, foto e lista de reclamações) serão ajustadas a esta regra. Depende de D04: se um mecanismo de identidade não for mantido, a regra deve ser revista.

## 4. Regras de negócio

A origem distingue regras já documentadas ou presentes no código das decisões desta versão. Existência no código não significa homologação.

| ID | Regra | Aplicação | Origem / situação |
|---|---|---|---|
| RN01 | Identificar cada refeição por campus, data e tipo. Avaliações, reclamações e intenções referenciam a refeição, não apenas o nome do prato. | RF01, RF02, RF04–RF08 | Contrato de importação e modelo atual. |
| RN02 | Exibir dias e refeições publicados para o campus. Ausência de dados não comprova ausência de serviço. Adotar semana de segunda a domingo e horário de Brasília nas regras temporais. | RF01, RF02 | Fonte por campus já prevista; convenções temporais definidas em D01. |
| RN03 | As dietas são comum, padrão, ovolactovegetariano e vegetariano estrito. A seleção inclui a classe escolhida e as mais restritivas compatíveis com ela: ovolactovegetariano exibe também vegetariano estrito; as demais classes correspondem exatamente à selecionada (decisão D02). A API atual ainda filtra por classe exata e precisa ser ajustada. | RF03 | API atual (classe exata, a ajustar); inclusão definida em D02. Itens comuns permanecem fora dos filtros vegetarianos. |
| RN04 | Aplicar exclusões cumulativamente pelas marcações da fonte. Vocabulário: leite, ovo, glúten, cogumelo, amendoim, mel, soja, pimenta, oleaginosas, carne suína e frutos do mar. A lista mistura alérgenos e outras restrições. Ausência de marcação não certifica segurança alimentar. | RF03 | Vocabulário do contrato; informação desconhecida a tratar em D02. |
| RN05 | Aceitar avaliações desde o início do serviço, inclusive, até antes de 00h do dia seguinte à data da refeição, no fuso `America/Sao_Paulo`. Após o prazo, manter o histórico consultável. Não exigir check-in ou planejamento nem afirmar comprovação de consumo. Os horários de início por refeição vêm de uma tabela de configuração versionada (D03); enquanto uma refeição não tiver horário cadastrado nem padrão, a avaliação é recusada, sem presumir elegibilidade. Para reclamações, vale a mesma janela das avaliações (D03/D06). | RF04, RF08 | Janela de avaliação e horários conforme D03; reclamações seguem a mesma janela (D06). |
| RN06 | Aceitar nota inteira de 1 a 5 e comentário opcional de até 500 caracteres. Registrar o instante do envio separadamente da data da refeição, sem alterar esta última. | RF04, RF05 | Limites e campos do schema atual. |
| RN07 | Reimportar a mesma refeição deve atualizar itens sem duplicar a refeição ou apagar avaliações, reclamações e intenções associadas; preservar também o estado ativo/cancelado das intenções. | RF05, RF06, RF08 | Avaliações: contrato de importação. Extensão proposta para reclamações e intenções; validar em D04/D06. |
| RN08 | Cada identidade (navegador) mantém no máximo uma intenção ativa por refeição futura; a garantia é por navegador, não por pessoa; cancelamento remove sua contribuição da estimativa. Intenção não é presença nem reserva. | RF06, RF07 | Planejamento previsto; identidade e unicidade conforme D04. |
| RN09 | Calcular movimento com intenções ativas do recorte informado e amostra mínima validada. Não converter contagem por refeição em horário de chegada ou tempo de espera. | RF07 | Dependência de dados já prevista; método e limiar pendentes em D05. |
| RN10 | Exigir categoria (qualidade, higiene, atendimento ou outros) e descrição de 1 a 1.000 caracteres na reclamação, sem exigir nota. Registro não equivale a encaminhamento oficial ao RU. | RF08 | Independência prevista; categorias, limites e destino propostos em D06. |

## 5. Requisitos não funcionais

As metas numéricas foram definidas na D07; não são resultados medidos nem exigências atribuídas à professora. Registrar ambiente, versão, massa de dados, ferramenta, resultado e evidência em cada verificação.

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

**Verificação:** integração com fonte controlada e registros de agendamento/importação. O prazo vem da decisão D07b; publicação semanal não implica dia fixo de publicação. Intervalo de consulta: 6 horas (D07b), por agendamento do GitHub Actions ou serviço no Docker; agendamentos do GitHub Actions podem atrasar, e esse atraso deve caber na margem das 24 horas.

### RNF03 — Preservar dados diante de variações e falhas de extração

**Requisito:** O extrator deve tolerar as variações de PDF do conjunto de referência e isolar falhas por campus, preservando a última importação válida. **Relacionados:** RF01–RF03; RN02, RN04, RN07.

- **CA-RNF03-01:** Dado um conjunto versionado de PDFs com resultados esperados revisados pela equipe, incluindo quebra de linha em nomes, espaços adicionais e repetição de cabeçalho, a extração deverá corresponder integralmente à saída esperada: mesmas chaves, quantidades de registros e valores de campus, data, refeição, item, dieta e marcações alimentares, sem omissões, registros extras ou duplicações. Registrar origem, variação e normalizações permitidas de cada arquivo de teste antes da execução; não ajustar o resultado esperado para ocultar divergências.
- **CA-RNF03-02:** Dado PDF ilegível, vazio ou de estrutura não reconhecida em um campus e PDFs válidos nos demais, quando a rotina executar, então os demais serão processados, a falha será identificada por campus e os dados anteriores do campus afetado não serão substituídos por resultado incompleto.
- **CA-RNF03-03:** Dada correção para formato antes não suportado, quando proposta sua integração, então o PDF que reproduz a falha e o resultado esperado deverão compor a regressão, e todo o conjunto deverá passar.

**Verificação:** comparação com arquivos de referência revisados e simulação de falha isolada. “Pequenas variações” fica limitado aos casos declarados; outros formatos exigem análise, sem promessa de ajuste em prazo indefinido.

### RNF04 — Disponibilizar uma versão para avaliação

**Requisito:** O sistema deve disponibilizar uma versão de avaliação por URL HTTPS, com instruções de acesso e identificação da versão. **Relacionados:** RFs incluídos na demonstração.

- **CA-RNF04-01:** Em sessão de navegador limpa e externa à máquina de desenvolvimento, a URL deverá abrir sem erro de certificado ou instalação de ferramentas locais; credenciais de demonstração, se necessárias, deverão constar nas instruções.
- **CA-RNF04-02:** Durante a janela de avaliação acordada e registrada, uma checagem a cada 5 minutos deverá acessar a interface e consultar um cardápio. Cada checagem deverá renderizar a interface e o cardápio em até 10 segundos no total, exibindo campus, semana e itens correspondentes a uma massa conhecida e versionada. Todas deverão passar; registrar início, fim, duração e resultado de cada checagem. O limite de 10 segundos foi definido na D07e. Isso não constitui promessa de disponibilidade contínua fora da janela.
- **CA-RNF04-03:** O roteiro deverá distinguir protótipo, dados de exemplo e funções integradas. Página estática não comprova atendimento dos RFs de persistência.

**Verificação:** roteiro, commit publicado e relatório das checagens. URL e janela a registrar em D07. Janela curta (1 a 2 horas, no dia da avaliação). Não há credenciais de demonstração, pois a proposta D04 dispensa cadastro.

### RNF05 — Verificar a segurança estática do código

**Requisito:** O projeto deve executar análise estática de segurança e não manter achados altos ou críticos em aberto na versão aceita. **Relacionados:** todos os RFs implementados.

- **CA-RNF05-01:** Cada proposta de integração de código deverá executar SAST sobre o código próprio em Python e JavaScript/TypeScript, com ferramenta, versão e regras registradas. Falha de execução ou linguagem não analisada não contará como aprovação.
- **CA-RNF05-02:** O relatório da versão candidata deverá apresentar zero achados altos ou críticos em aberto. Falso positivo só poderá ser encerrado com justificativa rastreável e revisão por outro integrante; ocultar ou desativar regra sem justificativa não atende ao critério.
- **CA-RNF05-03:** A evidência deverá identificar commit, arquivos/linguagens cobertos e exclusões justificadas. A verificação deverá impedir integração enquanto houver falha ou achado bloqueante.

**Verificação:** pipeline e relatório. Ferramentas (D07d): bandit para Python e CodeQL para JavaScript/TypeScript, bloqueando achados altos e críticos. O bandit classifica apenas em baixo, médio e alto; “crítico” só existe no CodeQL. Registrar no relatório essa equivalência de severidades. SAST não comprova sozinho a segurança completa do produto.

### RNF06 — Proteger a escrita administrativa

**Requisito:** As rotas que alteram dados do cardápio (importação) devem exigir um token secreto, usado pela rotina de sincronização. **Relacionados:** RF01; RNF02; D08.

- **CA-RNF06-01:** Dada uma requisição de importação sem token ou com token inválido, quando enviada, então será recusada (401 ou 403) e nenhum dado será gravado.
- **CA-RNF06-02:** Dada a rotina de sincronização configurada com o token correto, quando executar, então a importação será aceita. O token virá de variável de ambiente, nunca do repositório.
- **CA-RNF06-03:** Dado o repositório, quando inspecionado, então não conterá o token real; o `.env.example` terá apenas valor de exemplo.

**Verificação:** testes automatizados da API. Na base da Sprint 03, a rota exige Bearer token e falha fechada quando o segredo não está configurado; a sincronização envia o mesmo segredo pelo ambiente. As rotas HTTP de check-in legado foram retiradas, preservando modelo e tabela para migração futura. A execução no CI e a inspeção do repositório ainda precisam compor a evidência da versão aceita.

## 6. Rastreabilidade e evidências

Os caminhos abaixo são pontos de inspeção na versão-base `717d960`, não comprovação de aceitação de ponta a ponta.

| Requisito | Origem | Evidência existente / ponto de inspeção | Lacuna para aceitação |
|---|---|---|---|
| RF01 | Visão: consultar cardápio | `backend/app/api/routes/cardapio.py`; `backend/tests/test_cardapio_api.py` | Interface integrada, origem/atualização visíveis e indisponibilidade. |
| RF02 | Visão: consultar por campus | `backend/app/api/routes/campus.py`; filtros em `cardapio.py` | Seleção dos cinco campi e troca na interface. |
| RF03 | Visão: restrições alimentares | Filtros em `cardapio.py`; contrato de importação | Semântica das dietas; booleanos atuais não distinguem desconhecido de ausência. |
| RF04 | Visão: avaliar refeições | `backend/app/api/routes/avaliacao.py`; `backend/app/schemas/avaliacao.py` | API atual não verifica horário de elegibilidade nem limita uma avaliação por identidade; D03/D04 pendentes. |
| RF05 | Visão: consultar avaliações | Listagem em `avaliacao.py`; contrato de reimportação | Verificar persistência e histórico na interface. |
| RF06 | Sprint 02: substituir check-in | `scrum/sprint02.md` | Planejamento pendente; implementar identidade anônima por navegador (D04) e rota de intenções. |
| RF07 | Visão: estimar movimento | Dependência de RF06 documentada | Implementar demanda por refeição com amostra mínima (D05); sem horário de pico. |
| RF08 | Sprint 02: reclamações independentes | Visão e Sprint 02 | Implementar modelo e rotas; ajustar o protótipo (4 categorias, sem nome nem foto, sem lista pública). |
| RNF01 | v1.0: desempenho no pico | Critério agora quantificado | Aprovar cenário e executar medição. |
| RNF02 | v1.0: atualização semanal | `extracao/extracao/sincronizar.py`; `extracao/tests/test_sincronizar.py` | Evidenciar agendamento, prazo e última atualização. |
| RNF03 | v1.0: resiliência | `extracao/tests/test_main.py`; `extracao/tests/test_cobertura_total.py` | Revisar conjunto de referência e verificar cenários propostos. |
| RNF04 | v1.0: acesso para avaliação | Link de protótipo no README | Validar versão integrada e janela de avaliação. |
| RNF05 | v1.0: SAST | `.github/workflows/sast.yml`; `scripts/security/POLICY.md`; [evidência da issue 60](evidencias/sast-issue-60.md) | Bandit e CodeQL confirmados em PR real, com artefatos preservados e ambos os checks obrigatórios no ruleset ativo da `main`. |
| RNF06 | Revisão de 14/10/2026: importação sem autenticação | `backend/app/core/security.py`; rota de importação; rotina de sincronização; testes automatizados | Validar a execução no CI e configurar/rotacionar o segredo no ambiente real sem expô-lo. |

### Integração local do frontend — 01/10/2026

A tabela acima preserva a inspeção da versão-base. A aplicação local agora incorpora as telas React/TypeScript/Tailwind da equipe e consulta campi/cardápios pela API. Origem PDF, estados de falha/indisponibilidade e filtros locais sobre os marcadores publicados estão implementados; atualização dos dados, semântica de D01/D02 e aceite operacional continuam pendentes. Avaliações, reclamações, planejamento e lotação permanecem demonstrações sem persistência integrada. Checks locais e respostas simuladas no navegador não comprovam aceite dos RFs. Consulte [Arquitetura](Arquitetura.md) e [Protótipos](prototipos.md).

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

## 7. Decisões

As decisões abaixo orientam a implementação desta versão. Critério: menor atrito para o usuário e menor esforço de implementação, para caber nas cerca de 6 semanas até a Release 2.

| ID | Decisão necessária | Decisão adotada | Impacto |
|---|---|---|---|
| D01 | Semana e fuso horário. | Semana de segunda a domingo, fuso `America/Sao_Paulo`. Não presumir todas as refeições diariamente em todos os campi. | RF01, RF02; RN02. |
| D02 | Filtro de dieta, informação alimentar desconhecida e revisão das marcações. | a) Filtro **inclusivo**: ovolactovegetariano exibe também vegetariano estrito. b) Manter as marcações do RU e avisar na tela que “sem marcação” significa “não marcado na fonte”, não “livre de”. Revisar as marcações com PDFs reais na sprint de verificação. | RF03; RN03, RN04; extração e banco. |
| D03 | Horários de serviço e cancelamentos. | a) Tabela de configuração com o horário de início por refeição (padrão: café ____, almoço ____, jantar ____, a preencher com os horários publicados pelo RU); sem horário, a avaliação é recusada. b) Cancelamento do serviço (“suspenso”) fora do escopo e registrado como limitação conhecida. Janela de avaliação: início do serviço até antes de 00h do dia seguinte, em Brasília, sem check-in. | RF04, RF06, RF08; RN05, RN08. |
| D04 | Identidade do usuário. | a) **Sem cadastro nem login**: identidade anônima por navegador (código aleatório). b) A avaliação não exige login. c), d) e e) (verificação de e-mail, exclusão de conta e retenção) não se aplicam sem conta. f) Uma avaliação por identidade por refeição; novo envio atualiza a anterior. g) Aviso curto de privacidade dizendo o que é guardado. | RF04, RF06–RF08; RN07, RN08. |
| D05 | Estimativa de movimento. | a) Estimar intenções por refeição, campus e data, sem horário de chegada; o resultado é chamado de “intenções”. b) Amostra mínima de **10** intenções ativas (constante de configuração; testes em 9, 10 e 11). c) Na demonstração, usar dados simulados identificados como tal. | Bloqueia RF07; RF06; RN09. |
| D06 | Reclamações. | Quatro categorias (qualidade, higiene, atendimento e outros), até 1.000 caracteres, sem foto, sem nome e sem lista pública. Acesso restrito a quem registrou e à equipe, para análise interna. Sem encaminhamento automático ao RU. Preservada na reimportação (RN07). Depende de D04. | RF08; RN10. |
| D07 | Verificação e metas (cada item é uma decisão). | a) Carga com k6, 50 usuários simultâneos, ambiente local. b) Sincronização a cada 6 horas. c) 4 a 6 PDFs de referência, cobrindo os cinco campi e pelo menos um caso de falha. d) SAST com bandit (Python) e CodeQL (JS/TS), bloqueando achados altos e críticos. e) Checagem de 10 segundos a cada 5 minutos, em janela curta de avaliação. | RNF01–RNF05. |
| D08 | Segurança da importação (nova). | A rota de importação passa a exigir um token secreto, usado pela rotina de sincronização. | RNF06; RNF02. |

### Condições propostas para iniciar e concluir um requisito

Estas condições não são uma transcrição do DoR/DoD citado no Figma. A equipe deve conciliá-las com o material existente.

- **Pronto para desenvolvimento:** descrição/prioridade revisadas; CAs e RNs vinculados; decisões bloqueantes resolvidas; dependências, protótipo aplicável e issue identificados.
- **Pronto para aceitação:** CAs executados com evidência; desvios corrigidos ou requisito formalmente revisto; PR revisado por outro integrante; documentação e rastreabilidade atualizadas. Requisito bloqueado não deve ser marcado como aceito.

## 8. Restrições e histórico

- O projeto depende dos PDFs e da disponibilidade da fonte do RU; links e formato podem mudar. A origem está descrita na visão e no contrato de importação.
- Dias, horários, completude das marcações e alterações do cardápio precisam ser conferidos na fonte, não deduzidos da ausência de registros.
- Estimativa depende da adesão e não representa medição da fila real.
- A identidade por navegador (D04) não impede manipulação: quem limpar os dados ou usar outro navegador cria uma nova identidade. Notas e estimativas devem ser apresentadas com essa ressalva.
- Esta versão especifica expectativas para revisão; não certifica atendimento pelo produto.

| Versão | Data | Alteração | Validação |
|---|---|---|---|
| 1.0 | Não registrada no documento original | Oito RFs, cinco RNFs e restrições; planejamento substitui check-in. | Consultar histórico Git e Sprint 02. |
| 1.1 | 28/09/2026 | Preserva IDs; adiciona CAs, RNs, metas propostas, rastreabilidade e decisões; distingue releases acadêmicas de prioridades do produto. Após revisão, registra acordo com o responsável pelos requisitos: avaliações apenas do início do serviço ao fim do dia e notas separadas por campus/data/refeição, sem média histórica por prato. | Revisão da equipe pendente. |
| 1.2 | 14/10/2026 | Incorpora as decisões D01–D08 (filtro de dieta inclusivo, horários por tabela de configuração, identidade anônima por navegador em vez de login, estimativa de intenções com amostra mínima de 10, reclamações restritas ao autor e à equipe, metas de verificação). Acrescenta CA-RF04-04, CA-RF07-04, CA-RF08-04 e o RNF06 (token na importação). | Decisões do grupo incorporadas. |
