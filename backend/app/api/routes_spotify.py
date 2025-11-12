from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import database
from ..services.spotify_auth_service import SpotifyAuthService
from ..repositories.spotify_artists_repository import sync_top_artists

router = APIRouter(prefix="/spotify", tags=["spotify"])

@router.get("/login")
async def spotify_login():
    try:
        auth_service = SpotifyAuthService()
        auth_url = auth_service.get_auth_url()
        return RedirectResponse(url=auth_url, status_code=302)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/callback")
async def spotify_callback(code: str, db: Session = Depends(database.get_db)):
    try:
        auth_service = SpotifyAuthService()
        access_token = auth_service.get_access_token(code)
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao obter token de acesso do Spotify"
            )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro durante autenticação com Spotify: {str(e)}"
        )

@router.get("/top-artists")
async def get_top_artists(access_token: str, db: Session = Depends(database.get_db)):
    try:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de acesso do Spotify é necessário"
            )
        
        auth_service = SpotifyAuthService()
        top_artists_data = auth_service.get_top_artists(access_token, limit=50)
        
        # Sincroniza os artistas com o banco de dados
        sync_top_artists(top_artists_data, db)
        
        # Retorna o JSON recebido da API do Spotify diretamente
        return top_artists_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao recuperar artistas do Spotify: {str(e)}"
        )
