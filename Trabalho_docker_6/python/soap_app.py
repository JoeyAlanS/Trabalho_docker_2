import asyncio
import threading
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
from sqlalchemy.future import select
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica
import logging

logging.basicConfig(level=logging.ERROR)
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

# ==========================================
# PONTE: SÍNCRONO -> ASSÍNCRONO
# ==========================================
# Cria um único loop de eventos rodando em background.
# Isso garante que o pool de conexões do SQLAlchemy (asyncpg) nunca quebre, 
# pois ele estará amarrado a um loop contínuo, seguro para uso multithread do WSGI.
_loop = asyncio.new_event_loop()

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_background_loop, args=(_loop,), daemon=True).start()

def run_async(coro):
    """Executa a corotina no loop de background e retorna o resultado de forma síncrona."""
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()

# ==========================================
# MODELOS SOAP
# ==========================================
class SoapUsuario(ComplexModel): 
    id = Integer
    nome = Unicode
    idade = Integer

class SoapMusica(ComplexModel): 
    id = Integer
    nome = Unicode
    artista = Unicode
    album = Unicode(min_occurs=0)
    compositor = Unicode(min_occurs=0)
    ano_lancamento = Integer(min_occurs=0)
    genero = Unicode(min_occurs=0)
    duracao = Integer(min_occurs=0)

class SoapPlaylist(ComplexModel): 
    id = Integer
    nome = Unicode
    usuario_id = Integer

