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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()