# Engenharia de Requisitos — Estudo

## O que é

Engenharia de requisitos é a disciplina que trata de descobrir, entender, documentar e gerenciar o que um sistema de software deve fazer e sob quais condições. É a etapa que conecta as necessidades reais de quem vai usar o sistema (stakeholders) com o que a equipe de desenvolvimento vai efetivamente construir.

Um requisito mal levantado ou mal escrito custa caro: pesquisas apontam que grande parte dos problemas de projeto de software (requisitos incompletos, falhas de comunicação, mudanças constantes, especificações abstratas) tem origem nessa etapa, não na programação em si.

## Tipos de requisitos

### Requisitos funcionais
Descrevem **o que** o sistema deve fazer — as funcionalidades e comportamentos concretos.

> Exemplo (Bandejão): "o sistema deve permitir filtrar o cardápio do dia por restrição alimentar (vegetariano, sem glúten, sem lactose etc.)".

### Requisitos não funcionais
Descrevem **como** o sistema deve se comportar — qualidades e restrições que não são uma funcionalidade específica, mas afetam o sistema como um todo: desempenho, disponibilidade, segurança, usabilidade, escalabilidade.

> Exemplo (Bandejão): "a consulta ao cardápio da semana deve responder em até 1 segundo" ou "o sistema deve continuar funcionando mesmo se a extração do PDF de um campus falhar".

### Requisitos de usuário x requisitos de sistema
- **Requisitos de usuário**: descritos em linguagem natural, de alto nível, do ponto de vista de quem usa (ex: "quero ver o cardápio vegetariano da semana").
- **Requisitos de sistema**: versão técnica e precisa desse mesmo requisito, escrita pela equipe de desenvolvimento, já pensando em como implementar.

### Regras de negócio
Restrições ou políticas que não são requisitos funcionais em si, mas condicionam o comportamento do sistema (ex: "uma avaliação de refeição só pode ser feita por quem registrou check-in naquele restaurante no dia").

## Fases do processo

1. **Elicitação** — descobrir os requisitos junto aos stakeholders.
2. **Análise** — entender, detalhar e identificar conflitos ou inconsistências entre requisitos.
3. **Especificação** — documentar os requisitos de forma clara (histórias de usuário, casos de uso, etc.).
4. **Validação** — checar se o que foi documentado está correto, completo e reflete a necessidade real.
5. **Gestão** — acompanhar mudanças de requisitos ao longo do projeto (rastreabilidade).

Esse processo raramente é linear: é comum voltar a etapas anteriores conforme o entendimento do problema evolui.

## Técnicas de elicitação

- **Entrevistas** com stakeholders (ex: alunos, RU/UnB, coordenação do projeto).
- **Questionários** para levantar necessidades de um grupo maior de usuários.
- **Análise de documentos** já existentes (ex: o formato do cardápio publicado pelo RU).
- **Workshops** com os envolvidos para discutir e priorizar necessidades em grupo.
- **Prototipação** — mostrar telas ou fluxos simples para validar entendimento antes de construir de verdade.
- **Observação/estudo etnográfico** — observar o usuário no contexto real (ex: como um aluno de fato escolhe o que comer no RU).

## Especificação de requisitos

### Histórias de usuário (User Stories)
Muito usadas em métodos ágeis. Seguem o modelo dos "3Cs":

- **Cartão**: descrição curta, em linguagem do usuário.
- **Conversa**: discussão entre time e cliente/usuário para detalhar.
- **Confirmação**: critérios de aceitação que validam se a história foi implementada corretamente.

Formato padrão: *"Como [papel de usuário], eu quero [ação], para [benefício]"*.

> Exemplo: "Como aluno com restrição a glúten, eu quero filtrar o cardápio por essa restrição, para saber rapidamente quais pratos posso comer."

Boas histórias seguem os critérios **INVEST**: Independentes, Negociáveis, geradoras de **Valor**, Estimáveis, pequenas o bastante (**Small**) e **Testáveis**.

### Casos de uso
Descrição textual mais detalhada de como um **ator** (usuário ou outro sistema) interage com o sistema para atingir um objetivo. Estrutura típica:

- **Fluxo normal**: passo a passo do cenário de sucesso ("cenário feliz").
- **Extensões**: fluxos alternativos, erros e exceções.

> Exemplo: caso de uso "Avaliar refeição" — fluxo normal (usuário seleciona o prato do dia, dá uma nota, opcionalmente comenta, sistema salva a avaliação) e extensões (usuário tenta avaliar sem ter feito check-in → sistema bloqueia e informa o motivo).

Boas práticas: manter o fluxo normal enxuto (poucos passos), evitar linguagem técnica e usar vocabulário consistente com o resto da documentação.

## Qualidades de um bom requisito

Um requisito bem escrito deve ser:

- **Correto** — reflete de fato a necessidade do stakeholder.
- **Preciso / não ambíguo** — não dá margem a múltiplas interpretações.
- **Completo** — nada essencial fica de fora.
- **Consistente** — não contradiz outro requisito.
- **Verificável** — dá para testar se foi atendido ou não.

## Priorização

Nem todo requisito entra na primeira versão do sistema. É preciso priorizar considerando valor para o usuário, prazo e esforço de implementação — é isso que define o que entra em cada release.

No caso do Bandejão, essa lógica já aparece no próprio escopo do projeto: a Release 1 concentra o essencial (cardápio, filtros, avaliação), deixando a previsão de horário de pico (que depende de volume de dados histórico) para a Release 2.

## Validação de requisitos

Verificar, junto aos stakeholders, se os requisitos documentados realmente representam o que é necessário — antes de partir para a implementação. Erros encontrados nessa fase são muito mais baratos de corrigir do que erros encontrados depois do sistema pronto.

## Rastreabilidade

Manter a correlação entre requisitos e as partes do código/funcionalidades que os implementam. Isso facilita avaliar o impacto de uma mudança de requisito e evita "esquecer" de atualizar alguma parte do sistema quando um requisito muda.

## Relação com o projeto Bandejão

- A camada de **extração de dados** existe justamente por causa de um requisito não funcional implícito: o sistema depende de uma fonte externa (PDF do RU) que muda de formato e de URL sem aviso, então essa parte precisa ser isolada e resiliente a mudanças.
- Os filtros alimentares (vegetariano, alergias a leite/ovo/glúten/etc.) são requisitos funcionais que só são viáveis porque a fonte de dados já identifica essas informações no cardápio — é um bom exemplo de como um requisito depende diretamente da qualidade dos dados disponíveis.
- A divisão do escopo em Release 1 e Release 2 é, na prática, uma decisão de priorização de requisitos.

## Dúvidas em aberto

*(preencher conforme surgirem dúvidas durante o uso prático, ex: qual técnica de elicitação o grupo vai usar para levantar requisitos com o RU/UnB)*

## Fontes

- [Cap. 3: Requisitos – Engenharia de Software Moderna](https://engsoftmoderna.info/cap3.html)
- [Engenharia de Requisitos — Leandro Raposo, Medium](https://medium.com/@leandro-raposo/engenharia-de-requisitos-b7a36c2e645c)
- [O que são Requisitos Não Funcionais — Visure Solutions](https://visuresolutions.com/pt/alm-guide/non-functional-requirements/)
