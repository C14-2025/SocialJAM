import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import base64

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
    
    def get_auth_url(self, state: str = None):
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-top-read",
            state=state
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
        return {
            "access_token": token_info.get("access_token"),
            "refresh_token": token_info.get("refresh_token"),
            "expires_at": datetime.now() + timedelta(seconds=token_info.get("expires_in", 3600))
        }
    
    # get application access token
    def get_app_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        return response.json()["access_token"]

    def refresh_access_token(self, refresh_token: str):
        try:
            token_url = "https://accounts.spotify.com/api/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            response = requests.post(token_url, data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    "access_token": token_data.get("access_token"),
                    "expires_at": datetime.now() + timedelta(seconds=token_data.get("expires_in", 3600))
                }
            else:
                return None
        except Exception as e:
            print(f"Erro ao renovar token: {str(e)}")
            return None
    
    def validate_token(self, access_token: str) -> bool:
        try:
            sp = spotipy.Spotify(auth=access_token)
            sp.current_user()
            return True
        except Exception:
            return False
    
    def get_top_artists(self, access_token: str, limit: int = 50):
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_top_artists(limit=limit)
        return results

    def get_artist_albums(self, artist_name: str):
        base_url = "https://api.spotify.com/v1"
        token = self.get_app_access_token()  
        
        headers = {"Authorization": f"Bearer {token}"}

        search_url = f"{base_url}/search"
        search_params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1
        }

        artist_res = requests.get(search_url, headers=headers, params=search_params)
        artist_data = artist_res.json()

        if not artist_data.get("artists", {}).get("items"):
            return {"albums": []}

        artist = artist_data["artists"]["items"][0]
        artist_id = artist["id"]

        albums_url = f"{base_url}/artists/{artist_id}/albums"
        albums_params = {"limit": 50, "include_groups": "album,single"}

        albums_res = requests.get(albums_url, headers=headers, params=albums_params)
        albums_data = albums_res.json()

        raw_albums = albums_data.get("items", [])

        cleaned_albums = []

        for album in raw_albums:
            cleaned_albums.append({
                "name": album.get("name"),
                "release_date": album.get("release_date"),
                "total_tracks": album.get("total_tracks"),
                "image": (
                    album.get("images")[0]["url"]
                    if album.get("images") and len(album["images"]) > 0
                    else None
                )
            })

        return {
            "artist": artist.get("name"),
            "albums": cleaned_albums
        }

    def search_artists(self, query: str, limit: int = 12):
        token = self.get_app_access_token()

        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": query,
            "type": "artist",
            "limit": limit
        }

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()

        return data.get("artists", {}).get("items", [])
