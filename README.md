# Projeto-Integrador-UNIVESP-IV

Markdown
# 📚 Sistema de Frequência Inteligente (Extensão Sala do Futuro)

Este projeto tem como objetivo automatizar e otimizar o lançamento de frequência escolar, contando com notificações automáticas (E-mail e WhatsApp) e uma camada de inteligência preditiva para análise de riscos de faltas.

O sistema é dividido em duas partes:
- **Backend:** Desenvolvido em Python com **FastAPI**.
- **Frontend:** Desenvolvido em **React.js**.

---

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (versão 18 ou superior recomendada)
- [Python](https://www.python.org/) (versão 3.10 ou superior recomendada)

---

## 📂 Estrutura do Repositório

```text
/
├── backend/       # Código da API (FastAPI)
├── frontend/      # Interface do usuário (React)
└── README.md      # Documentação do projeto

```

### 💻 Rodando o Backend e o Frontend

```bash
# 1. Clonar o repositório
git clone [https://github.com/paaulooo/Projeto-Integrador-UNIVESP-IV.git](https://github.com/paaulooo/Projeto-Integrador-UNIVESP-IV.git)
cd Projeto-Integrador-UNIVESP-IV

# 2. Configurar e rodar o Backend
cd back_end

# Criar e ativar o ambiente virtual (Windows)
python -m venv venv
.venv\Scripts\activate

# Criar e ativar o ambiente virtual (Linux/Mac - use este se for o seu caso)
# python3 -m venv venv && source venv/bin/activate

# Instalar as dependências do Python
pip install -r requirements.txt

# Executar o servidor backend
uvicorn main:app --reload

# ------------------------------------------------------------------
# 3. Configurar e rodar o Frontend (Em um NOVO terminal)
# ------------------------------------------------------------------

# Navegar até a pasta do projeto e entrar no frontend
cd front-end

# Instalar as dependências do Node
npm install

# Executar o frontend
npm run dev
