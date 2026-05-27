from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, Usuario, Musica, Playlist, playlist_musica

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/usuarios")
def list_users(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.get("/musicas")
def list_songs(db: Session = Depends(get_db)):
    return db.query(Musica).all()

@app.get("/usuarios/{user_id}/playlists")
def user_playlists(user_id: int, db: Session = Depends(get_db)):
    return db.query(Playlist).filter(Playlist.usuario_id == user_id).all()

@app.get("/playlists/{playlist_id}/musicas")
def playlist_songs(playlist_id: int, db: Session = Depends(get_db)):
    p = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    return p.musicas if p else []

@app.get("/musicas/{musica_id}/playlists")
def song_playlists(musica_id: int, db: Session = Depends(get_db)):
    return db.query(Playlist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id).all()