from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica
import logging
logging.basicConfig(level=logging.DEBUG)

class SoapUsuario(ComplexModel): 
    id = Integer
    nome = Unicode
    idade = Integer

class SoapMusica(ComplexModel): 
    id = Integer
    nome = Unicode
    artista = Unicode

class SoapPlaylist(ComplexModel): 
    id = Integer
    nome = Unicode
    usuario_id = Integer

class SOAPService(ServiceBase):
    @rpc(_returns=Iterable(SoapUsuario))
    def listar_usuarios(ctx):
        db = SessionLocal()
        for u in db.query(DbUser).all(): 
            yield SoapUsuario(id=u.id, nome=u.nome, idade=u.idade)
        db.close()

    @rpc(_returns=Iterable(SoapMusica))
    def listar_musicas(ctx):
        db = SessionLocal()
        for m in db.query(DbMusica).all(): 
            yield SoapMusica(id=m.id, nome=m.nome, artista=m.artista)
        db.close()

    @rpc(Integer, _returns=Iterable(SoapPlaylist))
    def playlists_usuario(ctx, user_id):
        db = SessionLocal()
        for p in db.query(DbPlaylist).filter(DbPlaylist.usuario_id == user_id).all(): 
            yield SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)
        db.close()

    @rpc(Integer, _returns=Iterable(SoapMusica))
    def musicas_playlist(ctx, playlist_id):
        db = SessionLocal()
        p = db.query(DbPlaylist).filter(DbPlaylist.id == playlist_id).first()
        if p:
            for m in p.musicas: 
                yield SoapMusica(id=m.id, nome=m.nome, artista=m.artista)
        db.close()

    @rpc(Integer, _returns=Iterable(SoapPlaylist))
    def playlists_por_musica(ctx, musica_id):
        db = SessionLocal()
        for p in db.query(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id).all(): 
            yield SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)
        db.close()

application = Application([SOAPService], 'streaming.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())

if __name__ == '__main__':
    run_simple('0.0.0.0', 8002, WsgiApplication(application))