# Sistema de Permissões para Criação de Artistas e Álbuns

## Situação Atual

As rotas de criação de artistas (`/artist/create`) e álbuns (`/album/create`) estão **bloqueadas** para usuários comuns. Qualquer tentativa de criação retornará erro `403 Forbidden`.

## Como Funciona

1. **Módulo de Permissões**: `app/core/permissions.py`
   - Contém a classe `SystemPermissions` que gerencia as permissões
   - Função `allow_system_operations()` sempre retorna `False` (bloqueia tudo)

2. **Dependências nas Rotas**:
   - `require_system_script_for_artist_creation()` - bloqueia criação de artistas
   - `require_system_script_for_album_creation()` - bloqueia criação de álbuns

## Para Implementar o Script do Spotify (Futuro)

### Opção 1: Header Especial
Modifique `allow_system_operations()` em `permissions.py`:

```python
from fastapi import Request, Depends

def get_request():
    # Injeção de dependência para acessar o request
    pass

@staticmethod
def allow_system_operations(request: Request = Depends(get_request)):
    # Verificar header especial do script do Spotify
    return request.headers.get("X-System-Script") == "spotify-importer"
```

### Opção 2: API Key Especial
```python
import os

@staticmethod
def allow_system_operations(api_key: str = None):
    system_api_key = os.getenv("SPOTIFY_SCRIPT_API_KEY")
    return api_key == system_api_key and system_api_key is not None
```

### Opção 3: Rota Interna Separada
Criar rotas separadas apenas para o script:

```python
# Novas rotas em routes_internal.py
@router.post('/internal/artist/create')
def create_artist_internal(request: schemas.Artist, api_key: str):
    # Verificar API key do sistema
    if not verify_system_api_key(api_key):
        raise HTTPException(403, "Unauthorized")
    # Criar artista...
```

## Testando o Bloqueio

Para testar se está funcionando, tente fazer uma requisição POST para:
- `http://localhost:8000/artist/create`
- `http://localhost:8000/album/create`

Ambas devem retornar erro `403 Forbidden` com a mensagem explicando que a operação não é permitida.

## Vantagens desta Implementação

1. **Flexível**: Fácil de modificar quando implementar o script
2. **Seguro**: Bloqueia completamente a criação manual
3. **Organizado**: Lógica de permissões centralizada
4. **Extensível**: Pode ser usado para outras operações no futuro