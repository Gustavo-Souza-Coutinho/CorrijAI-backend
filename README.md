# CorrijAI-backend

CorrijAI é uma aplicação moderna e eficiente que utiliza inteligência artificial para corrigir textos, fornecer feedback e melhorar a escrita. Este projeto foi desenvolvido com foco em usabilidade, performance e escalabilidade.

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
  - [Arquivos Principais](#arquivos-principais)
- [Dependências](#dependencias)
- [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
- [Endpoints da API](#endpoints-da-api)
  - [Gerenciamento de Usuários](#gerenciamento-de-usuarios)
  - [Gerenciamento de Perguntas](#gerenciamento-de-perguntas)
  - [Gerenciamento de Respostas](#gerenciamento-de-respostas)
  - [Gerenciamento de Notas](#gerenciamento-de-notas)
- [Como Funciona](#como-funciona)
- [Executando a Aplicação](#executando-a-aplicacao)
- [Considerações de Segurança](#consideracoes-de-seguranca)
- [Melhorias Futuras](#melhorias-futuras)
- [Agradecimentos](#agradecimentos)
- [Contato](#contato)

---

## Funcionalidades

- **Gerenciamento de Usuários**: Suporte ao cadastro e login de dois tipos de usuários: Professores (`P`) e Alunos (`A`).
- **Gerenciamento de Perguntas**: Professores podem criar, atualizar, excluir e listar perguntas.
- **Gerenciamento de Respostas**: Alunos podem enviar respostas às perguntas, que são armazenadas e associadas às suas contas.
- **Correção Automatizada**: Integração com a API Gemini para correção automatizada e feedback das respostas dos alunos.
- **Integração com Banco de Dados**: Utiliza SQLite para armazenamento persistente de usuários, perguntas, respostas e notas.
- **API RESTful**: Disponibiliza um conjunto de endpoints para interação com o sistema.
- **CORS (Cross-Origin Resource Sharing)**: Habilitado para permitir que aplicações frontend interajam com o backend.

---

## Estrutura do Projeto

```
CorrijAI-backend/
├── .gitattributes
├── .idea/
├── app.py
├── db.py
├── pubspec.yaml
├── README.md
└── templates/
    └── index.html
```

### Arquivos Principais

- **`app.py`**: Arquivo principal da aplicação contendo todas as rotas e lógica da API Flask.
- **`db.py`**: Responsável pelas operações no banco de dados, incluindo criação de tabelas e operações CRUD.
- **`templates/index.html`**: Template HTML simples para a página de login.
- **`pubspec.yaml`**: Especifica as dependências do projeto.

---

## Dependências

O projeto utiliza as seguintes dependências:

- **Python 3.12**
- **Flask**
- **Flask-CORS**
- **SQLite**
- **google-generativeai**

Para instalar, execute:

```bash
pip install flask flask-cors google-generativeai
```

---

## Estrutura do Banco de Dados

A aplicação utiliza SQLite com as seguintes tabelas:

1. **`usuario`**
2. **`pergunta`**
3. **`resposta`**
4. **`nota_aluno`**

---

## Endpoints da API

### Gerenciamento de Usuários

- **`POST /cadastrar_usuario`**
- **`POST /login`**

### Gerenciamento de Perguntas

- **`GET /perguntas`**
- **`POST /perguntas`**
- **`PUT /perguntas/<int:id>`**
- **`DELETE /perguntas/<int:id>`**

### Gerenciamento de Respostas

- **`GET /alunos_respostas`**
- **`POST /corrigir`**

### Gerenciamento de Notas

- **`GET /alunos_notas`**

---

## Como Funciona

1. **Cadastro e Login de Usuários**
2. **Gerenciamento de Perguntas**
3. **Envio de Respostas**
4. **Correção Automatizada**
5. **Consulta de Notas**

---

## Executando a Aplicação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/CorrijAI-backend.git
cd CorrijAI-backend
```

2. Instale as dependências:

```bash
pip install flask flask-cors google-generativeai
```

3. Execute a aplicação:

```bash
python app.py
```

4. Acesse em `http://localhost:5000`.

---

## Considerações de Segurança

- **Chave da API** deve ser armazenada em variáveis de ambiente.
- **Armazenamento de Senhas** deve usar hashing (ex.: bcrypt).

---

## Melhorias Futuras

- Implementar autenticação JWT.
- Adicionar integração com frontend.
- Melhorar tratamento de erros e logging.
- Utilizar PostgreSQL para escalabilidade.

---

## Agradecimentos

- [Documentação do Flask](https://flask.palletsprojects.com/)
- [Documentação do SQLite](https://sqlite.org/docs.html)
- [Google Generative AI](https://developers.generativeai.google/)

---

## Contato

- **Email**: gustavo.couty@hotmail.com
- **GitHub**: [Gustavo de Souza Coutinho](https://github.com/Gustavo-Souza-Coutinho)

---

Obrigado por conferir o **CorrijAI Backend**!