# ==========================================
# SERVIÇO
# ==========================================
class SOAPService(ServiceBase):
    @rpc(_returns=Iterable(SoapUsuario))
    def listar_usuarios(ctx):
        async def _get():
            async with SessionLocal() as db:
                result = await db.execute(select(DbUser))
                # Montamos os objetos Soap DENTRO da sessão para evitar erro de detached instance
                return [SoapUsuario(id=u.id, nome=u.nome, idade=u.idade) for u in result.scalars().all()]
        
        for u in run_async(_get()): 
            yield u

    @rpc(_returns=Iterable(SoapMusica))
    def listar_musicas(ctx):
        async def _get():
            async with SessionLocal() as db:
                result = await db.execute(select(DbMusica))
                return [
                    SoapMusica(id=m.id, nome=m.nome, artista=m.artista, album=m.album, 
                               compositor=m.compositor, ano_lancamento=m.ano_lancamento, 
                               genero=m.genero, duracao=m.duracao) 
                    for m in result.scalars().all()
                ]
        for m in run_async(_get()): 
            yield m

    @rpc(Integer, _returns=Iterable(SoapPlaylist))
    def playlists_usuario(ctx, user_id):
        async def _get():
            async with SessionLocal() as db:
                result = await db.execute(select(DbPlaylist).filter(DbPlaylist.usuario_id == user_id))
                return [SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in result.scalars().all()]
        for p in run_async(_get()): 
            yield p

    @rpc(Integer, _returns=Iterable(SoapMusica))
    def musicas_playlist(ctx, playlist_id):
        async def _get():
            async with SessionLocal() as db:
                result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == playlist_id))
                p = result.scalars().first()
                musicas = p.musicas if p else []
                return [
                    SoapMusica(id=m.id, nome=m.nome, artista=m.artista, album=m.album, 
                               compositor=m.compositor, ano_lancamento=m.ano_lancamento, 
                               genero=m.genero, duracao=m.duracao) 
                    for m in musicas
                ]
        for m in run_async(_get()): 
            yield m

    @rpc(Integer, _returns=Iterable(SoapPlaylist))
    def playlists_por_musica(ctx, musica_id):
        async def _get():
            async with SessionLocal() as db:
                result = await db.execute(select(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id))
                return [SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in result.scalars().all()]
        for p in run_async(_get()): 
            yield p
    
    @rpc(Unicode, Integer, _returns=SoapUsuario)
    def criar_usuario(ctx, nome, idade):
        async def _run():
            async with SessionLocal() as db:
                novo = DbUser(nome=nome, idade=idade)
                db.add(novo)
                await db.commit()
                await db.refresh(novo)
                return novo.id, novo.nome, novo.idade
        id, n, i = run_async(_run())
        return SoapUsuario(id=id, nome=n, idade=i)

    @rpc(Unicode, Unicode, Unicode, Unicode, Integer, Unicode, Integer, _returns=SoapMusica)
    def criar_musica(ctx, nome, artista, album, compositor, ano_lancamento, genero, duracao):
        async def _run():
            async with SessionLocal() as db:
                nova = DbMusica(nome=nome, artista=artista, album=album, compositor=compositor, ano_lancamento=ano_lancamento, genero=genero, duracao=duracao)
                db.add(nova)
                await db.commit()
                await db.refresh(nova)
                return nova.id, nova.nome, nova.artista, nova.album, nova.compositor, nova.ano_lancamento, nova.genero, nova.duracao
        id, n, art, alb, comp, ano, gen, dur = run_async(_run())
        return SoapMusica(id=id, nome=n, artista=art, album=alb, compositor=comp, ano_lancamento=ano, genero=gen, duracao=dur)

    @rpc(Unicode, Integer, _returns=SoapPlaylist)
    def criar_playlist(ctx, nome, usuario_id):
        async def _run():
            async with SessionLocal() as db:
                nova = DbPlaylist(nome=nome, usuario_id=usuario_id)
                db.add(nova)
                await db.commit()
                await db.refresh(nova)
                return nova.id, nova.nome, nova.usuario_id
        id, n, uid = run_async(_run())
        return SoapPlaylist(id=id, nome=n, usuario_id=uid)

    @rpc(Integer, Unicode, Integer, _returns=SoapUsuario)
    def atualizar_usuario(ctx, id, nome, idade):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbUser).filter(DbUser.id == id))
                u = result.scalars().first()
                if u:
                    u.nome = nome
                    u.idade = idade
                    await db.commit()
                    await db.refresh(u)
                    return u.id, u.nome, u.idade
                return None
        res = run_async(_run())
        if res:
            return SoapUsuario(id=res[0], nome=res[1], idade=res[2])
        return None

    @rpc(Integer, _returns=Unicode)
    def deletar_usuario(ctx, id):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbUser).filter(DbUser.id == id))
                u = result.scalars().first()
                if u:
                    await db.delete(u)
                    await db.commit()
        run_async(_run())
        return "Deletado com sucesso"

    @rpc(Integer, Unicode, Unicode, _returns=SoapMusica)
    def atualizar_musica(ctx, id, nome, artista):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbMusica).filter(DbMusica.id == id))
                m = result.scalars().first()
                if m:
                    m.nome = nome
                    m.artista = artista
                    await db.commit()
                    await db.refresh(m)
                    return m.id, m.nome, m.artista
                return None
        res = run_async(_run())
        if res:
            return SoapMusica(id=res[0], nome=res[1], artista=res[2])
        return None

    @rpc(Integer, _returns=Unicode)
    def deletar_musica(ctx, id):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbMusica).filter(DbMusica.id == id))
                m = result.scalars().first()
                if m:
                    await db.delete(m)
                    await db.commit()
        run_async(_run())
        return "Deletado com sucesso"

    @rpc(Integer, Unicode, Integer, _returns=SoapPlaylist)
    def atualizar_playlist(ctx, id, nome, usuario_id):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == id))
                p = result.scalars().first()
                if p:
                    p.nome = nome
                    p.usuario_id = usuario_id
                    await db.commit()
                    await db.refresh(p)
                    return p.id, p.nome, p.usuario_id
                return None
        res = run_async(_run())
        if res:
            return SoapPlaylist(id=res[0], nome=res[1], usuario_id=res[2])
        return None

    @rpc(Integer, _returns=Unicode)
    def deletar_playlist(ctx, id):
        async def _run():
            async with SessionLocal() as db:
                result = await db.execute(select(DbPlaylist).filter(DbPlaylist.id == id))
                p = result.scalars().first()
                if p:
                    await db.delete(p)
                    await db.commit()
        run_async(_run())
        return "Deletado com sucesso"

application = Application([SOAPService], 'streaming.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    run_simple('0.0.0.0', 8002, wsgi_app, threaded=True)