from pydantic import BaseModel, SecretStr
import datetime

class Song(BaseModel):
    artist: str
    name: str = None
    album_name: str = None
    ts: datetime.datetime
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    password: str 
    class Config: 
        orm_mode = True