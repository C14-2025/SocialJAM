
import pytest
from fastapi import status
from app import models_sql as models
from app.core.security import Hash


class TestUserModel:
    
    def test_create_user_success(self, db_session, sample_user_data):
        # Arrange
        user_data = sample_user_data
        
        # Act
        new_user = models.User(
            nome=user_data["nome"],
            username=user_data["username"],
            email=user_data["email"],
            senha=Hash.hashPWD(user_data["senha"])
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        
        # Assert
        assert new_user.id is not None
        assert new_user.username == user_data["username"]
        assert new_user.nome == user_data["nome"]
        assert new_user.email == user_data["email"]
        assert new_user.senha != user_data["senha"]  # Senha deve estar hashada


class TestUserAPI:
    
    def test_create_user_api_success(self, client, sample_user_data):
        # Arrange
        user_data = sample_user_data
        
        # Act
        response = client.post("/user/", json=user_data)  # Nova rota com prefixo
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["nome"] == user_data["nome"]
        assert response_data["email"] == user_data["email"]
        assert "senha" not in response_data  # Senha não deve aparecer na resposta
    
    def test_get_user_by_username(self, client, sample_user_data):
        # Arrange - Primeiro criar o usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act
        response = client.get(f"/user/{user_data['username']}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["nome"] == user_data["nome"]
        assert response_data["email"] == user_data["email"]
    
    def test_get_all_users(self, client, sample_user_data):
        # Arrange - Criar alguns usuários
        user_data1 = sample_user_data.copy()
        user_data2 = sample_user_data.copy()
        user_data2["username"] = "testuser2"
        user_data2["email"] = "test2@example.com"
        
        client.post("/user/", json=user_data1)
        client.post("/user/", json=user_data2)
        
        # Act
        response = client.get("/user/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data) >= 2
        usernames = [user["username"] for user in response_data]
        assert user_data1["username"] in usernames
        assert user_data2["username"] in usernames
    
    def test_get_all_users_requires_auth(self, client, sample_user_data):
        # Act - Tentar acessar sem autenticação
        response = client.get("/user/")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_user_requires_auth(self, client, sample_user_data):
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        update_data = {
            "username": user_data["username"],
            "nome": "Nome Atualizado",
            "email": "novo@example.com",
            "senha": "novasenha123"
        }
        
        # Act - Tentar atualizar sem autenticação
        response = client.put(f"/user/{user_data['username']}/update", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_user_requires_auth(self, client, sample_user_data):
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act - Tentar deletar sem autenticação
        response = client.delete(f"/user/{user_data['username']}/delete")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_own_user_with_auth(self, client, sample_user_data):
        # Arrange - Criar usuário e fazer login
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["senha"]
        }
        response = client.post("/auth/login", data=login_data)
        token = response.json()["access_token"]
        
        update_data = {
            "username": user_data["username"],
            "nome": "Nome Atualizado",
            "email": "novo@example.com",
            "senha": "novasenha123"
        }
        
        # Act - Atualizar com autenticação
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put(f"/user/{user_data['username']}/update", json=update_data, headers=headers)
        
        # Assert
        assert response.status_code == status.HTTP_202_ACCEPTED
    
    def test_delete_own_user_with_auth(self, client, sample_user_data):
        # Arrange - Criar usuário e fazer login
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["senha"]
        }
        response = client.post("/auth/login", data=login_data)
        token = response.json()["access_token"]
        
        # Act - Deletar com autenticação
        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete(f"/user/{user_data['username']}/delete", headers=headers)
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestUserValidation:
    
    def test_get_nonexistent_user_returns_404(self, client):
        # Act
        response = client.get("/user/nonexistent_user")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_user_with_invalid_email_returns_422(self, client, sample_user_data):
        # Arrange - Email inválido
        user_data = sample_user_data.copy()
        user_data["email"] = "email-invalido"  # Sem @
        
        # Act
        response = client.post("/user/", json=user_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "message" in response_data
        assert "email" in str(response_data).lower()  # Mensagem deve mencionar email
    
    def test_create_user_with_username_containing_at_symbol_returns_422(self, client, sample_user_data):
        # Arrange - Username com @
        user_data = sample_user_data.copy()
        user_data["username"] = "user@name"  # @ não permitido em username
        
        # Act
        response = client.post("/user/", json=user_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "Username não pode conter '@'" in response_data["detail"]
    
    def test_create_user_with_duplicate_username(self, client, sample_user_data):
        # Arrange
        user_data = sample_user_data
        response1 = client.post("/user/", json=user_data)  # Criar primeiro usuário
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Mudar email para evitar conflito de email único
        duplicate_user = user_data.copy()
        duplicate_user["email"] = "outro@example.com"
        
        # Act & Assert - Tentar criar outro usuário com mesmo username deve dar erro
        try:
            response = client.post("/user/", json=duplicate_user)
            # Se chegou aqui sem exceção, deve ter retornado erro HTTP
            assert response.status_code >= 400, f"Esperado erro, mas got {response.status_code}"
        except Exception as e:
            # IntegrityError é esperado - teste passou
            assert "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(e)
    
    def test_create_user_with_duplicate_email(self, client, sample_user_data):
        # Arrange
        user_data = sample_user_data
        response1 = client.post("/user/", json=user_data)  # Criar primeiro usuário
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Mudar username para evitar conflito de username único
        duplicate_user = user_data.copy()
        duplicate_user["username"] = "outronome"
        
        # Act & Assert - Tentar criar outro usuário com mesmo email deve dar erro
        try:
            response = client.post("/user/", json=duplicate_user)
            # Se chegou aqui sem exceção, deve ter retornado erro HTTP
            assert response.status_code >= 400, f"Esperado erro, mas got {response.status_code}"
        except Exception as e:
            # IntegrityError é esperado - teste passou
            assert "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(e)


class TestLoginSchema:
    
    def test_login_with_valid_email_format(self, client):
        # Arrange
        login_data = {
            "username_email": "user@example.com",
            "senha": "password123"
        }
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert - Endpoint deve aceitar o formato (mesmo que não implemente lógica ainda)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_401_UNAUTHORIZED]
    
    def test_login_with_username_format(self, client):
        # Arrange
        login_data = {
            "username_email": "testuser",  # Sem @
            "senha": "password123"
        }
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert - Endpoint deve aceitar o formato (mesmo que não implemente lógica ainda)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_401_UNAUTHORIZED]