from scrapper import get_token
from spotify_client import SpotifyClient
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from models import Song as ModelSong
from models import User as ModelUser
from schema import Song as SchemaSong
from schema import User as SchemaUser
from dotenv import load_dotenv
import json
from sqlalchemy import func, desc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JWT_SECRET = 'mysecret'
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str):
    user = db.session.query(ModelUser).filter_by(username=username).first()
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error': 'invalid credentials'}
    token = jwt.encode({'user': user.username}, JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@app.get("/songs", status_code=200)
def get_songs(token: str = Depends(oauth2_scheme)):
    
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    user = db.session.query(ModelUser).filter_by(
        username=payload.get("user")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    spotify_cli = SpotifyClient()
    token = get_token()
    # ts = int(time.time())
    # ts = db.session.query(ModelSong).order_by(desc('ts')).first().ts
    ts = int(datetime.timestamp(db.session.query(
        ModelSong).order_by(desc('ts')).first().ts)*1000)

    songs = spotify_cli.get_user_recently_played(token, ts)
    if not songs:
        return {"msg": "no songs but success"}
    songs_schema = []
    for s in songs:
        songs_schema.append(ModelSong(
            artist=s['artist'], album_name=s['albums'], name=s['name'], ts=s['ts']))
    db.session.bulk_save_objects(songs_schema)
    db.session.commit()
    return songs_schema


@app.get("/songs_20", status_code=200)
def get_songs(token: str = Depends(oauth2_scheme)):

    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    user = db.session.query(ModelUser).filter_by(
        username=payload.get("user")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    spotify_cli = SpotifyClient()
    token = get_token()
    ts = int(datetime.now().timestamp()*1000-20*60*1000)
    songs = spotify_cli.get_user_recently_played(token, ts)
    if not songs:
        return {"msg": "no songs but success"}
    songs_schema = []
    for s in songs:
        songs_schema.append(ModelSong(
            artist=s['artist'], album_name=s['albums'], name=s['name'], ts=s['ts']))
    db.session.bulk_save_objects(songs_schema)
    db.session.commit()
    return songs_schema


@app.post("/song/", response_model=SchemaSong)
def create_song(song: SchemaSong):
    db_song = ModelSong(
        artist=song.artist, album_name=song.album_name, name=song.name, ts=song.ts
    )
    db.session.add(db_song)
    db.session.commit()
    return db_song


@app.post("/user/", response_model=SchemaUser)
def create_user(user: SchemaUser):
    db_user = ModelUser(
        username=user.username, password=generate_password_hash(user.password)
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user
