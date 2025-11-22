
"""
Testes para funcionalidades de usuário do SocialJAM

Este módulo contém testes abrangentes para todas as funcionalidades relacionadas
a usuários, incluindo CRUD, autenticação, validações e funcionalidades avançadas
como upload de foto e integração com Spotify.
"""

import pytest
from fastapi import status
from app import models_sql as models
from app.core.security import Hash


class TestUserModel:
    """
    Testes para o modelo SQLAlchemy User
    Verifica criação e validação de dados no nível do modelo
    """
    
    def test_create_user_success(self, db_session, sample_user_data):
        """
        Mock Test: Criação bem-sucedida de usuário no banco
        
        Simula criação direta no banco de dados usando SQLAlchemy.
        Testa se o hash da senha está funcionando corretamente.
        """
        # Arrange - Preparar dados do usuário
        user_data = sample_user_data
        
        # Act - Criar usuário diretamente no banco
        new_user = models.User(
            nome=user_data["nome"],
            username=user_data["username"],
            email=user_data["email"],
            senha=Hash.hashPWD(user_data["senha"])
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        
        # Assert - Verificar se dados foram salvos corretamente
        assert new_user.id is not None
        assert new_user.username == user_data["username"]
        assert new_user.nome == user_data["nome"]
        assert new_user.email == user_data["email"]
        assert new_user.senha != user_data["senha"]  # Senha deve estar hashada


class TestUserCRUD:
    """
    Testes para operações CRUD básicas via API
    Covers: Create, Read (single/multiple), Update, Delete
    """
    
    def test_create_user_api_success(self, client, sample_user_data):
        """
        Mock Test: Criação de usuário via API
        
        Simula POST /user/ com dados válidos.
        Verifica se usuário é criado e dados retornados corretamente.
        """
        # Arrange
        user_data = sample_user_data
        
        # Act
        response = client.post("/user/", json=user_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["nome"] == user_data["nome"]
        assert response_data["email"] == user_data["email"]
        assert "senha" not in response_data  # Senha não deve aparecer na resposta
    
    def test_get_user_by_username(self, client, sample_user_data):
        """
        Mock Test: Buscar usuário por username
        
        Simula GET /user/{username} após criar usuário.
        Verifica se dados são retornados corretamente.
        """
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
    
    def test_get_user_by_id(self, client, sample_user_data):
        """
        Mock Test: Buscar usuário por ID
        
        Simula GET /user/id/{user_id} após criar usuário.
        Testa nova funcionalidade de busca por ID.
        """
        # Arrange - Criar usuário e obter ID
        user_data = sample_user_data
        create_response = client.post("/user/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Act
        response = client.get(f"/user/id/{user_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == user_id
        assert response_data["username"] == user_data["username"]


class TestUserAuthentication:
    """
    Testes para autenticação e autorização
    Covers: Login, protected routes, token validation
    """
    
    def test_get_all_users_requires_auth(self, client):
        """
        Mock Test: Listar usuários requer autenticação
        
        Simula GET /user/ sem token de autenticação.
        Verifica se retorna 401 Unauthorized.
        """
        # Act - Tentar acessar sem autenticação
        response = client.get("/user/")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_all_users_with_auth(self, client, sample_user_data):
        """
        Mock Test: Listar usuários com autenticação
        
        Simula login e depois GET /user/ com token válido.
        Verifica se lista de usuários é retornada.
        """
        # Arrange - Criar usuário e fazer login
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["senha"]
        }
        login_response = client.post("/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # Act - Acessar com autenticação
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/user/", headers=headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_get_current_user_info(self, client, sample_user_data):
        """
        Mock Test: Obter informações do usuário logado
        
        Simula GET /user/me com token válido.
        Verifica se dados do usuário atual são retornados.
        """
        # Arrange - Criar usuário e fazer login
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["senha"]
        }
        login_response = client.post("/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # Act
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/user/me", headers=headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]
    
    def test_update_user_requires_auth(self, client, sample_user_data):
        """
        Mock Test: Atualizar usuário requer autenticação
        
        Simula PUT /user/{username}/update sem token.
        Verifica se retorna 401 Unauthorized.
        """
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
    
    def test_update_own_user_with_auth(self, client, sample_user_data):
        """
        Mock Test: Atualizar próprio usuário com autenticação
        
        Simula login e PUT /user/{username}/update com token válido.
        Verifica se usuário pode atualizar seus próprios dados.
        """
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
    
    def test_cannot_update_other_user(self, client, sample_user_data):
        """
        Mock Test: Usuário não pode atualizar dados de outro usuário
        
        Simula tentativa de atualizar outro usuário.
        Verifica se retorna 403 Forbidden.
        """
        # Arrange - Criar dois usuários
        user1_data = sample_user_data
        user2_data = sample_user_data.copy()
        user2_data["username"] = "user2"
        user2_data["email"] = "user2@example.com"
        
        client.post("/user/", json=user1_data)
        client.post("/user/", json=user2_data)
        
        # Login como user1
        login_data = {
            "username": user1_data["username"],
            "password": user1_data["senha"]
        }
        response = client.post("/auth/login", data=login_data)
        token = response.json()["access_token"]
        
        # Act - Tentar atualizar user2 com token do user1
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put(f"/user/{user2_data['username']}/update", json=user2_data, headers=headers)
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_user_requires_auth(self, client, sample_user_data):
        """
        Mock Test: Deletar usuário requer autenticação
        
        Simula DELETE /user/{username}/delete sem token.
        Verifica se retorna 401 Unauthorized.
        """
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act - Tentar deletar sem autenticação
        response = client.delete(f"/user/{user_data['username']}/delete")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_own_user_with_auth(self, client, sample_user_data):
        """
        Mock Test: Deletar próprio usuário com autenticação
        
        Simula login e DELETE /user/{username}/delete com token válido.
        Verifica se usuário pode deletar sua própria conta.
        """
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
    """
    Testes para validações de entrada e regras de negócio
    Covers: Email validation, username rules, unique constraints
    """
    
    def test_get_nonexistent_user_returns_404(self, client):
        """
        Mock Test: Buscar usuário inexistente retorna 404
        
        Simula GET /user/{username} com username que não existe.
        Verifica se retorna 404 Not Found.
        """
        # Act
        response = client.get("/user/nonexistent_user")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_user_with_invalid_email_returns_422(self, client, sample_user_data):
        """
        Mock Test: Criar usuário com email inválido retorna 422
        
        Simula POST /user/ com email sem @.
        Verifica se validação Pydantic funciona corretamente.
        """
        # Arrange - Email inválido
        user_data = sample_user_data.copy()
        user_data["email"] = "email-invalido"  # Sem @
        
        # Act
        response = client.post("/user/", json=user_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_user_with_username_containing_at_symbol_returns_422(self, client, sample_user_data):
        """
        Mock Test: Username com @ é rejeitado
        
        Simula POST /user/ com @ no username.
        Testa validação customizada que impede @ no username.
        """
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
        """
        Mock Test: Username duplicado é rejeitado
        
        Simula criação de dois usuários com mesmo username.
        Testa constraint de unicidade no banco.
        """
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
        """
        Mock Test: Email duplicado é rejeitado
        
        Simula criação de dois usuários com mesmo email.
        Testa constraint de unicidade no banco.
        """
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


class TestUserAdvancedFeatures:
    """
    Testes para funcionalidades avançadas
    Covers: Search, favorite artist, profile picture, Spotify integration
    """
    
    def test_search_users_by_username_prefix(self, client, sample_user_data):
        """
        Mock Test: Buscar usuários por prefixo do username
        
        Simula GET /user/pesquisar/{input} com prefixo.
        Testa funcionalidade de busca/autocompletar usuários.
        """
        # Arrange - Criar usuários com prefixos similares
        user1_data = sample_user_data.copy()
        user1_data["username"] = "test_user1"
        user1_data["email"] = "test1@example.com"
        
        user2_data = sample_user_data.copy()
        user2_data["username"] = "test_user2"
        user2_data["email"] = "test2@example.com"
        
        user3_data = sample_user_data.copy()
        user3_data["username"] = "another_user"
        user3_data["email"] = "another@example.com"
        
        client.post("/user/", json=user1_data)
        client.post("/user/", json=user2_data)
        client.post("/user/", json=user3_data)
        
        # Act - Buscar por prefixo "test"
        response = client.get("/user/pesquisar/test")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) == 2
        usernames = [user["username"] for user in results]
        assert "test_user1" in usernames
        assert "test_user2" in usernames
        assert "another_user" not in usernames
    
    def test_set_favorite_artist_requires_auth(self, client, sample_user_data):
        """
        Mock Test: Definir artista favorito requer autenticação
        
        Simula PUT /user/me/favorite-artist sem token.
        Verifica se retorna 401 Unauthorized.
        """
        # Act - Tentar definir artista favorito sem autenticação
        artist_data = {"artist_id": "spotify_artist_id"}
        response = client.put("/user/me/favorite-artist", json=artist_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # TODO: Adicionar testes para funcionalidades que requerem mocks externos:
    # - test_set_favorite_artist_with_valid_spotify_id (requer mock do Spotify API)
    # - test_set_favorite_artist_with_invalid_spotify_id (requer mock do Spotify API)
    # - test_upload_profile_picture (requer mock de file upload)
    # - test_spotify_token_integration (requer mock da autenticação Spotify)


class TestLoginAuthentication:
    """
    Testes para sistema de login
    Covers: Login com username, login com email, token generation
    """
    
    def test_login_with_username(self, client, sample_user_data):
        """
        Mock Test: Login com username válido
        
        Simula POST /auth/login com username.
        Verifica se token é gerado corretamente.
        """
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act - Login com username
        login_data = {
            "username": user_data["username"],
            "password": user_data["senha"]
        }
        response = client.post("/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"
    
    def test_login_with_email(self, client, sample_user_data):
        """
        Mock Test: Login com email válido
        
        Simula POST /auth/login com email no campo username.
        Testa funcionalidade de login flexível (username ou email).
        """
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act - Login com email
        login_data = {
            "username": user_data["email"],  # Usando email no campo username
            "password": user_data["senha"]
        }
        response = client.post("/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
    
    def test_login_with_invalid_credentials(self, client, sample_user_data):
        """
        Mock Test: Login com credenciais inválidas
        
        Simula POST /auth/login com senha incorreta.
        Verifica se retorna 404 Not Found (por segurança).
        """
        # Arrange - Criar usuário
        user_data = sample_user_data
        client.post("/user/", json=user_data)
        
        # Act - Login com senha incorreta
        login_data = {
            "username": user_data["username"],
            "password": "senha_errada"
        }
        response = client.post("/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_login_with_nonexistent_user(self, client):
        """
        Mock Test: Login com usuário inexistente
        
        Simula POST /auth/login com username que não existe.
        Verifica se retorna 404 Not Found.
        """
        # Act - Login com usuário inexistente
        login_data = {
            "username": "usuario_inexistente",
            "password": "qualquer_senha"
        }
        response = client.post("/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND