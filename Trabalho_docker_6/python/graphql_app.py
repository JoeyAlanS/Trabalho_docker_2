import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from sqlalchemy.future import select
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
    album: Optional[str] = None
    compositor: Optional[str] = None
    ano_lancamento: Optional[int] = None
    genero: Optional[str] = None
    duracao: Optional[int] = None

@strawberry.type
class PlaylistGQL:
    id: int
    nome: str
    usuario_id: int

@strawberry.type
class Query:
    @strawberry.field
    async def usuarios(self) -> List[UsuarioGQL]:
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser))
            res = result.scalars().all()
        return [UsuarioGQL(id=u.id, nome=u.nome, idade=u.idade) for u in res]

    @strawberry.field
    async def musicas(self) -> List[MusicaGQL]:
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica))
            res = result.scalars().all()
        return [MusicaGQL(id=m.id, nome=m.nome, artista=m.artista, album=m.album, compositor=m.compositor, ano_lancamento=m.ano_lancamento, genero=m.genero, duracao=m.duracao) for m in res]

    @strawberry.field
    async def playlists_usuario(self, user_id: int) -> List[PlaylistGQL]:
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.usuario_id == user_id))
            res = result.scalars().all()
        return [PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in res]

    @strawberry.field
    async def musicas_playlist(self, playlist_id: int) -> List[MusicaGQL]:
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == playlist_id))
            p = result.scalars().first()
            res = p.musicas if p else []
        return [MusicaGQL(id=m.id, nome=m.nome, artista=m.artista, album=m.album, compositor=m.compositor, ano_lancamento=m.ano_lancamento, genero=m.genero, duracao=m.duracao) for m in res]

    @strawberry.field
    async def playlists_por_musica(self, musica_id: int) -> List[PlaylistGQL]:
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id))
            res = result.scalars().all()
        return [PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in res]
    
@strawberry.type
class Mutation:
    @strawberry.field
    async def criar_usuario(self, nome: str, idade: int) -> UsuarioGQL:
        async with SessionLocal() as db:
            novo_usuario = DbUser(nome=nome, idade=idade)
            db.add(novo_usuario)
            await db.commit()
            await db.refresh(novo_usuario)
        return UsuarioGQL(id=novo_usuario.id, nome=novo_usuario.nome, idade=novo_usuario.idade)

    @strawberry.field
    async def criar_musica(self, nome: str, artista: str, album: str = None, compositor: str = None, ano_lancamento: int = None, genero: str = None, duracao: int = None) -> MusicaGQL:
        async with SessionLocal() as db:
            nova_musica = DbMusica(nome=nome, artista=artista, album=album, compositor=compositor, ano_lancamento=ano_lancamento, genero=genero, duracao=duracao)
            db.add(nova_musica)
            await db.commit()
            await db.refresh(nova_musica)
        return MusicaGQL(id=nova_musica.id, nome=nova_musica.nome, artista=nova_musica.artista, album=nova_musica.album, compositor=nova_musica.compositor, ano_lancamento=nova_musica.ano_lancamento, genero=nova_musica.genero, duracao=nova_musica.duracao)

    @strawberry.field
    async def criar_playlist(self, nome: str, usuario_id: int) -> PlaylistGQL:
        async with SessionLocal() as db:
            nova_playlist = DbPlaylist(nome=nome, usuario_id=usuario_id)
            db.add(nova_playlist)
            await db.commit()
            await db.refresh(nova_playlist)
        return PlaylistGQL(id=nova_playlist.id, nome=nova_playlist.nome, usuario_id=nova_playlist.usuario_id)
    
    @strawberry.field
    async def atualizar_usuario(self, id: int, nome: str, idade: int) -> UsuarioGQL:
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser).filter(DbUser.id == id))
            u = result.scalars().first()
            if u:
                u.nome = nome
                u.idade = idade
                await db.commit()
                await db.refresh(u)
        return UsuarioGQL(id=u.id, nome=u.nome, idade=u.idade)

    @strawberry.field
    async def deletar_usuario(self, id: int) -> bool:
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser).filter(DbUser.id == id))
            u = result.scalars().first()
            if u:
                await db.delete(u)
                await db.commit()
                return True
        return False

    @strawberry.field
    async def atualizar_musica(self, id: int, nome: str, artista: str) -> MusicaGQL:
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica).filter(DbMusica.id == id))
            m = result.scalars().first()
            if m:
                m.nome = nome
                m.artista = artista
                await db.commit()
                await db.refresh(m)
        return MusicaGQL(id=m.id, nome=m.nome, artista=m.artista)

    @strawberry.field
    async def deletar_musica(self, id: int) -> bool:
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica).filter(DbMusica.id == id))
            m = result.scalars().first()
            if m:
                await db.delete(m)
                await db.commit()
                return True
        return False

    @strawberry.field
    async def atualizar_playlist(self, id: int, nome: str, usuario_id: int) -> PlaylistGQL:
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == id))
            p = result.scalars().first()
            if p:
                p.nome = nome
                p.usuario_id = usuario_id
                await db.commit()
                await db.refresh(p)
        return PlaylistGQL(id=p.id, nome=p.nome, usuario_id=p.usuario_id)

    @strawberry.field
    async def deletar_playlist(self, id: int) -> bool:
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == id))
            p = result.scalars().first()
            if p:
                await db.delete(p)
                await db.commit()
                return True
        return False

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")