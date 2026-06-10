from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# 1. URL atualizada para usar o driver assíncrono (asyncpg)
DATABASE_URL = "postgresql+asyncpg://admin:password@db:5432/streaming_db"

# 2. Criação do motor assíncrono
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# 3. Configuração da sessão assíncrona
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

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
    album = Column(String, nullable=True)
    compositor = Column(String, nullable=True)
    ano_lancamento = Column(Integer, nullable=True)
    genero = Column(String, nullable=True)
    duracao = Column(Integer, nullable=True)

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"))
    
    # 4. Adicionado lazy="selectin" para permitir carregamento assíncrono seguro
    musicas = relationship("Musica", secondary=playlist_musica, lazy="selectin")