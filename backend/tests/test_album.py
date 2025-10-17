import pytest
from fastapi import status
from app.models_sql import Artist, Album, User


class TestAlbumModel:

    
    def test_create_album_success(self, db_session, sample_artist_data, sample_album_data):
        artist = Artist(
            nome=sample_artist_data["nome"],
            music_genre=sample_artist_data["music_genre"]
        )
        db_session.add(artist)
        db_session.commit()
        db_session.refresh(artist)

        # Act
        new_album = Album(
            nome=sample_album_data["nome"],
            total_tracks=sample_album_data["total_tracks"],
            artist_id=artist.id
        )
        db_session.add(new_album)
        db_session.commit()
        db_session.refresh(new_album)
        

        assert new_album.id is not None
        # Assert
        assert new_album.nome == sample_album_data["nome"]
        assert new_album.total_tracks == sample_album_data["total_tracks"]
        assert new_album.artist_id == artist.id
        assert new_album.criador.nome == artist.nome  


class TestAlbumAPI:
    
    def test_create_album_api_success(self, client, sample_artist_data, sample_album_data):
    
        artist_response = client.post("/artistCreate", json=sample_artist_data)
        artist_id = artist_response.json()["id"]
        
        album_data = sample_album_data.copy()
        album_data["artist_id"] = artist_id
        

        response = client.post("/albumCreate", json=album_data)
        

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["nome"] == album_data["nome"]
        assert response_data["total_tracks"] == album_data["total_tracks"]
        assert response_data["artist_id"] == artist_id
        assert "id" in response_data
    
    def test_get_album_by_name(self, client, sample_artist_data, sample_album_data):

        artist_response = client.post("/artistCreate", json=sample_artist_data)
        artist_id = artist_response.json()["id"]
        
        album_data = sample_album_data.copy()
        album_data["artist_id"] = artist_id
        client.post("/albumCreate", json=album_data)
        

        response = client.get(f"/album/{album_data['nome']}")
        

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 1
        album = response_data[0]
        assert album["nome"] == album_data["nome"]
        assert album["total_tracks"] == album_data["total_tracks"]
        assert album["artist_id"] == artist_id


class TestAlbumValidation:

    def test_get_nonexistent_album_returns_404(self, client):


        response = client.get("/album/NonexistentAlbum")
        

        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert "Nao existe esse Album" in response_data["detail"]
    
    def test_album_artist_relationship(self, db_session, sample_artist_data):

        artist = Artist(
            nome=sample_artist_data["nome"],
            music_genre=sample_artist_data["music_genre"]
        )
        db_session.add(artist)
        db_session.commit()
        db_session.refresh(artist)
        
        album1 = Album(nome="Album 1", total_tracks=10, artist_id=artist.id)
        album2 = Album(nome="Album 2", total_tracks=12, artist_id=artist.id)
        
        db_session.add(album1)
        db_session.add(album2)
        db_session.commit()
        db_session.refresh(artist)

        assert len(artist.albums) == 2
        album_names = [album.nome for album in artist.albums]
        assert "Album 1" in album_names
        assert "Album 2" in album_names