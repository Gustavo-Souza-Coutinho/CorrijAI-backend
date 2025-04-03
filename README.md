# CorrijAI-backend

CorrijAI-backend é uma aplicação backend desenvolvida em Python utilizando Flask e SQLite. Ela foi projetada para gerenciar o cadastro de usuários, lidar com perguntas e respostas, e integrar-se com a API Gemini para correção automatizada e feedback. Este projeto é ideal para plataformas educacionais que necessitam de avaliação automatizada das respostas dos alunos.

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
│   ├── .gitignore
│   ├── inspectionProfiles/
│   │   └── profiles_settings.xml
│   ├── misc.xml
│   ├── modules.xml
│   ├── workspace (2).xml
│   └── xdxd.iml
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
- **`.idea/`**: Contém arquivos de configuração específicos do IDE (ex.: PyCharm).

---

## Dependências

O projeto utiliza as seguintes dependências:

- **Python 3.12**: Linguagem de programação principal.
- **Flask**: Framework web leve para aplicações WSGI.
- **Flask-CORS**: Habilita o compartilhamento de recursos entre origens diferentes (CORS).
- **SQLite**: Banco de dados leve baseado em arquivos.
- **google-generativeai**: Para integração com a API Gemini.
- **http**: Dependência especificada no `pubspec.yaml` para requisições HTTP.

Para instalar as dependências necessárias do Python, execute:

```bash
pip install flask flask-cors google-generativeai
```

---

## Estrutura do Banco de Dados

A aplicação utiliza SQLite com as seguintes tabelas:

1. **`usuario`**: Armazena informações dos usuários.
   - `id`: Chave primária.
   - `nome`: Nome do usuário.
   - `email`: E-mail do usuário (único).
   - `senha`: Senha do usuário.
   - `flg_tipo`: Tipo de usuário (`P` para Professor, `A` para Aluno).

2. **`pergunta`**: Armazena as perguntas.
   - `id`: Chave primária.
   - `texto`: Texto da pergunta.

3. **`resposta`**: Armazena as respostas dos alunos.
   - `id`: Chave primária.
   - `id_pergunta`: Chave estrangeira referenciando `pergunta`.
   - `id_aluno`: Chave estrangeira referenciando `usuario`.
   - `resposta`: Texto da resposta.

4. **`nota_aluno`**: Armazena as notas e feedbacks.
   - `id`: Chave primária.
   - `id_aluno`: Chave estrangeira referenciando `usuario`.
   - `nota`: Nota como porcentagem inteira.
   - `respostas_corrigidas`: Texto com o feedback.
   - `data_avaliacao`: Data e hora da avaliação.

---

## Endpoints da API

### Gerenciamento de Usuários

- **`POST /cadastrar_usuario`**: Cadastra um novo usuário.
- **`POST /login`**: Autentica um usuário.

### Gerenciamento de Perguntas

- **`GET /perguntas`**: Lista todas as perguntas.
- **`POST /perguntas`**: Adiciona uma nova pergunta.
- **`PUT /perguntas/<int:id>`**: Atualiza uma pergunta.
- **`DELETE /perguntas/<int:id>`**: Exclui uma pergunta.

### Gerenciamento de Respostas

- **`GET /alunos_respostas`**: Lista as respostas de um aluno específico.
- **`POST /corrigir`**: Envia respostas para correção automatizada.

### Gerenciamento de Notas

- **`GET /alunos_notas`**: Lista as notas de todos os alunos.

---

## Como Funciona

1. **Cadastro e Login de Usuários**:
   - Usuários podem se cadastrar como Professor ou Aluno.
   - As credenciais de login são validadas no banco de dados.

2. **Gerenciamento de Perguntas**:
   - Professores podem criar, atualizar e excluir perguntas.
   - As perguntas são armazenadas na tabela `pergunta`.

3. **Envio de Respostas**:
   - Alunos enviam respostas às perguntas.
   - As respostas são armazenadas na tabela `resposta`.

4. **Correção Automatizada**:
   - O endpoint `/corrigir` envia perguntas e respostas para a API Gemini.
   - A API retorna feedback e uma nota, que são armazenados na tabela `nota_aluno`.

5. **Consulta de Notas**:
   - Professores podem visualizar as notas de todos os alunos.
   - Alunos podem visualizar suas próprias notas e feedbacks.

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

4. Acesse a aplicação em `http://localhost:5000`.

---

## Considerações de Segurança

- **Chave da API**: A chave da API Gemini está hardcoded no arquivo `app.py`. Para produção, considere usar variáveis de ambiente para armazenar informações sensíveis.
- **Armazenamento de Senhas**: As senhas são armazenadas em texto puro. Implemente hashing (ex.: bcrypt) para maior segurança.

---

## Melhorias Futuras

- Implementar autenticação de usuários com JWT.
- Adicionar integração com frontend para uma experiência completa.
- Melhorar o tratamento de erros e o logging.
- Utilizar um sistema de banco de dados mais robusto (ex.: PostgreSQL) para escalabilidade.

---

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Agradecimentos

- [Documentação do Flask](https://flask.palletsprojects.com/)
- [Documentação do SQLite](https://sqlite.org/docs.html)
- [Google Generative AI](https://developers.generativeai.google/)
