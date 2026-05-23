import grpc
from concurrent import futures
import streaming_pb2
import streaming_pb2_grpc
from db import SessionLocal, Usuario as DbUsuario

class StreamingServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def GetUsuarios(self, request, context):
        db = SessionLocal()
        usuarios = db.query(DbUsuario).all()
        db.close()
        
        user_list = [streaming_pb2.Usuario(id=u.id, nome=u.nome, idade=u.idade) for u in usuarios]
        return streaming_pb2.UsuarioList(usuarios=user_list)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()