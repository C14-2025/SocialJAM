import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

class SpotifyAuthService:
    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.redirect_uri = SPOTIFY_REDIRECT_URI
        
        if not self.client_id or not self.client_secret:
            raise ValueError("SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET não estão configurados no .env")
    
    def get_auth_url(self):
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-top-read"
        )
        auth_url = sp_oauth.get_authorize_url()
        return auth_url
    
    def get_access_token(self, code: str):
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-top-read"
        )
        token_info = sp_oauth.get_access_token(code)
        return token_info.get("access_token")
    
    def get_top_artists(self, access_token: str, limit: int = 50):
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_top_artists(limit=limit)
        return results
