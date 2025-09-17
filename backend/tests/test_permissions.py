"""
Testes para o sistema de permissões de artistas e álbuns
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import status


def test_create_artist_blocked_for_users(client: TestClient, sample_artist_data):
    """Testa que usuários comuns não podem criar artistas"""
    response = client.post("/artist/create", json=sample_artist_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Criação de artistas não permitida" in response.json()["detail"]
    assert "Spotify" in response.json()["detail"]


def test_create_album_blocked_for_users(client: TestClient, sample_album_data):
    """Testa que usuários comuns não podem criar álbuns"""
    response = client.post("/album/create", json=sample_album_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Criação de álbuns não permitida" in response.json()["detail"]
    assert "Spotify" in response.json()["detail"]


def test_create_artist_blocked_even_with_auth(client: TestClient, sample_user_data, sample_artist_data):
    """Testa que mesmo usuários autenticados não podem criar artistas"""
    # Cria e autentica usuário
    client.post("/user/", json=sample_user_data)
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Tenta criar artista com token válido
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/artist/create", json=sample_artist_data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Criação de artistas não permitida" in response.json()["detail"]


def test_create_album_blocked_even_with_auth(client: TestClient, sample_user_data, sample_album_data):
    """Testa que mesmo usuários autenticados não podem criar álbuns"""
    # Cria e autentica usuário
    client.post("/user/", json=sample_user_data)
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Tenta criar álbum com token válido
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/album/create", json=sample_album_data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Criação de álbuns não permitida" in response.json()["detail"]


def test_read_artists_still_works(client: TestClient):
    """Testa que a leitura de artistas ainda funciona"""
    # Não deve retornar erro, mesmo que não tenha artistas
    response = client.get("/artist/all")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_search_artist_by_name_still_works(client: TestClient):
    """Testa que a busca de artista por nome ainda funciona"""
    # Deve retornar 404 se não encontrar (não erro de permissão)
    response = client.get("/artist/nonexistent_artist")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Nao existe esse Artista" in response.json()["detail"]


def test_search_album_by_name_still_works(client: TestClient):
    """Testa que a busca de álbum por nome ainda funciona"""
    # Deve retornar alguma resposta (mesmo que lista vazia ou erro de não encontrado)
    response = client.get("/album/nonexistent_album")
    # Pode ser 404 (não encontrado) ou 200 (lista vazia), ambos são válidos
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


def test_permission_system_imports_correctly():
    """Testa que o sistema de permissões pode ser importado sem erro"""
    from app.core.permissions import SystemPermissions, require_system_script_for_artist_creation, require_system_script_for_album_creation
    
    # Verifica que as classes e funções existem
    assert SystemPermissions is not None
    assert require_system_script_for_artist_creation is not None
    assert require_system_script_for_album_creation is not None
    
    # Verifica que allow_system_operations retorna False (bloqueado)
    assert SystemPermissions.allow_system_operations() == False


def test_permission_exceptions_have_correct_status():
    """Testa que as exceções de permissão têm o status correto"""
    from app.core.permissions import SystemPermissions
    from fastapi import HTTPException
    
    # Testa exceção para artistas
    with pytest.raises(HTTPException) as exc_info:
        SystemPermissions.check_artist_creation_permission(is_system_script=False)
    
    assert exc_info.value.status_code == 403
    assert "artistas" in exc_info.value.detail.lower()
    
    # Testa exceção para álbuns
    with pytest.raises(HTTPException) as exc_info:
        SystemPermissions.check_album_creation_permission(is_system_script=False)
    
    assert exc_info.value.status_code == 403
    assert "álbuns" in exc_info.value.detail.lower()


def test_system_script_permission_would_work():
    """Testa que permissões funcionariam para scripts do sistema (futuro)"""
    from app.core.permissions import SystemPermissions
    
    # Testa que não gera exceção quando is_system_script=True
    try:
        SystemPermissions.check_artist_creation_permission(is_system_script=True)
        SystemPermissions.check_album_creation_permission(is_system_script=True)
        # Se chegou até aqui, não houve exceção (comportamento correto)
        assert True
    except Exception:
        # Se gerou exceção, o teste falha
        assert False, "Permissões do sistema não deveriam gerar exceção para scripts autorizados"