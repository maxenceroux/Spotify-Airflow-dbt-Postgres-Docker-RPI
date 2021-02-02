from fastapi.testclient import TestClient
import requests
from main import app
client = TestClient(app)


def get_token():
    url = "http://web:8000/token"
    print(1)
    header = {'accept': 'application/json'},
    data = {'username': 'maxence', 'password': 'maxence'}
    response = requests.request("POST", headers=header[0], data=data, url=url)
    return response.json()['access_token']


def test_get_token_authorized():
    response = client.post(
        "/token",
        data={'username': 'maxence', 'password': 'maxence'})
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_get_token_unauthorized():
    response = client.post(
        "/token",
        data={'username': 'maxime', 'password': 'maxime'})
    assert response.status_code == 200
    assert 'error' in response.json()
    assert response.json()['error'] == 'invalid credentials'


def test_get_songs():
    token = get_token()
    response = client.get(
        "/songs",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "msg" in response.json()


# def test_post_song():
#     # TODO: handling json
#     response = client.post(
#         "/song",
#         headers={"accept": "application/json",
#                  "Content-Type": "application/json"},
#         json={
#             "songs": [
#                 {
#                     "artist": "maxence",
#                     "name": "string",
#                     "album_name": "string",
#                     "spotify_id": "string",
#                     "danceability": 0,
#                     "energy": 0,
#                     "key": 0,
#                     "loudness": 0,
#                     "mode": 0,
#                     "speechiness": 0,
#                     "acousticness": 0,
#                     "instrumentalness": 0,
#                     "liveness": 0,
#                     "valence": 0,
#                     "tempo": 0,
#                     "duration": 0,
#                     "popularity": 0
#                 }
#             ]
#         })
#     assert response.json() == {"ds,": "sd,o"}
