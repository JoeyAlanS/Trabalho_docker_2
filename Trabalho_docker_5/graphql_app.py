import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List
from db import SessionLocal, Usuario as DbUsuario, Musica as DbMusica, Playlist as DbPlaylist

@strawberry.type
class Musica:
    id: int
    nome: str
    artista: str

@strawberry.type
class Playlist:
    id: int
    nome: str

@strawberry.type
class Usuario:
    id: int
    nome: str
    idade: int

@strawberry.type
class Query:
    @strawberry.field
    def usuarios(self) -> List[Usuario]:
        db = SessionLocal()
        users = db.query(DbUsuario).all()
        db.close()
        return [Usuario(id=u.id, nome=u.nome, idade=u.idade) for u in users]

    @strawberry.field
    def musicas(self) -> List[Musica]:
        db = SessionLocal()
        musicas = db.query(DbMusica).all()
        db.close()
        return [Musica(id=m.id, nome=m.nome, artista=m.artista) for m in musicas]

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="GraphQL Streaming API")
app.include_router(graphql_app, prefix="/graphql")