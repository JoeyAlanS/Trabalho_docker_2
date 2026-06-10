import asyncio
import grpc
from grpc import aio
import streaming_pb2, streaming_pb2_grpc
from sqlalchemy.future import select
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica

class StreamingServicer(streaming_pb2_grpc.StreamingServiceServicer):
    async def ListarUsuarios(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser))
            users = result.scalars().all()
        return streaming_pb2.UsuarioList(usuarios=[streaming_pb2.Usuario(id=u.id, nome=u.nome, idade=u.idade) for u in users])

    async def ListarMusicas(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica))
            musicas = result.scalars().all()
        return streaming_pb2.MusicaList(musicas=[streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista, album=m.album or "", compositor=m.compositor or "", ano_lancamento=m.ano_lancamento or 0, genero=m.genero or "", duracao=m.duracao or 0) for m in musicas])

    async def ListarPlaylistsUsuario(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.usuario_id == request.id))
            playlists = result.scalars().all()
        return streaming_pb2.PlaylistList(playlists=[streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in playlists])

    async def ListarMusicasPlaylist(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == request.id))
            p = result.scalars().first()
            musicas = p.musicas if p else []
        return streaming_pb2.MusicaList(musicas=[streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista, album=m.album or "", compositor=m.compositor or "", ano_lancamento=m.ano_lancamento or 0, genero=m.genero or "", duracao=m.duracao or 0) for m in musicas])

    async def ListarPlaylistsPorMusica(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == request.id))
            playlists = result.scalars().all()
        return streaming_pb2.PlaylistList(playlists=[streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in playlists])
    
    async def CriarUsuario(self, request, context):
        async with SessionLocal() as db:
            novo = DbUser(nome=request.nome, idade=request.idade)
            db.add(novo)
            await db.commit()
            await db.refresh(novo)
        return streaming_pb2.Usuario(id=novo.id, nome=novo.nome, idade=novo.idade)

    async def CriarMusica(self, request, context):
        async with SessionLocal() as db:
            nova = DbMusica(nome=request.nome, artista=request.artista, album=request.album or None, compositor=request.compositor or None, ano_lancamento=request.ano_lancamento or None, genero=request.genero or None, duracao=request.duracao or None)
            db.add(nova)
            await db.commit()
            await db.refresh(nova)
        return streaming_pb2.Musica(id=nova.id, nome=nova.nome, artista=nova.artista, album=nova.album or "", compositor=nova.compositor or "", ano_lancamento=nova.ano_lancamento or 0, genero=nova.genero or "", duracao=nova.duracao or 0)

    async def CriarPlaylist(self, request, context):
        async with SessionLocal() as db:
            nova = DbPlaylist(nome=request.nome, usuario_id=request.usuario_id)
            db.add(nova)
            await db.commit()
            await db.refresh(nova)
        return streaming_pb2.Playlist(id=nova.id, nome=nova.nome, usuario_id=nova.usuario_id)
    
    async def AtualizarUsuario(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser).filter(DbUser.id == request.id))
            u = result.scalars().first()
            if u:
                u.nome = request.nome
                u.idade = request.idade
                await db.commit()
                await db.refresh(u)
        return streaming_pb2.Usuario(id=u.id, nome=u.nome, idade=u.idade)

    async def DeletarUsuario(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbUser).filter(DbUser.id == request.id))
            u = result.scalars().first()
            if u:
                await db.delete(u)
                await db.commit()
        return streaming_pb2.Empty()

    async def AtualizarMusica(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica).filter(DbMusica.id == request.id))
            m = result.scalars().first()
            if m:
                m.nome = request.nome
                m.artista = request.artista
                m.album = request.album or None
                m.compositor = request.compositor or None
                m.ano_lancamento = request.ano_lancamento or None
                m.genero = request.genero or None
                m.duracao = request.duracao or None
                await db.commit()
                await db.refresh(m)
        return streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista, album=m.album or "", compositor=m.compositor or "", ano_lancamento=m.ano_lancamento or 0, genero=m.genero or "", duracao=m.duracao or 0)

    async def DeletarMusica(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbMusica).filter(DbMusica.id == request.id))
            m = result.scalars().first()
            if m:
                await db.delete(m)
                await db.commit()
        return streaming_pb2.Empty()

    async def AtualizarPlaylist(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == request.id))
            p = result.scalars().first()
            if p:
                p.nome = request.nome
                p.usuario_id = request.usuario_id
                await db.commit()
                await db.refresh(p)
        return streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)

    async def DeletarPlaylist(self, request, context):
        async with SessionLocal() as db:
            result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == request.id))
            p = result.scalars().first()
            if p:
                await db.delete(p)
                await db.commit()
        return streaming_pb2.Empty()

async def serve():
    # Iniciando o servidor assíncrono nativo do gRPC
    server = aio.server()
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())