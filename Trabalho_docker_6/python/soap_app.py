from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica
import logging

# 1. Calar o logger base e o Spyne
logging.basicConfig(level=logging.ERROR)

# 2. Calar os logs de acesso do Werkzeug (ESSENCIAL PARA TESTE DE CARGA)
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

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
            yield SoapMusica(id=m.id, nome=m.nome, artista=m.artista, album=m.album, compositor=m.compositor, ano_lancamento=m.ano_lancamento, genero=m.genero, duracao=m.duracao)
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
                yield SoapMusica(id=m.id, nome=m.nome, artista=m.artista, album=m.album, compositor=m.compositor, ano_lancamento=m.ano_lancamento, genero=m.genero, duracao=m.duracao)
        db.close()

    @rpc(Integer, _returns=Iterable(SoapPlaylist))
    def playlists_por_musica(ctx, musica_id):
        db = SessionLocal()
        for p in db.query(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id).all(): 
            yield SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)
        db.close()
    
    @rpc(Unicode, Integer, _returns=SoapUsuario)
    def criar_usuario(ctx, nome, idade):
        db = SessionLocal()
        novo = DbUser(nome=nome, idade=idade)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        db.close()
        return SoapUsuario(id=novo.id, nome=novo.nome, idade=novo.idade)

    @rpc(Unicode, Unicode, Unicode, Unicode, Integer, Unicode, Integer, _returns=SoapMusica)
    def criar_musica(ctx, nome, artista, album, compositor, ano_lancamento, genero, duracao):
        db = SessionLocal()
        nova = DbMusica(nome=nome, artista=artista, album=album, compositor=compositor, ano_lancamento=ano_lancamento, genero=genero, duracao=duracao)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return SoapMusica(id=nova.id, nome=nova.nome, artista=nova.artista, album=nova.album, compositor=nova.compositor, ano_lancamento=nova.ano_lancamento, genero=nova.genero, duracao=nova.duracao)

    @rpc(Unicode, Integer, _returns=SoapPlaylist)
    def criar_playlist(ctx, nome, usuario_id):
        db = SessionLocal()
        nova = DbPlaylist(nome=nome, usuario_id=usuario_id)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return SoapPlaylist(id=nova.id, nome=nova.nome, usuario_id=nova.usuario_id)

    @rpc(Integer, Unicode, Integer, _returns=SoapUsuario)
    def atualizar_usuario(ctx, id, nome, idade):
        db = SessionLocal()
        u = db.query(DbUser).filter(DbUser.id == id).first()
        if u:
            u.nome = nome
            u.idade = idade
            db.commit()
            db.refresh(u)
        db.close()
        return SoapUsuario(id=u.id, nome=u.nome, idade=u.idade)

    @rpc(Integer, _returns=Unicode)
    def deletar_usuario(ctx, id):
        db = SessionLocal()
        db.query(DbUser).filter(DbUser.id == id).delete()
        db.commit()
        db.close()
        return "Deletado com sucesso"

    @rpc(Integer, Unicode, Unicode, _returns=SoapMusica)
    def atualizar_musica(ctx, id, nome, artista):
        db = SessionLocal()
        m = db.query(DbMusica).filter(DbMusica.id == id).first()
        if m:
            m.nome = nome
            m.artista = artista
            db.commit()
            db.refresh(m)
        db.close()
        return SoapMusica(id=m.id, nome=m.nome, artista=m.artista)

    @rpc(Integer, _returns=Unicode)
    def deletar_musica(ctx, id):
        db = SessionLocal()
        db.query(DbMusica).filter(DbMusica.id == id).delete()
        db.commit()
        db.close()
        return "Deletado com sucesso"

    @rpc(Integer, Unicode, Integer, _returns=SoapPlaylist)
    def atualizar_playlist(ctx, id, nome, usuario_id):
        db = SessionLocal()
        p = db.query(DbPlaylist).filter(DbPlaylist.id == id).first()
        if p:
            p.nome = nome
            p.usuario_id = usuario_id
            db.commit()
            db.refresh(p)
        db.close()
        return SoapPlaylist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)

    @rpc(Integer, _returns=Unicode)
    def deletar_playlist(ctx, id):
        db = SessionLocal()
        db.query(DbPlaylist).filter(DbPlaylist.id == id).delete()
        db.commit()
        db.close()
        return "Deletado com sucesso"

application = Application([SOAPService], 'streaming.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())

if __name__ == '__main__':
    run_simple('0.0.0.0', 8002, WsgiApplication(application), threaded=True)