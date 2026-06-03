import grpc
from concurrent import futures
import streaming_pb2, streaming_pb2_grpc
from db import SessionLocal, Usuario as DbUser, Musica as DbMusica, Playlist as DbPlaylist, playlist_musica

class StreamingServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def ListarUsuarios(self, request, context):
        db = SessionLocal(); users = db.query(DbUser).all(); db.close()
        return streaming_pb2.UsuarioList(usuarios=[streaming_pb2.Usuario(id=u.id, nome=u.nome, idade=u.idade) for u in users])

    def ListarMusicas(self, request, context):
        db = SessionLocal(); musicas = db.query(DbMusica).all(); db.close()
        return streaming_pb2.MusicaList(musicas=[streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista) for m in musicas])

    def ListarPlaylistsUsuario(self, request, context):
        db = SessionLocal(); playlists = db.query(DbPlaylist).filter(DbPlaylist.usuario_id == request.id).all(); db.close()
        return streaming_pb2.PlaylistList(playlists=[streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in playlists])

    def ListarMusicasPlaylist(self, request, context):
        db = SessionLocal(); p = db.query(DbPlaylist).filter(DbPlaylist.id == request.id).first(); musicas = p.musicas if p else []; db.close()
        return streaming_pb2.MusicaList(musicas=[streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista) for m in musicas])

    def ListarPlaylistsPorMusica(self, request, context):
        db = SessionLocal(); playlists = db.query(DbPlaylist).join(playlist_musica).filter(playlist_musica.c.musica_id == request.id).all(); db.close()
        return streaming_pb2.PlaylistList(playlists=[streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id) for p in playlists])
    
    def CriarUsuario(self, request, context):
        db = SessionLocal()
        novo = DbUser(nome=request.nome, idade=request.idade)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        db.close()
        return streaming_pb2.Usuario(id=novo.id, nome=novo.nome, idade=novo.idade)

    def CriarMusica(self, request, context):
        db = SessionLocal()
        nova = DbMusica(nome=request.nome, artista=request.artista)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return streaming_pb2.Musica(id=nova.id, nome=nova.nome, artista=nova.artista)

    def CriarPlaylist(self, request, context):
        db = SessionLocal()
        nova = DbPlaylist(nome=request.nome, usuario_id=request.usuario_id)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return streaming_pb2.Playlist(id=nova.id, nome=nova.nome, usuario_id=nova.usuario_id)
    
    def AtualizarUsuario(self, request, context):
        db = SessionLocal()
        u = db.query(DbUser).filter(DbUser.id == request.id).first()
        if u:
            u.nome = request.nome
            u.idade = request.idade
            db.commit()
            db.refresh(u)
        db.close()
        return streaming_pb2.Usuario(id=u.id, nome=u.nome, idade=u.idade)

    def DeletarUsuario(self, request, context):
        db = SessionLocal()
        db.query(DbUser).filter(DbUser.id == request.id).delete()
        db.commit()
        db.close()
        return streaming_pb2.Empty()

    def AtualizarMusica(self, request, context):
        db = SessionLocal()
        m = db.query(DbMusica).filter(DbMusica.id == request.id).first()
        if m:
            m.nome = request.nome
            m.artista = request.artista
            db.commit()
            db.refresh(m)
        db.close()
        return streaming_pb2.Musica(id=m.id, nome=m.nome, artista=m.artista)

    def DeletarMusica(self, request, context):
        db = SessionLocal()
        db.query(DbMusica).filter(DbMusica.id == request.id).delete()
        db.commit()
        db.close()
        return streaming_pb2.Empty()

    def AtualizarPlaylist(self, request, context):
        db = SessionLocal()
        p = db.query(DbPlaylist).filter(DbPlaylist.id == request.id).first()
        if p:
            p.nome = request.nome
            p.usuario_id = request.usuario_id
            db.commit()
            db.refresh(p)
        db.close()
        return streaming_pb2.Playlist(id=p.id, nome=p.nome, usuario_id=p.usuario_id)

    def DeletarPlaylist(self, request, context):
        db = SessionLocal()
        db.query(DbPlaylist).filter(DbPlaylist.id == request.id).delete()
        db.commit()
        db.close()
        return streaming_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()