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
from models import Listen as ModelListen

from schema import Song as SchemaSong
from schema import Songs as SchemaSongs
from schema import User as SchemaUser
from schema import Listen as SchemaListen
from sqlalchemy.dialects.postgresql import insert


from dotenv import load_dotenv
import json
from sqlalchemy import func, desc, create_engine
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import logging

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


@app.post('/token', status_code=200)
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
    logging.warning('collect token')
    token = get_token()
    try:
        ts = int(datetime.timestamp(db.session.query(
            ModelListen).order_by(desc('ts')).first().ts)*1000)
    except: 
        ts = int(datetime.timestamp(datetime.now() - timedelta(days=5))*1000)
    songs = spotify_cli.get_user_recently_played(token, ts)
    if not songs:
        return {"msg": "no songs but success"}
    songs_schema = []
    for s in songs:
        songs_schema.append(ModelListen(
            ts=s['ts'], spotify_id=s['spotify_id']))
    db.session.bulk_save_objects(songs_schema)
    db.session.commit()
    return {"msg": "uploaded songs", "songs": songs_schema}
    
@app.post("/song/", response_model=SchemaSongs, status_code=200)
def create_song(song: SchemaSongs):
    songs_to_insert = []
    engine = create_engine(os.environ['DATABASE_URL'])
    with engine.connect() as conn:
        for s in song.songs:
                stmt = insert(ModelSong).values(artist=s.artist, album_name=s.album_name, name=s.name, added_at=datetime.now(), spotify_id=s.spotify_id,
                            danceability=s.danceability, energy=s.energy, key=s.key, loudness=s.loudness, mode=s.mode, speechiness=s.speechiness, 
                            acousticness=s.acousticness, instrumentalness=s.instrumentalness, liveness=s.liveness, valence=s.valence,
                            tempo=s.tempo, duration=s.duration, popularity=s.popularity)
                stmt = stmt.on_conflict_do_nothing(
                    index_elements=['spotify_id']
                )
                conn.execute(stmt)
    return song


@app.post("/user/", response_model=SchemaUser)
def create_user(user: SchemaUser):
    db_user = ModelUser(
        username=user.username, password=generate_password_hash(user.password)
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user
