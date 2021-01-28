from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Listen(Base):
    __tablename__ = "listen"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime)
    spotify_id = Column(String)

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String,)
    name = Column(String)
    album_name = Column(String)
    added_at = Column(DateTime)
    spotify_id = Column(String)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    duration = Column(Integer)



class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)