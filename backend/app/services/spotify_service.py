import requests
import base64
import os
from fastapi import HTTPException, status
from typing import Optional

class SpotifyService:
    """Serviço para integração com a API do Spotify"""
    
    def __init__(self):
        # Para usar a API do Spotify, você precisará configurar essas variáveis de ambiente
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.base_url = "https://api.spotify.com/v1"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.access_token = None
    
    def _get_access_token(self) -> str:
        """Obtém token de acesso usando Client Credentials Flow"""
        if not self.client_id or not self.client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Credenciais do Spotify não configuradas"
            )
        
        # Encode client_id:client_secret em base64
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            return token_data.get("access_token")
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao obter token do Spotify: {str(e)}"
            )
    
    def get_artist_info(self, artist_id: str) -> Optional[dict]:
        """Busca informações de um artista pelo ID do Spotify"""
        
        # Para desenvolvimento: se credenciais não estão configuradas, retorna dados mockados
        if not self.client_id or not self.client_secret:
            return {
                "id": artist_id,
                "name": f"Artista Mock (ID: {artist_id[:8]})",
                "genres": ["pop", "rock"],
                "popularity": 75,
                "external_urls": {"spotify": f"https://open.spotify.com/artist/{artist_id}"}
            }
        
        if not self.access_token:
            self.access_token = self._get_access_token()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/artists/{artist_id}",
                headers=headers
            )
            
            if response.status_code == 401:  # Token expirado
                self.access_token = self._get_access_token()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.get(
                    f"{self.base_url}/artists/{artist_id}",
                    headers=headers
                )
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Artista não encontrado no Spotify"
                )
            
            response.raise_for_status()
            artist_data = response.json()
            
            return {
                "id": artist_data.get("id"),
                "name": artist_data.get("name"),
                "genres": artist_data.get("genres", []),
                "popularity": artist_data.get("popularity"),
                "external_urls": artist_data.get("external_urls", {})
            }
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar artista no Spotify: {str(e)}"
            )

# Instância global do serviço
spotify_service = SpotifyService()