# Roteiro manual de ponta a ponta

**Objetivo:** conferir os fluxos principais da aplicação integrada, desde uma sessão limpa até o registro de avaliação, reclamação e intenção.

## Preparação

- Use a URL da aplicação integrada e confirme que ela consulta a API publicada. O protótipo visual não substitui a versão integrada.
- Registre a data, o commit esperado da versão, o navegador e o dispositivo na evidência em `docs/evidencias/`.
- Abra uma janela anônima para começar sem dados locais anteriores. Não informe dados pessoais reais na reclamação.
- Para cada execução, preencha o resultado observado, a data e o commit em todos os passos. Se o fluxo falhar, anote a mensagem e abra uma issue com a evidência.
- Repita a execução em um celular físico. Emulador ou redimensionamento do navegador não substitui essa etapa.

## Passos

### 1. Cardápio da semana

- **Ação:** selecionar um campus e uma semana com publicação conhecida.
- **Esperado:** aparecem somente as refeições publicadas para o campus e o período; origem e última importação são identificadas quando disponíveis.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 2. Filtro por dieta

- **Ação:** escolher uma dieta presente no cardápio e comparar os itens antes e depois do filtro.
- **Esperado:** os itens seguem a classe indicada; o filtro ovolactovegetariano também inclui itens vegetarianos estritos.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 3. Filtro por alérgeno

- **Ação:** selecionar um alérgeno que esteja marcado em um item do cardápio.
- **Esperado:** o item marcado é excluído conforme o filtro. A interface esclarece que ausência de marcação significa “não marcado na fonte”, não “livre de”.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 4. Avaliação de uma refeição

- **Ação:** escolher uma refeição dentro do período permitido e enviar uma nota, com comentário opcional.
- **Esperado:** a aplicação confirma o envio; dados inválidos ou período encerrado exibem o motivo sem registrar a avaliação.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 5. Histórico da refeição

- **Ação:** abrir o histórico da mesma refeição após enviar a avaliação.
- **Esperado:** a avaliação aparece vinculada àquela refeição, sem misturar campus, data ou tipo de refeição.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 6. Reclamação

- **Ação:** enviar uma reclamação de teste sem nome, telefone ou outro dado pessoal.
- **Esperado:** a aplicação confirma o recebimento ou informa o erro. Reclamações não aparecem em uma lista pública.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 7. Marcar e desmarcar intenção

- **Ação:** marcar uma refeição futura e depois desmarcá-la.
- **Esperado:** a interface confirma a intenção ativa e sua remoção; não apresenta intenção como reserva ou presença.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

### 8. Estimativa

- **Ação:** consultar a estimativa para campus, data e refeição com os dados disponíveis.
- **Esperado:** dados reais e simulados permanecem separados e identificados; abaixo do mínimo configurado a aplicação não apresenta uma contagem como se fosse confiável.
- **Obtido:** a preencher na execução.
- **Data:** a preencher.
- **Commit:** a preencher.
- **Resultado:** pendente.

## Execução em celular

Copie os passos acima e preencha uma segunda rodada usando um celular físico. Registre modelo, sistema, navegador, data e commit na evidência. Anote diferenças de tela ou de comportamento.