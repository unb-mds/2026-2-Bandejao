# Estudo — Frontend

## Introdução

O desenvolvimento frontend é a área da programação responsável por tudo aquilo que o usuário vê e interage diretamente em um site ou aplicação web. Isso envolve a criação de elementos como layout, cores, botões, formulários, animações, responsividade e a experiência do usuário.

Este documento reune os principais conceitos sobre  **componentes** , **estado**, e **renderização** , com exemplos e comparações entre frameworks mais usados no mercado.

## 1. Componentes

Um **componente** é uma unidade independente e reutilizável da interface. Em vez de construir uma página inteira em um único arquivo, o ideal é dividir a tela em blocos menores, cada um com sua própria responsibilidade.

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
- **Manutenção:** alterações em um componente podem ser feitas sem precisar modificar cada parte da aplicação individualmente

- **Composição:** componentes podem ser combinados para formar componentes maiores

- **Isolamento:** mudanças em um componente não afetam os outros diretamente

