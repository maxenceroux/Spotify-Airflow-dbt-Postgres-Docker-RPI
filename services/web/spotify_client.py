import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import logging
load_dotenv()


class SpotifyClient:
    client_id = ""
    client_secret = ""

    def __init__(self):
        try:
            self.client_id = os.environ['SPOTIPY_CLIENT_ID']
            self.client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        except Exception:
            logging.error('could not find spotify credentials')

    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        payload = 'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, auth=HTTPBasicAuth(
            self.client_id, self.client_secret), headers=headers, data=payload)
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
        url = f"""https://api.spotify.com/v1/me/player/recently-played?limit=50
                &after={after}"""
        logging.warning(after)
        logging.warning(url)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.request("GET", url, headers=headers)
        if "items" not in response.json():
            return False
        songs = response.json()['items']
        if len(songs) == 0:
            return False
        ts_li, spotify_li = [], []
        for song in songs:
            ts_li.append(song['played_at'])
            spotify_li.append(song['track']['id'])
        songs_json = [{"ts": t, "spotify_id": sp}
                      for t, sp in zip(ts_li, spotify_li)]
        return songs_json
