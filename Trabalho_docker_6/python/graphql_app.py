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
    
@strawberry.type
class Mutation:
    @strawberry.field
    def criar_usuario(self, nome: str, idade: int) -> UsuarioGQL:
        db = SessionLocal()
        novo_usuario = DbUser(nome=nome, idade=idade)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        db.close()
        return UsuarioGQL(id=novo_usuario.id, nome=novo_usuario.nome, idade=novo_usuario.idade)

    @strawberry.field
    def criar_musica(self, nome: str, artista: str) -> MusicaGQL:
        db = SessionLocal()
        nova_musica = DbMusica(nome=nome, artista=artista)
        db.add(nova_musica)
        db.commit()
        db.refresh(nova_musica)
        db.close()
        return MusicaGQL(id=nova_musica.id, nome=nova_musica.nome, artista=nova_musica.artista)

    @strawberry.field
    def criar_playlist(self, nome: str, usuario_id: int) -> PlaylistGQL:
        db = SessionLocal()
        nova_playlist = DbPlaylist(nome=nome, usuario_id=usuario_id)
        db.add(nova_playlist)
        db.commit()
        db.refresh(nova_playlist)
        db.close()
        return PlaylistGQL(id=nova_playlist.id, nome=nova_playlist.nome, usuario_id=nova_playlist.usuario_id)
    
    @strawberry.field
    def atualizar_usuario(self, id: int, nome: str, idade: int) -> UsuarioGQL:
        db = SessionLocal()
        u = db.query(DbUser).filter(DbUser.id == id).first()
        if u:
            u.nome = nome
            u.idade = idade
            db.commit()
            db.refresh(u)
        db.close()
        return UsuarioGQL(id=u.id, nome=u.nome, idade=u.idade)

    @strawberry.field
    def deletar_usuario(self, id: int) -> bool:
        db = SessionLocal()
        linhas_afetadas = db.query(DbUser).filter(DbUser.id == id).delete()
        db.commit()
        db.close()
        return linhas_afetadas > 0

    @strawberry.field
    def atualizar_musica(self, id: int, nome: str, artista: str) -> MusicaGQL:
        db = SessionLocal()
        m = db.query(DbMusica).filter(DbMusica.id == id).first()
        if m:
            m.nome = nome
            m.artista = artista
            db.commit()
            db.refresh(m)
        db.close()
        return MusicaGQL(id=m.id, nome=m.nome, artista=m.artista)

    @strawberry.field
    def deletar_musica(self, id: int) -> bool:
        db = SessionLocal()
        linhas_afetadas = db.query(DbMusica).filter(DbMusica.id == id).delete()
        db.commit()
        db.close()
        return linhas_afetadas > 0

    @strawberry.field
    def atualizar_playlist(self, id: int, nome: str, usuario_id: int) -> PlaylistGQL:
        db = SessionLocal()
        p = db.query(DbPlaylist).filter(DbPlaylist.id == id).first()
        if p:
            p.nome = nome
            p.usuario_id = usuario_id
            db.commit()
            db.refresh(p)
        db.close()
        return PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id)

    @strawberry.field
    def deletar_playlist(self, id: int) -> bool:
        db = SessionLocal()
        linhas_afetadas = db.query(DbPlaylist).filter(DbPlaylist.id == id).delete()
        db.commit()
        db.close()
        return linhas_afetadas > 0

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
