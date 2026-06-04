import express, { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();

app.use(express.json());

// ==========================================
// OPERAÇÕES DE CRUD: USUÁRIOS
// ==========================================

// GET: Listar todos os usuários
app.get('/usuarios', async (req: Request, res: Response) => {
  const usuarios = await prisma.usuarios.findMany();
  res.json(usuarios);
});

// GET: Buscar um usuário por ID
app.get('/usuarios/:user_id', async (req: Request, res: Response) => {
  const { user_id } = req.params;
  const usuario = await prisma.usuarios.findUnique({
    where: { id: Number(user_id) }
  });

  if (!usuario) {
    return res.status(404).json({ detail: 'Usuário não encontrado' });
  }
  res.json(usuario);
});

// POST: Criar um novo usuário
app.post('/usuarios', async (req: Request, res: Response) => {
  const { nome, idade } = req.body;
  const novoUsuario = await prisma.usuarios.create({
    data: { nome, idade: Number(idade) }
  });
  res.status(201).json(novoUsuario);
});

// PUT: Atualizar um usuário existente
app.put('/usuarios/:user_id', async (req: Request, res: Response) => {
  const { user_id } = req.params;
  const { nome, idade } = req.body;

  try {
    const usuarioAtualizado = await prisma.usuarios.update({
      where: { id: Number(user_id) },
      data: { nome, idade: Number(idade) }
    });
    res.json(usuarioAtualizado);
  } catch (error) {
    res.status(404).json({ detail: 'Usuário não encontrado' });
  }
});

// DELETE: Deletar um usuário
app.delete('/usuarios/:user_id', async (req: Request, res: Response) => {
  const { user_id } = req.params;

  try {
    await prisma.usuarios.delete({
      where: { id: Number(user_id) }
    });
    res.json({ mensagem: 'Usuário deletado com sucesso' });
  } catch (error) {
    res.status(404).json({ detail: 'Usuário não encontrado' });
  }
});

// ==========================================
// OPERAÇÕES DE CRUD: MÚSICAS
// ==========================================

// GET: Listar todas as músicas
app.get('/musicas', async (req: Request, res: Response) => {
  const musicas = await prisma.musicas.findMany();
  res.json(musicas);
});

// GET: Buscar uma música por ID
app.get('/musicas/:musica_id', async (req: Request, res: Response) => {
  const { musica_id } = req.params;
  const musica = await prisma.musicas.findUnique({
    where: { id: Number(musica_id) }
  });

  if (!musica) {
    return res.status(404).json({ detail: 'Música não encontrada' });
  }
  res.json(musica);
});

// POST: Criar uma nova música
app.post('/musicas', async (req: Request, res: Response) => {
  const { nome, artista, album, compositor, ano_lancamento, genero, duracao } = req.body;
  const novaMusica = await prisma.musicas.create({
    data: { nome, artista, album, compositor, ano_lancamento, genero, duracao }
  });
  res.status(201).json(novaMusica);
});

// PUT: Atualizar uma música existente
app.put('/musicas/:musica_id', async (req: Request, res: Response) => {
  const { musica_id } = req.params;
  const { nome, artista, album, compositor, ano_lancamento, genero, duracao } = req.body;

  try {
    const musicaAtualizada = await prisma.musicas.update({
      where: { id: Number(musica_id) },
      data: { nome, artista, album, compositor, ano_lancamento, genero, duracao }
    });
    res.json(musicaAtualizada);
  } catch (error) {
    res.status(404).json({ detail: 'Música não encontrada' });
  }
});

// DELETE: Deletar uma música
app.delete('/musicas/:musica_id', async (req: Request, res: Response) => {
  const { musica_id } = req.params;

  try {
    await prisma.musicas.delete({
      where: { id: Number(musica_id) }
    });
    res.json({ mensagem: 'Música deletada com sucesso' });
  } catch (error) {
    res.status(404).json({ detail: 'Música não encontrada' });
  }
});

// ==========================================
// OPERAÇÕES DE CRUD: PLAYLISTS
// ==========================================

// GET: Listar as playlists de um usuário específico
app.get('/usuarios/:user_id/playlists', async (req: Request, res: Response) => {
  const { user_id } = req.params;
  const playlists = await prisma.playlists.findMany({
    where: { usuario_id: Number(user_id) }
  });
  res.json(playlists);
});

// POST: Criar uma nova playlist
app.post('/playlists', async (req: Request, res: Response) => {
  const { nome, usuario_id } = req.body;

  const usuarioExiste = await prisma.usuarios.findUnique({
    where: { id: Number(usuario_id) }
  });

  if (!usuarioExiste) {
    return res.status(400).json({ detail: 'Usuário informado não existe' });
  }

  const novaPlaylist = await prisma.playlists.create({
    data: { nome, usuario_id: Number(usuario_id) }
  });
  res.status(201).json(novaPlaylist);
});

// PUT: Atualizar o nome de uma playlist
app.put('/playlists/:playlist_id', async (req: Request, res: Response) => {
  const { playlist_id } = req.params;
  const { nome } = req.body;

  try {
    const playlistAtualizada = await prisma.playlists.update({
      where: { id: Number(playlist_id) },
      data: { nome }
    });
    res.json(playlistAtualizada);
  } catch (error) {
    res.status(404).json({ detail: 'Playlist não encontrada' });
  }
});

// DELETE: Deletar uma playlist
app.delete('/playlists/:playlist_id', async (req: Request, res: Response) => {
  const { playlist_id } = req.params;

  try {
    await prisma.playlists.delete({
      where: { id: Number(playlist_id) }
    });
    res.json({ mensagem: 'Playlist deletada com sucesso' });
  } catch (error) {
    res.status(404).json({ detail: 'Playlist não encontrada' });
  }
});

// ==========================================
// RELACIONAMENTO MUITOS-PARA-MUITOS (PLAYLIST x MÚSICA)
// ==========================================

// GET: Listar todas as músicas de uma playlist específica
app.get('/playlists/:playlist_id/musicas', async (req: Request, res: Response) => {
  const { playlist_id } = req.params;

  const vinculos = await prisma.playlist_musica.findMany({
    where: { playlist_id: Number(playlist_id) },
    include: { musicas: true } // Traz o objeto da música associada
  });

  const musicas = vinculos.map((v: any) => v.musicas);
  res.json(musicas);
});

// GET: Listar em quais playlists uma música específica está inserida
app.get('/musicas/:musica_id/playlists', async (req: Request, res: Response) => {
  const { musica_id } = req.params;

  const vinculos = await prisma.playlist_musica.findMany({
    where: { musica_id: Number(musica_id) },
    include: { playlists: true }
  });

  const playlists = vinculos.map((v: any) => v.playlists);
  res.json(playlists);
});

// POST: Vincular uma música a uma playlist (Tabela intermediária)
app.post('/playlists/:playlist_id/musicas/:musica_id', async (req: Request, res: Response) => {
  const { playlist_id, musica_id } = req.params;

  const pId = Number(playlist_id);
  const mId = Number(musica_id);

  const playlist = await prisma.playlists.findUnique({ where: { id: pId } });
  const musica = await prisma.musicas.findUnique({ where: { id: mId } });

  if (!playlist || !musica) {
    return res.status(404).json({ detail: 'Playlist ou Música não encontrada' });
  }

  const jaExiste = await prisma.playlist_musica.findFirst({
    where: { playlist_id: pId, musica_id: mId }
  });

  if (jaExiste) {
    return res.status(400).json({ detail: 'Esta música já está nesta playlist' });
  }

  await prisma.playlist_musica.create({
    data: { playlist_id: pId, musica_id: mId }
  });

  res.json({ mensagem: `Música adicionada com sucesso` });
});

// DELETE: Remover uma música de uma playlist
app.delete('/playlists/:playlist_id/musicas/:musica_id', async (req: Request, res: Response) => {
  const { playlist_id, musica_id } = req.params;

  const pId = Number(playlist_id);
  const mId = Number(musica_id);

  const vinculo = await prisma.playlist_musica.findFirst({
    where: { playlist_id: pId, musica_id: mId }
  });

  if (!vinculo) {
    return res.status(400).json({ detail: 'Esta música não faz parte desta playlist' });
  }

  await prisma.playlist_musica.delete({
    where: {
      playlist_id_musica_id: { playlist_id: pId, musica_id: mId }
    }
  });

  res.json({ mensagem: `Música removida da playlist com sucesso` });
});

// Inicialização do servidor
app.listen(9000, () => {
  console.log('TS REST Server rodando na porta 9000');
});