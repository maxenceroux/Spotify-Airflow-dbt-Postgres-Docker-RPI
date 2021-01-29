from pydantic import BaseModel, SecretStr
import datetime
from typing import List

class Song(BaseModel):
    artist: str
    name: str = None
    album_name: str = None
    spotify_id: str = None
    danceability: float = None
    energy: float = None
    key: int = None
    loudness: float = None
    mode: int = None
    speechiness: float = None
    acousticness: float = None
    instrumentalness: float = None
    liveness: float = None
    valence: float = None
    tempo: float = None
    duration: int = None
    popularity: int = None
    class Config:
        orm_mode = True

class Songs(BaseModel):
    songs: List[Song]
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    password: str 
    class Config: 
        orm_mode = True

class Listen(BaseModel):
    ts: datetime.datetime
    spotify_id: str
    class Config:
        orm_mode = True
