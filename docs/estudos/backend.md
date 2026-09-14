# Fundamentos de Backend e APIs

## 1. Backend

Backend é a parte da aplicação responsável por:

- Processar regras de negócio;
- Acessar e alterar dados no banco;
- Autenticar usuários;
- Receber requisições e enviar respostas.

O **frontend** é a interface do usuário, enquanto o backend processa as operações.

## 2. API

API significa *Application Programming Interface*. É uma forma padronizada de comunicação entre aplicações.

Exemplo:

```http
GET /produtos
```

A API recebe a requisição e pode responder com dados em JSON:

```json
[
  {
    "id": 1,
    "nome": "Teclado",
    "preco": 120
  }
]
```

## 3. API REST

REST é um estilo arquitetural usado para construir APIs utilizando recursos e métodos HTTP.

Principais características:

- Recursos são representados por URLs;
- Comunicação geralmente ocorre por HTTP;
- Dados são frequentemente enviados em JSON;
- Cada requisição deve conter as informações necessárias;
- Cliente e servidor possuem responsabilidades separadas.

## 4. Endpoints

Um endpoint é um endereço da API associado a um método HTTP.

| Método | Endpoint | Função |
|---|---|---|
| GET | `/usuarios` | Listar usuários |
| GET | `/usuarios/1` | Consultar usuário |
| POST | `/usuarios` | Criar usuário |
| PUT | `/usuarios/1` | Substituir usuário |
| PATCH | `/usuarios/1` | Alterar parte do usuário |
| DELETE | `/usuarios/1` | Excluir usuário |

## 5. Requisição HTTP

Uma requisição pode conter:

- **Método:** GET, POST, PUT, PATCH ou DELETE;
- **URL:** endereço do recurso;
- **Headers:** informações adicionais;
- **Parâmetros:** valores na URL;
- **Body:** dados enviados ao servidor.

Exemplo:

```http
POST /usuarios
Content-Type: application/json
```

```json
{
  "nome": "Gabriel",
  "email": "gabriel@email.com"
}
```

## 6. Resposta HTTP

Uma resposta normalmente contém um código de status, headers e, opcionalmente, um corpo.

Principais códigos:

| Código | Significado |
|---|---|
| 200 | Sucesso |
| 201 | Recurso criado |
| 204 | Sucesso sem conteúdo |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## 7. Frameworks de backend

Frameworks oferecem ferramentas prontas para criar servidores e APIs.

| Framework | Linguagem | Característica principal |
|---|---|---|
| Express | JavaScript/TypeScript | Simples e flexível |
| NestJS | TypeScript | Estruturado e modular |
| FastAPI | Python | APIs rápidas e documentação automática |
| Django | Python | Completo, com vários recursos integrados |
| Spring Boot | Java | Muito usado em sistemas corporativos |
| ASP.NET Core | C# | Integração com o ecossistema .NET |
| Laravel | PHP | Produtividade no desenvolvimento web |

A escolha depende da linguagem, do projeto e da experiência da equipe.

## 8. Conceitos importantes

- **Rota:** associa uma URL e um método a uma função.
- **Middleware:** executa tarefas entre a requisição e a resposta.
- **Controller:** recebe a requisição e prepara a resposta.
- **Service:** concentra as regras de negócio.
- **Banco de dados:** armazena as informações da aplicação.
- **Autenticação:** verifica quem é o usuário.
- **Autorização:** verifica o que o usuário pode fazer.
- **JSON:** formato comum para troca de dados.
- **Swagger/OpenAPI:** ferramentas para descrever e documentar APIs.

## 9. Boas práticas

- Usar nomes claros nos endpoints;
- Escolher corretamente os métodos HTTP;
- Validar os dados recebidos;
- Retornar códigos HTTP adequados;
- Proteger informações sensíveis;
- Separar controllers, services e acesso ao banco;
- Documentar e testar a API.

## Conclusão

Backend processa as regras da aplicação e se comunica com o frontend por meio de APIs. APIs REST utilizam recursos, URLs e métodos HTTP para realizar operações. Frameworks como Express, FastAPI e Spring Boot facilitam a construção dessas aplicações.
