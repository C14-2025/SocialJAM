"""
Testes unitários para funcionalidades do artista (Artist)
"""
import pytest
from fastapi import status
from app.models_sql import Artist, Album, User


class TestArtistModel:
    """Testes para o modelo Artist"""
    
    def test_create_artist_success(self, db_session, sample_artist_data):
        """Teste 4: Criação bem-sucedida de artista"""
        # Arrange
        artist_data = sample_artist_data
        
        # Act
        new_artist = Artist(
            nome=artist_data["nome"],
            music_genre=artist_data["music_genre"]
        )
        db_session.add(new_artist)
        db_session.commit()
        db_session.refresh(new_artist)
        
        # Assert
        assert new_artist.id is not None
        assert new_artist.nome == artist_data["nome"]
        assert new_artist.music_genre == artist_data["music_genre"]
        assert new_artist.albums == []  # Lista de álbuns deve estar vazia inicialmente


class TestArtistAPI:
    """Testes para as rotas da API de artistas"""
    
    def test_create_artist_api_success(self, client, sample_artist_data):
        """Teste 5: Criação de artista via API"""
        # Arrange
        artist_data = sample_artist_data
        
        # Act
        response = client.post("/artistCreate", json=artist_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["nome"] == artist_data["nome"]
        assert response_data["music_genre"] == artist_data["music_genre"]
        assert "id" in response_data
    
    def test_get_artist_by_name(self, client, sample_artist_data):
        """Teste 6: Buscar artista por nome"""
        # Arrange - Primeiro criar o artista
        artist_data = sample_artist_data
        client.post("/artistCreate", json=artist_data)
        
        # Act
        response = client.get(f"/artist/{artist_data['nome']}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 1
        artist = response_data[0]
        assert artist["nome"] == artist_data["nome"]
        assert artist["music_genre"] == artist_data["music_genre"]


class TestArtistValidation:
    """Testes de validação e casos de erro para artistas"""
    
    def test_get_nonexistent_artist_returns_404(self, client):
        """Teste adicional: Buscar artista inexistente deve retornar 404"""
        # Act
        response = client.get("/artist/NonexistentArtist")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert "Nao existe esse Artista" in response_data["detail"]
    
    def test_get_all_artists(self, client, sample_artist_data):
        """Teste adicional: Listar todos os artistas"""
        # Arrange - Criar alguns artistas
        artist1_data = sample_artist_data
        artist2_data = {
            "nome": "Second Artist", 
            "music_genre": "Pop"
        }
        
        client.post("/artistCreate", json=artist1_data)
        client.post("/artistCreate", json=artist2_data)
        
        # Act
        response = client.get("/artistAll")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 2
        artist_names = [artist["nome"] for artist in response_data]
        assert artist1_data["nome"] in artist_names
        assert artist2_data["nome"] in artist_names