from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, Usuario, Musica, Playlist, init_db

app = FastAPI(title="REST Streaming API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.get("/musicas")
def get_musicas(db: Session = Depends(get_db)):
    return db.query(Musica).all()

@app.get("/usuarios/{user_id}/playlists")
def get_user_playlists(user_id: int, db: Session = Depends(get_db)):
    return db.query(Playlist).filter(Playlist.usuario_id == user_id).all()

@app.get("/playlists/{playlist_id}/musicas")
def get_playlist_musicas(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    return playlist.musicas if playlist else []

@app.get("/musicas/{musica_id}/playlists")
def get_playlists_by_musica(musica_id: int, db: Session = Depends(get_db)):
    musica = db.query(Musica).filter(Musica.id == musica_id).first()
    return musica.playlists if musica else []