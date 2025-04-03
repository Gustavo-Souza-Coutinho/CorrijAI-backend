# CorrijAI - Backend

## 📌 Sobre o Projeto
O **CorrijAI** é um sistema backend desenvolvido em **Python (Flask)** para automatizar a correção de provas utilizando a API da IA **Gemini**. Este projeto faz parte de um **TCC** e tem como objetivo auxiliar professores no processo de avaliação de respostas de alunos, garantindo agilidade e precisão.

## 🚀 Tecnologias Utilizadas
- **Python 3**
- **Flask** (Microframework para desenvolvimento web)
- **SQLite** (Banco de dados leve e eficiente)
- **API Gemini** (Processamento de IA para correções automatizadas)
- **Jinja2** (Templates dinâmicos para interface básica)

## 📂 Estrutura do Projeto
```
TCC_backend/
├── app.py          # Arquivo principal da aplicação
├── db.py           # Configuração do banco de dados SQLite
├── templates/      # Arquivos HTML para renderização
├── static/         # Arquivos estáticos (CSS, JS, imagens)
├── requirements.txt # Dependências do projeto
└── README.md       # Documentação do projeto
```

## ⚙️ Instalação e Configuração

### **1️⃣ Clonar o Repositório**
```bash
git clone https://github.com/seu-usuario/CorrijAI-backend.git
cd CorrijAI-backend
```

### **2️⃣ Criar e Ativar o Ambiente Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows
```

### **3️⃣ Instalar as Dependências**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configurar o Banco de Dados**
```bash
python db.py  # Cria o banco de dados SQLite
```

### **5️⃣ Executar o Servidor**
```bash
python app.py
```
O servidor será iniciado em `http://127.0.0.1:5000/`.

## 📡 Endpoints da API
| Método | Rota        | Descrição                         |
|--------|------------|---------------------------------|
| GET    | `/`        | Página inicial                   |
| POST   | `/correcao` | Envia resposta para correção    |
| GET    | `/status`  | Verifica status do servidor     |

## 🛠 Melhorias Futuras
- Implementação de autenticação JWT para segurança.
- Melhor estruturação do banco de dados.
- Integração com Firebase para armazenamento.

## 📜 Licença
Este projeto é de código aberto e está licenciado sob a **MIT License**.

---
Desenvolvido por [Seu Nome](https://github.com/seu-usuario). 🚀

