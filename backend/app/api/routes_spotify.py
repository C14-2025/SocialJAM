from fastapi import APIRouter, Depends, HTTPException, requests, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import database, oauth2
from ..services.spotify_auth_service import SpotifyAuthService
from ..repositories.spotify_artists_repository import sync_top_artists
from ..repositories.artist import show_all_artists
from ..repositories.user import update_spotify_tokens, get_user_spotify_tokens
from ..repositories.spotify_albums_repository import get_all_albums_from_artists
from datetime import datetime
import json
import base64

router = APIRouter(prefix="/spotify", tags=["spotify"])

@router.get("/login")
async def spotify_login(
    redirect_url: str = Query(default="/"),
    current_user = Depends(oauth2.get_current_user)
):
    try:
        auth_service = SpotifyAuthService()
        state_data = {
            "user_id": current_user.id,
            "redirect_url": redirect_url
        }
        state_encoded = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
        auth_url = auth_service.get_auth_url(state=state_encoded)
        # Retornar a URL em JSON ao invés de fazer redirect
        # Isso evita problemas de CORS com o frontend
        return {"auth_url": auth_url}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/callback")
async def spotify_callback(
    code: str,
    state: str = Query(default=None),
    db: Session = Depends(database.get_db)
):
    try:
        if not state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State não fornecido"
            )
        
        try:
            state_decoded = json.loads(base64.urlsafe_b64decode(state.encode()).decode())
            user_id = state_decoded.get("user_id")
            redirect_url = state_decoded.get("redirect_url", "/")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State inválido"
            )
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID não encontrado no state"
            )
        
        auth_service = SpotifyAuthService()
        token_data = auth_service.get_access_token(code)
        
        if not token_data or not token_data.get("access_token"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao obter token de acesso do Spotify"
            )
        
        # Salvar tokens no banco de dados do usuário
        update_spotify_tokens(
            user_id=user_id,
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_at=token_data["expires_at"],
            db=db
        )
        
        # Redirecionar para a página de origem no frontend
        # Se redirect_url for relativo (/profile), construir URL completa
        if redirect_url.startswith('http'):
            frontend_url = redirect_url
        else:
            # Garantir que começa com /
            path = redirect_url if redirect_url.startswith('/') else f'/{redirect_url}'
            frontend_url = f"http://localhost:5173{path}"
        
        return RedirectResponse(url=frontend_url, status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro durante autenticação com Spotify: {str(e)}"
        )

@router.get("/top-artists")
async def get_top_artists(
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.get_current_user)
):
    try:
        auth_service = SpotifyAuthService()
        
        user_tokens = get_user_spotify_tokens(current_user.id, db)
        
        if not user_tokens or not user_tokens.get("access_token"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não autenticado com Spotify. Faça login primeiro."
            )
        
        access_token = user_tokens["access_token"]
        refresh_token = user_tokens["refresh_token"]
        expires_at = user_tokens["expires_at"]
        
        token_valid = True
        if expires_at and expires_at <= datetime.now():
            token_valid = False
        
        if not token_valid or not auth_service.validate_token(access_token):
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expirado e refresh token não disponível. Faça login novamente."
                )
            
            new_token_data = auth_service.refresh_access_token(refresh_token)
            
            if not new_token_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Falha ao renovar token. Faça login novamente com o Spotify."
                )
            
            update_spotify_tokens(
                user_id=current_user.id,
                access_token=new_token_data["access_token"],
                refresh_token=None,  
                expires_at=new_token_data["expires_at"],
                db=db
            )
            
            access_token = new_token_data["access_token"]
        
        top_artists_data = auth_service.get_top_artists(access_token, limit=50)
        
        # Sincronizar artistas no banco (para manter histórico)
        sync_top_artists(top_artists_data, db)
        
        # Formatar dados do Spotify para o frontend
        formatted_artists = []
        if "items" in top_artists_data:
            for artist in top_artists_data["items"]:
                formatted_artists.append({
                    "id": artist.get("id"),  # ID do Spotify
                    "name": artist.get("name"),
                    "followers": artist.get("followers", {}).get("total", 0),
                    "genres": artist.get("genres", []),
                    "popularity": artist.get("popularity", 0),
                    "photo": artist.get("images", [{}])[0].get("url") if artist.get("images") else None
                })
        
        return formatted_artists
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao recuperar artistas do Spotify: {str(e)}"
        )

@router.get("/albums")
async def get_all_albums(
    db: Session = Depends(database.get_db),
):
    try:
        albums = get_all_albums_from_artists(db)
        
        if not albums:
            return {
                "message": "Nenhum álbum encontrado",
                "albums": []
            }
        
        return {
            "total": len(albums),
            "albums": albums
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao recuperar álbuns: {str(e)}"
        )
 

@router.get("/search-artists")
async def search_spotify_artists(
    query: str = Query(..., min_length=1, alias="q"),
    current_user=Depends(oauth2.get_current_user)
):
    try:
        auth_service = SpotifyAuthService()
        artists = auth_service.search_artists(query=query)

        formatted_artists = []
        for artist in artists:
            formatted_artists.append({
                "id": artist.get("id"),
                "name": artist.get("name"),
                "followers": artist.get("followers", {}).get("total", 0),
                "genres": artist.get("genres", []),
                "popularity": artist.get("popularity", 0),
                "photo": artist.get("images", [{}])[0].get("url") if artist.get("images") else None
            })

        return formatted_artists
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar artistas no Spotify: {str(e)}"
        )

@router.get("/artist/{artist_id}")
async def get_artist_by_id(
    artist_id: str,
    current_user=Depends(oauth2.get_current_user)
):
    try:
        auth_service = SpotifyAuthService()
        token = auth_service.get_app_access_token()

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"https://api.spotify.com/v1/artists/%7Bartist_id%7D",
            headers=headers
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artista não encontrado no Spotify"
            )

        response.raise_for_status()
        artist = response.json()

        return {
            "id": artist.get("id"),
            "name": artist.get("name"),
            "followers": artist.get("followers", {}).get("total", 0),
            "genres": artist.get("genres", []),
            "popularity": artist.get("popularity", 0),
            "photo": artist.get("images", [{}])[0].get("url") if artist.get("images") else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar artista no Spotify: {str(e)}"
        )