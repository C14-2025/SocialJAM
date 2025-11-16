from fastapi import APIRouter, Depends, HTTPException, status, Query
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
        return RedirectResponse(url=auth_url, status_code=302)
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
        
        # Redirecionar para a página de origem
        frontend_url = redirect_url if redirect_url and redirect_url != "/" else "http://localhost:5173"
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
        
        sync_top_artists(top_artists_data, db)
        
        return show_all_artists(db)
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
