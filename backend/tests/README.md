# Testes Unitários - SocialJAM Backend

Este diretório contém testes unitários abrangentes para o backend do projeto SocialJAM, cobrindo as funcionalidades das entidades **Album**, **User**, **Artist** e repositórios **Posts** e **Comments** (MongoDB).

## Estrutura dos Testes

### 📁 Arquivos Criados

```
tests/
├── __init__.py                    # Pacote Python
├── conftest.py                    # Configurações e fixtures compartilhadas
├── test_album.py                  # 3 testes principais + 2 adicionais para Album
├── test_user.py                   # 3 testes principais + 2 adicionais para User
├── test_artist.py                 # 3 testes principais + 2 adicionais para Artist
├── test_posts_repository.py       # 7 testes para repositório de posts (MongoDB)
└── test_comments_repository.py    # 13 testes para repositório de comentários (MongoDB)
```

## Testes Implementados

### 💿 Album (test_album.py)
1. **test_create_album_success** - Criação bem-sucedida de álbum no modelo
2. **test_create_album_api_success** - Criação de álbum via API
3. **test_get_album_by_name** - Buscar álbum por nome
4. **test_get_nonexistent_album_returns_404** - Buscar álbum inexistente (404)
5. **test_album_artist_relationship** - Relacionamento entre artista e álbuns

### 👤 User (test_user.py)
1. **test_create_user_success** - Criação bem-sucedida de usuário no modelo
2. **test_create_user_api_success** - Criação de usuário via API
3. **test_get_user_by_username** - Buscar usuário por username
4. **test_get_nonexistent_user_returns_404** - Buscar usuário inexistente (404)
5. **test_create_user_with_duplicate_username** - Validação de username único

### 🎵 Artist (test_artist.py)  
1. **test_create_artist_success** - Criação bem-sucedida de artista no modelo
2. **test_create_artist_api_success** - Criação de artista via API
3. **test_get_artist_by_name** - Buscar artista por nome
4. **test_get_nonexistent_artist_returns_404** - Buscar artista inexistente (404)
5. **test_get_all_artists** - Listar todos os artistas

### 📝 Posts Repository (test_posts_repository.py)
1. **test_get_post_by_id_found** - Buscar post por ID (encontrado)
2. **test_get_post_by_id_not_found** - Buscar post por ID (não encontrado)
3. **test_get_post_by_id_invalidID** - Buscar post com ID inválido
4. **test_create_post** - Criar post
5. **test_creat_post_invalid_id** - Criar post com ID inválido
6. **test_like_post_invalid_id** - Curtir post com ID inválido
7. **test_delete_post_invalid_id** - Deletar post com ID inválido

### 💬 Comments Repository (test_comments_repository.py)
1. **test_create_comment** - Criar comentário
2. **test_create_comment_with_wrong_ids** - Criar comentário com IDs inválidos
3. **test_get_comment_by_id** - Buscar comentário por ID
4. **test_get_comment_by_id_comment_not_found** - Buscar comentário não encontrado
5. **test_get_comment_by_id_wrong_id** - Buscar comentário com ID inválido
6. **test_like_comment_not_found** - Curtir comentário não encontrado
7. **test_like_comment_invalid_ids** - Curtir comentário com IDs inválidos
8. **test_get_post_comments** - Buscar comentários de um post
9. **test_get_post_comments_wrong_id** - Buscar comentários com ID de post inválido
10. **test_delete_comment_not_found** - Deletar comentário não encontrado (primeira versão)
11. **test_delete_comment_not_found** - Deletar comentário não encontrado (segunda versão)
12. **test_on_post_deleted** - Ações quando post é deletado
13. **test_on_post_deleted_wrong_id** - Ações quando post é deletado com ID inválido

## Como Executar

### Pré-requisitos
- Python 3.13+
- uv (gerenciador de dependências)

### Comandos

```bash
# Navegar para o diretório do backend
cd backend

# Instalar dependências
uv sync

# Executar todos os testes
uv run pytest tests/ -v

# Executar testes específicos
uv run pytest tests/test_user.py -v
uv run pytest tests/test_artist.py -v
uv run pytest tests/test_album.py -v
uv run pytest tests/test_posts_repository.py -v
uv run pytest tests/test_comments_repository.py -v

# Executar com coverage
uv run pytest tests/ --cov=app --cov-report=html
```

## Características dos Testes

### 🛠️ Configuração (conftest.py)
- **Banco de dados de teste em memória** (SQLite)
- **Fixtures reutilizáveis** para dados de exemplo
- **Cliente de teste FastAPI** configurado
- **Isolamento entre testes** (cada teste tem sua própria sessão de banco)
- **Mocks para MongoDB** (testes de repositórios Posts e Comments)

### ✅ Cobertura de Funcionalidades
- **Modelos SQLAlchemy**: Criação e validação de entidades
- **APIs REST**: Endpoints de criação, busca e listagem
- **Relacionamentos**: Associações entre Artist e Album
- **Validações**: Constraints de unicidade e dados obrigatórios
- **Tratamento de Erros**: Casos de erro 404 e validação
- **Repositórios MongoDB**: Operações CRUD para Posts e Comments
- **Mocking Avançado**: Testes unitários com mocks para MongoDB
- **Testes Assíncronos**: Cobertura de operações assíncronas

### 🎯 Boas Práticas
- **Arrange-Act-Assert**: Estrutura clara nos testes
- **Nomenclatura descritiva**: Nomes explicativos para cada teste
- **Dados isolados**: Cada teste usa dados independentes
- **Múltiplos cenários**: Casos de sucesso e erro
- **Documentação**: Docstrings explicativas

## Resultados

```
================================= 35 testes implementados =================================
```

A suíte de testes abrange **35 casos de teste** distribuídos em:
- **15 testes** para entidades básicas (User, Artist, Album)
- **7 testes** para repositório de posts (MongoDB)
- **13 testes** para repositório de comentários (MongoDB)

Todos os testes garantem a qualidade e confiabilidade do código backend.

## Dependências de Teste

As seguintes dependências foram utilizadas:
- `pytest` - Framework de testes
- `fastapi[all]` - Cliente de teste para APIs
- `sqlalchemy` - ORM e banco de dados de teste
- `pytest-cov` - Cobertura de código (opcional)

