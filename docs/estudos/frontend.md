# Estudo — Frontend

## Introdução

O desenvolvimento frontend é a área da programação responsável por tudo aquilo que o usuário vê e interage diretamente em um site ou aplicação web. Isso envolve a criação de elementos como layout, cores, botões, formulários, animações, responsividade e a experiência do usuário.

Este documento reune os principais conceitos sobre  **componentes** , **estado**, e **renderização** , com exemplos e comparações entre frameworks mais usados no mercado.

## 1. Componentes

Um **componente** é uma unidade independente e reutilizável da interface. Em vez de construir uma página inteira em um único arquivo, o ideal é dividir a tela em blocos menores, cada um com sua própria responsabilidade.

Cada componente:
- Tem sua própria estrutura (HTML/JSK) 
- Tem seu próprio estilo (CSS)
- Pode ter sua própria lógica (JavaScript/TypeScript)
- Pode ser reutilizado em várias partes da aplicação

### Exemplo:

Um componente `Botao` pode ser utulizado em uma tela de login, em um formulário de cadastro e em uma página de configurações mantendo
o mesmo visual e comportamento.

### Exemplo prático
Em React, um componente é uma função que retorna JSX (uma sintaxe parecida com HTML):

```jsx
function Botao({ texto, onClick }) {
  return (
    <button className="botao" onClick={onClick}>
      {texto}
    </button>
  );
}
```
Esse componente Botao pode ser usado assim:

```jsx
<Botao texto="Salvar" onClick={salvar} />
<Botao texto="Cancelar" onClick={cancelar} />
```

Sempre com o mesmo visual e comportamento, mas com textos e ações diferentes.


### Vantagens 

- **Reutilização:**  escreve uma vez, usa em vários lugares
- **Organização:** o código fica dividido em blocos menores e mais fáceis de entender 
- **Manutenção:** alterações em um componente podem ser feitas em um lugar só sem precisar modificar cada parte da aplicação individualmente

- **Composição:** componentes podem ser combinados para formar componentes maiores

- **Isolamento:** mudanças em um componente não afetam os outros diretamente


## 2. Estado

O **estado** é a informação que pode mudar ao longo do tempo dentro de um
componente ou da aplicação. Quando o estado muda, a interface reage e se
atualiza automaticamente.

**Exemplos de estado:**
- O texto digitado em um campo de busca
- Se um menu está aberto ou fechado
- Os itens dentro de um carrinho de compras
- Se o usuário está logado ou não
- O resultado de uma requisição à API

### Estado vs. Props

| Conceito | O que é | Pode mudar? |
|----------|---------|-------------|
| **Props** | Dados passados de um componente pai para um filho |  Não (são somente leitura) |
| **Estado** | Dados que pertencem ao próprio componente | Sim |

### Por que o estado importa

Sem estado, a interface seria estática, sempre mostrando a mesma coisa.
O estado é o que torna a aplicação **interativa** e **dinâmica**.

## 3. Renderização

A **renderização** é o processo de transformar dados e estado em elementos visuais na tela. É o que faz o usuário ver o resultado do que está acontecendo na aplicação.

### O que significa renderizar

Renderizar é, basicamente, **mostrar na tela**. Quando você tem dados (uma lista de receitas, o nome de um usuário, o texto de um botão) e esses dados aparecem para o usuário, isso é a renderização acontecendo.

Uma analogia simples: é como imprimir um documento. Você escreve o texto no Word (os dados) e aperta Ctrl + P (a renderização). O papel que sai da impressora é o que o usuário vê (a tela).

Sem renderização, os dados existiriam apenas na memória do computador, mas o usuário não veria nada.

### Tipos de renderização

Existem duas formas principais de renderizar uma interface: a **imperativa** e a **declarativa**.

### Renderização imperativa

Na renderização imperativa, o programador diz **passo a passo** o que o navegador deve fazer. É o estilo usado com JavaScript puro e jQuery.

```javascript
// Exemplo imperativo
const botao = document.querySelector("#meuBotao");
botao.textContent = "Cliquei!";
botao.style.color = "red";
```

Traduzindo o código acima:

- "Pega o botão que tem id meuBotao"

- "Muda o texto dele para 'Cliquei!'"

- "Muda a cor dele para vermelho"

O programador está mandando o navegador fazer cada coisa, um passo por vez. Se esquecer um passo, a tela fica errada.

 Problemas da abordagem imperativa:

- Em aplicações grandes, fica difícil controlar todas as mudanças

- É fácil esquecer de atualizar algo e a interface ficar inconsistente com os dados

- O código fica cheio de comandos repetitivos

- Manutenção se torna complicada

### Renderização declarativa
Na renderização declarativa, o programador descreve como a tela deve ficar e o framework cuida de atualizar o que for necessário. É o estilo usado por ***React, Vue e Svelte.***

