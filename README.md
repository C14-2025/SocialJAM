# SocialJAM

Uma rede social focada em música, onde usuários podem compartilhar suas experiências musicais, descobrir novos artistas e álbuns, e interagir com outros amantes da música.

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido para Python
- **SQLAlchemy** - ORM para banco de dados relacional  
- **SQLite** - Banco de dados para desenvolvimento
- **MongoDB** - Banco de dados para posts e comentários
- **JWT** - Autenticação via tokens
- **Pydantic** - Validação de dados
- **pytest** - Framework de testes

### Frontend
- **React** - Biblioteca para interfaces de usuário
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS utilitário
- **JavaScript** - Linguagem principal do frontend

## 📋 Pré-requisitos

### Windows

1. **Python 3.11+**
   ```powershell
   # Baixar do site oficial python.org ou usar winget
   winget install Python.Python.3.11
   ```

2. **Node.js 18+**
   ```powershell
   # Baixar do site oficial nodejs.org ou usar winget
   winget install OpenJS.NodeJS
   ```

3. **Git**
   ```powershell
   winget install Git.Git
   ```

4. **UV (gerenciador de pacotes Python)**
   ```powershell
   pip install uv
   ```

### Linux (Ubuntu/Debian)

1. **Python 3.11+**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip
   ```

2. **Node.js 18+**
   ```bash
   # Via NodeSource
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # Ou via snap
   sudo snap install node --classic
   ```

3. **Git**
   ```bash
   sudo apt install git
   ```

4. **UV (gerenciador de pacotes Python)**
   ```bash
   pip install uv
   ```

## 🛠️ Configuração do Ambiente

### 1. Clonar o Repositório

```bash
git clone https://github.com/C14-2025/SocialJAM.git
cd SocialJAM
```

### 2. Configurar Backend

```bash
cd backend

# Instalar dependências com UV
uv sync

# Criar arquivo de variáveis de ambiente
cp .env.example .env  # Ou crie manualmente

# Configurar variáveis no .env
# SECRET_KEY=sua_chave_secreta_aqui_muito_forte
# DATABASE_URL=sqlite:///./database.db
# MONGO_URL=mongodb://localhost:27017/socialjam
```

#### Gerar SECRET_KEY (obrigatório)

**Windows (PowerShell):**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Linux/macOS:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Configurar Frontend

```bash
cd ../front

# Instalar dependências
npm install

# Ou com yarn
yarn install
```

### 4. Configurar Banco de Dados

O projeto usa SQLite para dados relacionais e MongoDB para posts. Para desenvolvimento local:

**SQLite** - Criado automaticamente na primeira execução

**MongoDB** (opcional para desenvolvimento completo):

**Windows:**
```powershell
# Instalar MongoDB Community
winget install MongoDB.Server
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

## ▶️ Executar o Projeto

### Backend (FastAPI)

```bash
cd backend

# Executar servidor de desenvolvimento
uv run python main.py

# Ou usando uvicorn diretamente
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em: http://localhost:8000
- Documentação da API: http://localhost:8000/docs
- Documentação alternativa: http://localhost:8000/redoc

### Frontend (React)

```bash
cd front

# Executar servidor de desenvolvimento
npm run dev

# Ou com yarn
yarn dev
```

O frontend estará disponível em: http://localhost:5173

## 🧪 Executar Testes

### Backend

```bash
cd backend

# Executar todos os testes
uv run pytest

# Executar com cobertura
uv run pytest --cov=app

# Executar testes específicos
uv run pytest tests/test_user.py
uv run pytest tests/test_authentication.py
```

### Frontend

```bash
cd front

# Executar testes
npm test

# Ou com yarn
yarn test
```

## 🏗️ Estrutura do Projeto

```
SocialJAM/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Rotas da API
│   │   ├── core/           # Configurações e segurança
│   │   ├── models/         # Modelos de dados
│   │   ├── repositories/   # Camada de acesso a dados
│   │   ├── services/       # Lógica de negócio
│   │   └── schemas/        # Schemas Pydantic
│   ├── tests/              # Testes automatizados
│   └── main.py            # Ponto de entrada da API
├── front/                  # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── _auth/         # Páginas de autenticação
│   │   ├── _root/         # Páginas principais
│   │   └── lib/           # Utilitários e configurações
│   └── public/            # Arquivos estáticos
└── README.md              # Este arquivo
```

## 🔐 Funcionalidades de Segurança

### Autenticação
- Login com username ou email
- Tokens JWT com expiração configurável
- Senhas hasheadas com bcrypt

### Autorização
- Usuários só podem editar/deletar seus próprios perfis
- Proteção de rotas sensíveis
- Sistema de permissões para criação de conteúdo

### Permissões Especiais
- Criação de artistas/álbuns bloqueada para usuários
- Preparado para integração futura com API do Spotify
- Sistema extensível de permissões

## 🚀 Adicionando Novas Funcionalidades

### 1. Adicionando Nova Rota da API

```python
# backend/app/api/routes_nova_feature.py
from fastapi import APIRouter, Depends
from ..oauth2 import get_current_user

router = APIRouter(prefix="/nova-feature", tags=["Nova Feature"])

@router.post("/")
def criar_nova_feature(current_user = Depends(get_current_user)):
    # Sua lógica aqui
    pass
```

### 2. Registrar Rota no Main

```python
# backend/main.py
from app.api import routes_nova_feature

app.include_router(routes_nova_feature.router)
```

### 3. Criar Testes

```python
# backend/tests/test_nova_feature.py
import pytest
from fastapi.testclient import TestClient

def test_nova_feature(client: TestClient):
    # Seus testes aqui
    pass
```

### 4. Adicionar Componente Frontend

```jsx
// front/src/components/NovaFeature.jsx
import React from 'react';

const NovaFeature = () => {
  return (
    <div>
      {/* Seu componente aqui */}
    </div>
  );
};

export default NovaFeature;
```

## 📚 Recursos Úteis

### Documentação das Tecnologias
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)

### Comandos Úteis

```bash
# Backend - Gerar requirements.txt
uv export --format requirements-txt --output requirements.txt

# Backend - Atualizar dependências
uv sync --upgrade

# Frontend - Atualizar dependências
npm update

# Git - Ver status das mudanças
git status

# Git - Fazer commit das mudanças
git add .
git commit -m "feat: sua nova funcionalidade"
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Convenções

### Commits
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, ponto e vírgula, etc
- `refactor:` refatoração de código
- `test:` adição ou correção de testes
- `chore:` mudanças em ferramentas, configs, etc

### Estrutura de Branches
- `main` - branch principal
- `develop` - branch de desenvolvimento
- `feature/*` - novas funcionalidades
- `fix/*` - correções de bugs

## ❓ Problemas Comuns

### Backend não inicia
- Verifique se o Python 3.11+ está instalado
- Confirme se o UV está instalado (`pip install uv`)
- Verifique se o arquivo `.env` existe e tem SECRET_KEY

### Frontend não carrega
- Verifique se o Node.js 18+ está instalado
- Execute `npm install` ou `yarn install`
- Confirme se o backend está rodando na porta 8000

### Testes falhando
- Verifique se todas as dependências estão instaladas
- Execute `uv run pytest -v` para ver detalhes dos erros

### Erro de permissão
- No Linux, use `sudo` se necessário para instalações globais
- Configure variáveis de ambiente corretamente

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido com ❤️ pela equipe SocialJAM**