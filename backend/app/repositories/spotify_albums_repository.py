from sqlalchemy.orm import Session
from ..models_sql import Artist
from ..services.spotify_auth_service import SpotifyAuthService
from typing import List, Dict, Any


def get_all_albums_from_artists(db: Session) -> List[Dict[str, Any]]:
    artists = db.query(Artist).all()
    
    if not artists:
        return []
    
    auth_service = SpotifyAuthService()
    
    result = []
    
    for artist in artists:
        try:
            spotify_data = auth_service.get_artist_albums(artist.nome)
            
            if spotify_data and "albums" in spotify_data:
                for album in spotify_data["albums"]:
                    result.append({
                        "artist_id": artist.id,
                        "artist_name": artist.nome,
                        "artist_genre": artist.music_genre,
                        "album_name": album.get("name"),
                        "release_date": album.get("release_date"),
                        "total_tracks": album.get("total_tracks"),
                        "image": album.get("image")
                    })
        except Exception as e:
            print(f"Erro ao buscar álbuns do artista {artist.nome} no Spotify: {str(e)}")
    
    return result