from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List
# Importando as configurações novas do db.py
from db import SessionLocal, Usuario, Musica, Playlist, playlist_musica

app = FastAPI()

# ==========================================
# DEPENDÊNCIA DO BANCO DE DADOS (ASSÍNCRONA)
# ==========================================
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

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
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    return result.scalars().all()

@app.get("/usuarios/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.id == user_id))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def criar_usuario(user: UsuarioSchema, db: AsyncSession = Depends(get_db)):
    novo_usuario = Usuario(nome=user.nome, idade=user.idade)
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario

@app.put("/usuarios/{user_id}")
async def atualizar_usuario(user_id: int, user: UsuarioSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.id == user_id))
    usuario_db = result.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario_db.nome = user.nome
    usuario_db.idade = user.idade
    await db.commit()
    await db.refresh(usuario_db)
    return usuario_db

@app.delete("/usuarios/{user_id}")
async def deletar_usuario(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.id == user_id))
    usuario_db = result.scalars().first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    await db.delete(usuario_db)
    await db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}

# ==========================================
# OPERAÇÕES DE CRUD: MÚSICAS
# ==========================================

@app.get("/musicas")
async def list_songs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Musica))
    return result.scalars().all()

@app.get("/musicas/{musica_id}")
async def get_song(musica_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Musica).filter(Musica.id == musica_id))
    musica = result.scalars().first()
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return musica

@app.post("/musicas", status_code=status.HTTP_201_CREATED)
async def criar_musica(song: MusicaSchema, db: AsyncSession = Depends(get_db)):
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
    await db.commit()
    await db.refresh(nova_musica)
    return nova_musica

@app.put("/musicas/{musica_id}")
async def atualizar_musica(musica_id: int, song: MusicaSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Musica).filter(Musica.id == musica_id))
    musica_db = result.scalars().first()
    if not musica_db:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    musica_db.nome = song.nome
    musica_db.artista = song.artista
    musica_db.album = song.album
    musica_db.compositor = song.compositor
    musica_db.ano_lancamento = song.ano_lancamento
    musica_db.genero = song.genero
    musica_db.duracao = song.duracao
    await db.commit()
    await db.refresh(musica_db)
    return musica_db

@app.delete("/musicas/{musica_id}")
async def deletar_musica(musica_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Musica).filter(Musica.id == musica_id))
    musica_db = result.scalars().first()
    if not musica_db:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    await db.delete(musica_db)
    await db.commit()
    return {"mensagem": "Música deletada com sucesso"}

# ==========================================
# OPERAÇÕES DE CRUD: PLAYLISTS
# ==========================================

@app.get("/usuarios/{user_id}/playlists")
async def user_playlists(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).filter(Playlist.usuario_id == user_id))
    return result.scalars().all()

@app.post("/playlists", status_code=status.HTTP_201_CREATED)
async def criar_playlist(playlist: PlaylistCreateSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.id == playlist.usuario_id))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário informado não existe")
        
    nova_playlist = Playlist(nome=playlist.nome, usuario_id=playlist.usuario_id)
    db.add(nova_playlist)
    await db.commit()
    await db.refresh(nova_playlist)
    return nova_playlist

@app.put("/playlists/{playlist_id}")
async def atualizar_playlist(playlist_id: int, playlist: PlaylistUpdateSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).filter(Playlist.id == playlist_id))
    playlist_db = result.scalars().first()
    if not playlist_db:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    playlist_db.nome = playlist.nome
    await db.commit()
    await db.refresh(playlist_db)
    return playlist_db

@app.delete("/playlists/{playlist_id}")
async def deletar_playlist(playlist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).filter(Playlist.id == playlist_id))
    playlist_db = result.scalars().first()
    if not playlist_db:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    await db.delete(playlist_db)
    await db.commit()
    return {"mensagem": "Playlist deletada com sucesso"}

# ==========================================
# RELACIONAMENTO MUITOS-PARA-MUITOS
# ==========================================

@app.get("/playlists/{playlist_id}/musicas")
async def playlist_songs(playlist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playlist).filter(Playlist.id == playlist_id))
    p = result.scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    # No modo assíncrono, para carregar relacionamentos dinamicamente usa-se await
    # Esse método assume que o relacionamento está configurado corretamente no modelo (lazy='selectin' ou similar)
    return await p.awaitable_attrs.musicas if hasattr(p, 'awaitable_attrs') else p.musicas

@app.get("/musicas/{musica_id}/playlists")
async def song_playlists(musica_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Playlist).join(playlist_musica).filter(playlist_musica.c.musica_id == musica_id)
    )
    return result.scalars().all()

@app.post("/playlists/{playlist_id}/musicas/{musica_id}")
async def adicionar_musica_na_playlist(playlist_id: int, musica_id: int, db: AsyncSession = Depends(get_db)):
    res_p = await db.execute(select(Playlist).filter(Playlist.id == playlist_id))
    playlist = res_p.scalars().first()
    res_m = await db.execute(select(Musica).filter(Musica.id == musica_id))
    musica = res_m.scalars().first()
    
    if not playlist or not musica:
        raise HTTPException(status_code=404, detail="Playlist ou Música não encontrada")
    
    # Carrega as músicas existentes de forma segura
    musicas_atuais = await playlist.awaitable_attrs.musicas if hasattr(playlist, 'awaitable_attrs') else playlist.musicas
    if musica in musicas_atuais:
        raise HTTPException(status_code=400, detail="Esta música já está nesta playlist")
        
    musicas_atuais.append(musica)
    await db.commit()
    return {"mensagem": f"Música '{musica.nome}' adicionada à playlist '{playlist.nome}'"}

@app.delete("/playlists/{playlist_id}/musicas/{musica_id}")
async def remover_musica_da_playlist(playlist_id: int, musica_id: int, db: AsyncSession = Depends(get_db)):
    res_p = await db.execute(select(Playlist).filter(Playlist.id == playlist_id))
    playlist = res_p.scalars().first()
    res_m = await db.execute(select(Musica).filter(Musica.id == musica_id))
    musica = res_m.scalars().first()
    
    if not playlist or not musica:
        raise HTTPException(status_code=404, detail="Playlist ou Música não encontrada")
        
    musicas_atuais = await playlist.awaitable_attrs.musicas if hasattr(playlist, 'awaitable_attrs') else playlist.musicas
    if musica not in musicas_atuais:
        raise HTTPException(status_code=400, detail="Esta música não faz parte desta playlist")
        
    musicas_atuais.remove(musica)
    await db.commit()
    return {"mensagem": f"Música '{musica.nome}' removida da playlist '{playlist.nome}'"}