```jsx

// Exemplo declarativo (React)
function Botao({ clicado }) {
  return (
    <button style={{ color: clicado ? "red" : "black" }}>
      {clicado ? "Cliquei!" : "Clique aqui"}
    </button>
  );
}

```

Traduzindo o código acima:

- "Se clicado for verdadeiro, a cor é vermelha; se não, é preta"

- "Se clicado for verdadeiro, o texto é 'Cliquei!'; se não, é 'Clique aqui'"

O programador não disse "muda a cor". Ele descreveu como deve ficar. O React cuida de mudar.

### Vantagens da abordagem declarativa:

- O código fica mais limpo e fácil de entender

- O programador não precisa se preocupar com cada passo da atualização

- O framework otimiza as mudanças automaticamente

- Menos chances de erro

### Comparação entre os dois tipos

|  | **Imperativa** | **Declarativa** |
|---|---|---|
| Você diz | **Como** fazer (passo a passo) | **O que** deve aparecer |
| Quem manda | Você | O framework |
| Se errar | A tela fica errada | O framework corrige |
| Usado por | JavaScript puro, jQuery | React, Vue, Svelte |
| Código | Mais verboso | Mais enxuto |
| Manutenção | Mais difícil | Mais fácil |


### Re-renderização
Quando o estado muda, a tela precisa ser atualizada. Isso é a re-renderização.

Um exemplo prático: no Instagram, quando você clica no coração de um post:

1. estado muda de "não curtido" para "curtido"

2. O React percebe que o estado mudou

3. O React re-renderiza o componente

4. O coração fica vermelho

Tudo isso acontece automaticamente. Você não precisa dizer "muda a cor do coração". Você só muda o estado, e o framework faz o resto.

### Virtual DOM
Em **React e Vue**, a re-renderização é otimizada pelo Virtual DOM.

O Virtual DOM é uma cópia leve da interface, mantida na memória. Quando o estado muda, o framework:

1. Cria uma nova versão do Virtual DOM com as mudanças

2. Compara com a versão anterior (processo chamado diffing)

3. Descobre exatamente o que mudou

4. Aplica apenas essas mudanças no DOM real do navegador

Isso é muito mais rápido do que reconstruir a tela inteira toda vez.

|  | **DOM real** | **Virtual DOM** |
|---|---|---|
| O que é | A árvore de elementos que o navegador usa | Uma cópia leve em memória |
| Velocidade de leitura | Lenta | Rápida |
| Atualização | Direta, custosa | Calculada antes de aplicar |
| Usado por | JavaScript puro, jQuery | React, Vue |

## 4. Frameworks de frontend

Existem vários frameworks/bibliotecas para desenvolvimento frontend.
Os mais comuns são:

### React
- **Criado por:** Facebook (Meta)
- **Linguagem:** JavaScript/TypeScript
- **Característica principal:** componentes + JSX + Virtual DOM
- **Curva de aprendizado:** média

### Vue
- **Criado por:** Evan You
- **Linguagem:** JavaScript
- **Característica principal:** sintaxe simples, reatividade nativa
- **Curva de aprendizado:** baixa

### Angular
- **Criado por:** Google
- **Linguagem:** TypeScript
- **Característica principal:** framework completo (tudo incluso)
- **Curva de aprendizado:** alta

### Svelte
- **Criado por:** Rich Harris
- **Linguagem:** JavaScript
- **Característica principal:** compila para JS puro, sem Virtual DOM
- **Curva de aprendizado:** baixa

### Comparação

| Framework | Tipo | Linguagem | Curva | Diferencial |
|-----------|------|-----------|-------|-------------|
| React | Biblioteca | JS/TS | Média | Virtual DOM, maior comunidade |
| Vue | Framework progressivo | JS | Baixa | Fácil de aprender, reativo |
| Angular | Framework completo | TS | Alta | Solução "tudo em um" |
| Svelte | Compilador | JS | Baixa | Sem Virtual DOM, muito rápido |


## Conclusão

O frontend é responsável pela parte da aplicação que o usuário vê e usa. Os **componentes** ajudam a organizar e reutilizar o código, o **estado** permite que a tela mude conforme as ações do usuário e a **renderização** mostra essas mudanças na tela.


 Esses conceitos formam uma base importante para trabalhar com desenvolvimento frontend e entender melhor como as aplicações web modernas funcionam.

 ## Referências

- [Documentação do React](https://pt-br.react.dev/learn)
- [Documentação do Vue](https://vuejs.org/)
- [Documentação do Angular](https://angular.io/docs)
- [Documentação do Svelte](https://svelte.dev/docs)
- [MDN Web Docs](https://developer.mozilla.org/pt-BR/docs/Learn)