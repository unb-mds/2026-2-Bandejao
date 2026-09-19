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
