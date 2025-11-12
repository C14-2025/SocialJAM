from sqlalchemy.orm import Session
from .. import models_sql
from typing import Dict, List

def sync_top_artists(spotify_artists_data: Dict, db: Session):
    """
    Sincroniza os artistas mais ouvidos do Spotify com o banco de dados.
    Se o artista já existe, atualiza suas informações.
    Se é novo, cria um novo registro.
    
    Args:
        spotify_artists_data: Dados retornados pela API do Spotify contendo os artistas
        db: Sessão do banco de dados
    
    Returns:
        Lista de artistas sincronizados
    """
    synced_artists = []
    
    if "items" in spotify_artists_data:
        for artist_data in spotify_artists_data["items"]:
            artist_name = artist_data.get("name")
            genres = artist_data.get("genres", [])
            # Pega o primeiro gênero ou define como "Unknown"
            music_genre = genres[0] if genres else "Unknown"
            
            # Procura se o artista já existe
            existing_artist = db.query(models_sql.Artist).filter(
                models_sql.Artist.nome == artist_name
            ).first()
            
            if existing_artist:
                # Atualiza o artista existente
                existing_artist.music_genre = music_genre
                db.commit()
                db.refresh(existing_artist)
                synced_artists.append(existing_artist)
            else:
                # Cria um novo artista
                new_artist = models_sql.Artist(
                    nome=artist_name,
                    music_genre=music_genre
                )
                db.add(new_artist)
                db.commit()
                db.refresh(new_artist)
                synced_artists.append(new_artist)
    
    return synced_artists
