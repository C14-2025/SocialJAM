"""
Testes para o sistema de autenticação
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import status
import os

def test_login_with_username(client: TestClient, sample_user_data):
    """Testa login usando username"""
    # Primeiro cria o usuário
    response = client.post("/user/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Tenta fazer login com username
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_email(client: TestClient, sample_user_data):
    """Testa login usando email"""
    # Primeiro cria o usuário
    response = client.post("/user/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Tenta fazer login com email
    login_data = {
        "username": sample_user_data["email"],  # OAuth2PasswordRequestForm usa 'username' para ambos
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, sample_user_data):
    """Testa login com credenciais inválidas"""
    # Cria usuário
    response = client.post("/user/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Tenta login com senha errada
    login_data = {
        "username": sample_user_data["username"],
        "password": "senhaerrada"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_login_nonexistent_user(client: TestClient):
    """Testa login com usuário que não existe"""
    login_data = {
        "username": "usuarioinexistente",
        "password": "qualquersenha"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_protected_route_without_token(client: TestClient):
    """Testa acesso a rota protegida sem token"""
    response = client.get("/user/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route_with_token(client: TestClient, sample_user_data):
    """Testa acesso a rota protegida com token válido"""
    # Cria usuário
    response = client.post("/user/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Faz login para obter token
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Acessa rota protegida
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_protected_route_with_invalid_token(client: TestClient):
    """Testa acesso a rota protegida com token inválido"""
    headers = {"Authorization": "Bearer token_invalido"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
def authenticated_client(client: TestClient, sample_user_data):
    """Fixture que retorna um cliente autenticado"""
    # Cria usuário
    client.post("/user/", json=sample_user_data)
    
    # Faz login
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Configura headers padrão
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def test_user_can_only_update_own_profile(client: TestClient):
    """Testa que usuário só pode atualizar seu próprio perfil"""
    # Cria dois usuários
    user1_data = {
        "username": "user1",
        "nome": "User One",
        "email": "user1@example.com",
        "senha": "password123"
    }
    user2_data = {
        "username": "user2", 
        "nome": "User Two",
        "email": "user2@example.com",
        "senha": "password123"
    }
    
    client.post("/user/", json=user1_data)
    client.post("/user/", json=user2_data)
    
    # Login como user1
    login_data = {
        "username": user1_data["username"],
        "password": user1_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token1 = response.json()["access_token"]
    
    # Tenta atualizar perfil do user2 (deve falhar)
    headers = {"Authorization": f"Bearer {token1}"}
    update_data = {"nome": "Novo Nome"}
    response = client.put("/user/user2/update", json=user2_data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Você só pode atualizar sua própria conta" in response.json()["detail"]


def test_user_can_only_delete_own_profile(client: TestClient):
    """Testa que usuário só pode deletar seu próprio perfil"""
    # Cria dois usuários
    user1_data = {
        "username": "user1",
        "nome": "User One", 
        "email": "user1@example.com",
        "senha": "password123"
    }
    user2_data = {
        "username": "user2",
        "nome": "User Two",
        "email": "user2@example.com", 
        "senha": "password123"
    }
    
    client.post("/user/", json=user1_data)
    client.post("/user/", json=user2_data)
    
    # Login como user1
    login_data = {
        "username": user1_data["username"],
        "password": user1_data["senha"]
    }
    response = client.post("/auth/login", data=login_data)
    token1 = response.json()["access_token"]
    
    # Tenta deletar perfil do user2 (deve falhar)
    headers = {"Authorization": f"Bearer {token1}"}
    response = client.delete("/user/user2/delete", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Você só pode deletar sua própria conta" in response.json()["detail"]