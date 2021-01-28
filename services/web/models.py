from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String,)
    name = Column(String)
    album_name = Column(String)
    ts = Column(DateTime)
    spotify_id = Column(String)

class RefSong(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String,)
    name = Column(String)
    album_name = Column(String)
    ts = Column(DateTime)
    spotify_id = Column(String)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)