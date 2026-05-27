import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica

@strawberry.type
class UsuarioGQL:
    id: int
    nome: str
    idade: int

@strawberry.type
class MusicaGQL:
    id: int
    nome: str
    artista: str

@strawberry.type
class PlaylistGQL:
    id: int
    nome: str
    usuario_id: int

@strawberry.type
class Query:
    @strawberry.field
    def usuarios(self) -> List[UsuarioGQL]:
        db = SessionLocal()
        res = db.query(DbUser).all()
        db.close()
        return [UsuarioGQL(id=u.id, nome=u.nome, idade=u.idade) for u in res]

    @strawberry.field
    def musicas(self) -> List[MusicaGQL]:
        db = SessionLocal()
        res = db.query(DbMusica).all()
        db.close()
        return [MusicaGQL(id=m.id, nome=m.nome, artista=m.artista) for m in res]

    @strawberry.field
    def playlists_usuario(self, user_id: int) -> List[PlaylistGQL]:
        db = SessionLocal()
        res = db.query(DbPlaylist).filter(DbPlaylist.usuario_id == user_id).all()
        db.close()
        return [PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in res]

    @strawberry.field
    def musicas_playlist(self, playlist_id: int) -> List[MusicaGQL]:
        db = SessionLocal()
        p = db.query(DbPlaylist).filter(DbPlaylist.id == playlist_id).first()
        res = p.musicas if p else []
        db.close()
        return [MusicaGQL(id=m.id, nome=m.nome, artista=m.artista) for m in res]

    @strawberry.field
    def playlists_por_musica(self, musica_id: int) -> List[PlaylistGQL]:
        db = SessionLocal()
        res = db.query(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id).all()
        db.close()
        return [PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in res]

schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")