from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
from db import SessionLocal, Usuario as DbUsuario

class Usuario(ComplexModel):
    id = Integer
    nome = Unicode
    idade = Integer

class StreamingService(ServiceBase):
    @rpc(_returns=Iterable(Usuario))
    def listar_usuarios(ctx):
        db = SessionLocal()
        usuarios = db.query(DbUsuario).all()
        db.close()
        for u in usuarios:
            yield Usuario(id=u.id, nome=u.nome, idade=u.idade)

application = Application([StreamingService], 'streaming.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    # Roda o servidor SOAP na porta 8002
    run_simple('0.0.0.0', 8002, wsgi_app)