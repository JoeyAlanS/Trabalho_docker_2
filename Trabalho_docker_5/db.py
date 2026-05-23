from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

DATABASE_URL = "sqlite:////app/data/streaming.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

playlist_musica = Table(
    'playlist_musica',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id'), primary_key=True),
    Column('musica_id', Integer, ForeignKey('musicas.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    playlists = relationship("Playlist", back_populates="usuario")

class Musica(Base):
    __tablename__ = "musicas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    artista = Column(String)
    playlists = relationship("Playlist", secondary=playlist_musica, back_populates="musicas")

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="playlists")
    musicas = relationship("Musica", secondary=playlist_musica, back_populates="playlists")

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(Usuario).first():
        u1 = Usuario(nome="Alice", idade=25)
        m1 = Musica(nome="Bohemian Rhapsody", artista="Queen")
        m2 = Musica(nome="Stairway to Heaven", artista="Led Zeppelin")
        p1 = Playlist(nome="Rock Classics", usuario=u1, musicas=[m1, m2])
        db.add_all([u1, m1, m2, p1])
        db.commit()
    db.close()