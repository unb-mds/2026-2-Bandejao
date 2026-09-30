# Estudo — IA aplicada ao desenvolvimento de software

## O que é um assistente de programação

Um assistente de programação usa modelos de IA generativa para sugerir, explicar ou transformar código a partir de uma instrução e de algum contexto. Dependendo da ferramenta, esse contexto pode incluir o trecho aberto no editor, arquivos do repositório, a conversa ou uma issue. O modelo produz uma sugestão; a ferramenta e as permissões disponíveis determinam se ela apenas aparece para revisão ou se pode também editar arquivos e executar comandos. [A documentação do GitHub descreve esse fluxo para o Copilot](https://docs.github.com/en/copilot/responsible-use/inline-suggestions).

O resultado pode estar correto, incompleto ou parecer convincente sem corresponder ao comportamento desejado. O modelo não substitui a leitura do código, as decisões da equipe ou a validação por testes.

## Formas comuns de uso

| Forma | O que faz | Exemplo |
|---|---|---|
| Sugestão no editor | Completa linhas ou trechos usando o código próximo | Repetição de um padrão já presente no projeto |
| Chat | Responde perguntas e propõe explicações, testes ou alterações | Entender uma rota e solicitar um caso de teste |
| Agente de código | Planeja uma tarefa em etapas e pode usar ferramentas para pesquisar, editar e testar | Corrigir uma issue pequena e preparar um diff para revisão |
| Revisão assistida | Examina um diff e aponta possíveis problemas | Pedir uma segunda leitura de uma mudança antes do PR |

As fronteiras variam por produto. Agentes podem ter permissões para alterar arquivos ou executar comandos; o trabalho realizado precisa ser inspecionado da mesma forma que qualquer contribuição. A documentação do [Copilot Chat](https://docs.github.com/en/copilot/responsible-use/chat) apresenta exemplos de chat, modo agente, testes, correções e revisão.

## Como formular uma solicitação

Uma tarefa pequena, com contexto relevante e critérios de aceite verificáveis, tende a ser mais fácil de orientar e revisar. Um modelo simples:

```text
Objetivo: qual problema precisa ser resolvido?
Contexto: quais arquivos, rotas ou regras ajudam a entender o problema?
Comportamento esperado: o que deve acontecer depois da mudança?
Restrições: o que precisa continuar igual ou ainda depende de decisão?
Verificação: quais testes, comandos ou evidências devem passar?
```

Se a resposta ficar ampla ou vaga, reduza a tarefa, mostre um exemplo de entrada e saída ou esclareça o critério que faltou. As recomendações do GitHub também sugerem dividir tarefas complexas, especificar requisitos e exemplos e fornecer contexto relevante, em vez de abrir arquivos sem relação com o pedido ([boas práticas de prompting e validação](https://docs.github.com/en/copilot/get-started/best-practices)).

## Boas práticas

1. **Defina o trabalho antes de pedir código.** Use uma issue com objetivo, escopo e critérios de aceite. Não peça para o assistente decidir sozinho políticas do produto que ainda precisam de aprovação.
2. **Passe contexto suficiente e pertinente.** Indique os arquivos e contratos envolvidos, as convenções do projeto e o resultado esperado. Não inclua senhas, tokens, dados pessoais ou outros conteúdos que não devam ser enviados ao serviço; confira as regras de privacidade da ferramenta usada.
3. **Peça mudanças pequenas e revisáveis.** Um diff focado ajuda a equipe a entender a causa, revisar o código e localizar regressões.
4. **Leia o diff inteiro.** Confira lógica, nomes, dependências, efeitos colaterais, tratamento de erro, segurança e compatibilidade com a arquitetura. Só aceite partes que você consiga explicar.
5. **Verifique afirmações e fontes.** Para APIs, regras ou fatos que podem mudar, consulte a documentação oficial e os dados reais do projeto. Uma explicação gerada não é evidência de que o comportamento existe.
6. **Rode verificações independentes.** Execute testes, lint e build pertinentes. Os testes sugeridos pela IA também precisam de revisão: eles podem não cobrir o caso importante ou repetir a suposição que introduziu o defeito.
7. **Use o fluxo normal de contribuição.** Registre a issue, trabalhe em branch, vincule o PR, observe a CI e deixe a revisão e o merge seguirem as regras da equipe. Uma revisão automatizada complementa a revisão humana.

O GitHub recomenda entender e revisar sugestões, avaliar segurança e manutenção e usar testes e ferramentas automatizadas. Também documenta riscos de código incorreto, vulnerabilidades, contexto limitado e correspondência com código público ([uso responsável das sugestões](https://docs.github.com/en/copilot/responsible-use/inline-suggestions)).

## Aplicação neste projeto

No Bandejão, um assistente pode ajudar a explicar rotas, preparar testes para a extração de PDFs, organizar uma documentação ou sugerir um ajuste localizado. Ele não deve inventar regras de dieta ou declarar segurança alimentar com base em campos incompletos. As decisões ainda pendentes, como D01 e D02 em [Requisitos](../Requisitos.md#7-decisoes-pendentes), continuam com a equipe. A validação usa o código, a fonte oficial, os testes e a CI do repositório.

## Referências

- [Best practices for using GitHub Copilot — GitHub Docs](https://docs.github.com/en/copilot/get-started/best-practices)
- [Responsible use of GitHub Copilot Chat — GitHub Docs](https://docs.github.com/en/copilot/responsible-use/chat)
- [Application card: GitHub Copilot inline suggestions — GitHub Docs](https://docs.github.com/en/copilot/responsible-use/inline-suggestions)
