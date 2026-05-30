from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
DATABASE_URL = "postgresql://admin:password@db:5432/streaming_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

playlist_musica = Table(
    'playlist_musica', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id', ondelete="CASCADE"), primary_key=True),
    Column('musica_id', Integer, ForeignKey('musicas.id', ondelete="CASCADE"), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer)

class Musica(Base):
    __tablename__ = 'musicas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    artista = Column(String, nullable=False)

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"))
    
    musicas = relationship("Musica", secondary=playlist_musica)