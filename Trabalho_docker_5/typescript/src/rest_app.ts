import express from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();

app.get('/usuarios', async (req, res) => {
    res.json(await prisma.usuarios.findMany());
});

app.get('/musicas', async (req, res) => {
    res.json(await prisma.musicas.findMany());
});

app.get('/usuarios/:id/playlists', async (req, res) => {
    res.json(await prisma.playlists.findMany({ where: { usuario_id: Number(req.params.id) } }));
});

app.get('/playlists/:id/musicas', async (req, res) => {
    const data = await prisma.playlist_musica.findMany({
        where: { playlist_id: Number(req.params.id) },
        include: { musicas: true }
    });
    res.json(data.map(d => d.musicas));
});

app.get('/musicas/:id/playlists', async (req, res) => {
    const data = await prisma.playlist_musica.findMany({
        where: { musica_id: Number(req.params.id) },
        include: { playlists: true }
    });
    res.json(data.map(d => d.playlists));
});

app.listen(9000, () => console.log('TS REST rodando na 9000'));