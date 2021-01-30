from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_get_token():
    response = client.post(
        "/token",
        headers={"accept":"application/json"},
        json={
            "username":"maxence",
            "password":"maxence"
        })
    assert response.status_code == 200

def test_post_song():
    response = client.post(
        "/song",
        headers={"accept":"application/json", "Content-Type": "application/json"},
        json={
            "songs": [
                {
                "artist": "string",
                "name": "string",
                "album_name": "string",
                "spotify_id": "string",
                "danceability": 0,
                "energy": 0,
                "key": 0,
                "loudness": 0,
                "mode": 0,
                "speechiness": 0,
                "acousticness": 0,
                "instrumentalness": 0,
                "liveness": 0,
                "valence": 0,
                "tempo": 0,
                "duration": 0,
                "popularity": 0
                }
            ]
            })
