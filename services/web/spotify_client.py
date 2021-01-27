import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import requests
import logging
load_dotenv()

class SpotifyClient:
    client_id = ""
    client_secret = ""

    def __init__(self):
        try:
            self.client_id = os.environ['SPOTIPY_CLIENT_ID']
            self.client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        except Exception as e: 
            logging.error('could not find spotify credentials')
    

    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        payload='grant_type=client_credentials'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, auth=HTTPBasicAuth(self.client_id, self.client_secret), headers=headers, data=payload)
        return response.json()['access_token']

    def get_current_play(self, token):
        url = "https://api.spotify.com/v1/me/player"
        headers = {
        'Accept': 'application/json',    
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }
        response = requests.request("GET", url, headers=headers)
        return response.text
        
    def get_user_recently_played(self, token, after):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={after}"
        logging.warning(after)
        logging.warning(url)
        headers = {
        'Accept': 'application/json',    
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }
        response = requests.request("GET", url, headers=headers)
        if not "items" in response.json():
            return False
        songs=response.json()['items']
        if len(songs)==0:
            return False
        artists_li, names_li, ts_li, albums_li, spotify_li = [], [], [], [], []
        for song in songs:
            artists_li.append(song['track']['album']['artists'][0]['name'])
            albums_li.append(song['track']['album']['name'])
            names_li.append(song['track']['name'])
            ts_li.append(song['played_at'])
            spotify_li.append(song['track']['id'])
        songs_json = [{"artist":a, "albums":ab, "name":n, "ts":t, "spotify_id":sp} for a, ab, n, t, sp in zip(artists_li, albums_li, names_li, ts_li, spotify_li)]
        return songs_json