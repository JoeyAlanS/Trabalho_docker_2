from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from db import SessionLocal, Usuario, Musica, Playlist, playlist_musica

app = FastAPI()

# ==========================================
# DEPENDÊNCIA DO BANCO DE DADOS
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ESQUEMAS PYDANTIC (VALIDAÇÃO DE ENTRADA)
# ==========================================
class UsuarioSchema(BaseModel):
    nome: str
    idade: int

class MusicaSchema(BaseModel):
    nome: str
    artista: str
    album: str = None
    compositor: str = None
    ano_lancamento: int = None
    genero: str = None
    duracao: int = None

class PlaylistCreateSchema(BaseModel):
    nome: str
    usuario_id: int

class PlaylistUpdateSchema(BaseModel):
    nome: str

# ==========================================
# OPERAÇÕES DE CRUD: USUÁRIOS
# ==========================================

@app.get("/usuarios")
def list_users(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.get("/usuarios/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def criar_usuario(user: UsuarioSchema, db: Session = Depends(get_db)):
    novo_usuario = Usuario(nome=user.nome, idade=user.idade)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.put("/usuarios/{user_id}")
def atualizar_usuario(user_id: int, user: UsuarioSchema, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario_db.nome = user.nome
    usuario_db.idade = user.idade
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@app.delete("/usuarios/{user_id}")
def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(usuario_db)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}

# ==========================================
# OPERAÇÕES DE CRUD: MÚSICAS
# ==========================================

@app.get("/musicas")
def list_songs(db: Session = Depends(get_db)):
    return db.query(Musica).all()

@app.get("/musicas/{musica_id}")
def get_song(musica_id: int, db: Session = Depends(get_db)):
    musica = db.query(Musica).filter(Musica.id == musica_id).first()
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return musica

@app.post("/musicas", status_code=status.HTTP_201_CREATED)
def criar_musica(song: MusicaSchema, db: Session = Depends(get_db)):
    nova_musica = Musica(
        nome=song.nome, 
        artista=song.artista,
        album=song.album,
        compositor=song.compositor,
        ano_lancamento=song.ano_lancamento,
        genero=song.genero,
        duracao=song.duracao
    )
    db.add(nova_musica)
    db.commit()
    db.refresh(nova_musica)
    return nova_musica

@app.put("/musicas/{musica_id}")
def atualizar_musica(musica_id: int, song: MusicaSchema, db: Session = Depends(get_db)):
    musica_db = db.query(Musica).filter(Musica.id == musica_id).first()
    if not musica_db:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    musica_db.nome = song.nome
    musica_db.artista = song.artista
    musica_db.album = song.album
    musica_db.compositor = song.compositor
    musica_db.ano_lancamento = song.ano_lancamento
    musica_db.genero = song.genero
    musica_db.duracao = song.duracao
    db.commit()
    db.refresh(musica_db)
    return musica_db

@app.delete("/musicas/{musica_id}")
def deletar_musica(musica_id: int, db: Session = Depends(get_db)):
    musica_db = db.query(Musica).filter(Musica.id == musica_id).first()
    if not musica_db:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    db.delete(musica_db)
    db.commit()
    return {"mensagem": "Música deletada com sucesso"}

# ==========================================
# OPERAÇÕES DE CRUD: PLAYLISTS
# ==========================================

@app.get("/usuarios/{user_id}/playlists")
def user_playlists(user_id: int, db: Session = Depends(get_db)):
    return db.query(Playlist).filter(Playlist.usuario_id == user_id).all()

@app.post("/playlists", status_code=status.HTTP_201_CREATED)
def criar_playlist(playlist: PlaylistCreateSchema, db: Session = Depends(get_db)):
    # Valida se o usuário dono da playlist realmente existe
    usuario = db.query(Usuario).filter(Usuario.id == playlist.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário informado não existe")
        
    nova_playlist = Playlist(nome=playlist.nome, usuario_id=playlist.usuario_id)
    db.add(nova_playlist)
    db.commit()
    db.refresh(nova_playlist)
    return nova_playlist

@app.put("/playlists/{playlist_id}")
def atualizar_playlist(playlist_id: int, playlist: PlaylistUpdateSchema, db: Session = Depends(get_db)):
    playlist_db = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist_db:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    playlist_db.nome = playlist.nome
    db.commit()
    db.refresh(playlist_db)
    return playlist_db

@app.delete("/playlists/{playlist_id}")
def deletar_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist_db = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist_db:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    db.delete(playlist_db)
    db.commit()
    return {"mensagem": "Playlist deletada com sucesso"}

# ==========================================
# RELACIONAMENTO MUITOS-PARA-MUITOS (PLAYLIST x MÚSICA)
# ==========================================

@app.get("/playlists/{playlist_id}/musicas")
def playlist_songs(playlist_id: int, db: Session = Depends(get_db)):
    p = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    return p.musicas

@app.get("/musicas/{musica_id}/playlists")
def song_playlists(musica_id: int, db: Session = Depends(get_db)):
    return db.query(Playlist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id).all()

# Vincular uma música a uma playlist
@app.post("/playlists/{playlist_id}/musicas/{musica_id}")
def adicionar_musica_na_playlist(playlist_id: int, musica_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    musica = db.query(Musica).filter(Musica.id == musica_id).first()
    
    if not playlist or not musica:
        raise HTTPException(status_code=404, detail="Playlist ou Música não encontrada")
        
    if musica in playlist.musicas:
        raise HTTPException(status_code=400, detail="Esta música já está nesta playlist")
        
    playlist.musicas.append(musica)
    db.commit()
    return {"mensagem": f"Música '{musica.nome}' adicionada à playlist '{playlist.nome}'"}

# Remover uma música de uma playlist
@app.delete("/playlists/{playlist_id}/musicas/{musica_id}")
def remover_musica_da_playlist(playlist_id: int, musica_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    musica = db.query(Musica).filter(Musica.id == musica_id).first()
    
    if not playlist or not musica:
        raise HTTPException(status_code=404, detail="Playlist ou Música não encontrada")
        
    if musica not in playlist.musicas:
        raise HTTPException(status_code=400, detail="Esta música não faz parte desta playlist")
        
    playlist.musicas.remove(musica)
    db.commit()
    return {"mensagem": f"Música '{musica.nome}' removida da playlist '{playlist.nome}'"}