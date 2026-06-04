import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const packageDefinition = protoLoader.loadSync('streaming.proto', { keepCase: true, longs: String, enums: String, defaults: true, oneofs: true });
const streamingProto = grpc.loadPackageDefinition(packageDefinition).streaming as any;

const server = new grpc.Server();

server.addService(streamingProto.StreamingService.service, {
  ListarUsuarios: async (_: any, callback: any) => {
    const u = await prisma.usuarios.findMany();
    callback(null, { usuarios: u });
  },
  ListarMusicas: async (_: any, callback: any) => {
    const m = await prisma.musicas.findMany();
    callback(null, { musicas: m });
  },
  ListarPlaylistsUsuario: async (call: any, callback: any) => {
    const p = await prisma.playlists.findMany({ where: { usuario_id: call.request.id } });
    callback(null, { playlists: p });
  },
  ListarMusicasPlaylist: async (call: any, callback: any) => {
    const d = await prisma.playlist_musica.findMany({ where: { playlist_id: call.request.id }, include: { musicas: true } });
    callback(null, { musicas: d.map(x => x.musicas) });
  },
  ListarPlaylistsPorMusica: async (call: any, callback: any) => {
    const d = await prisma.playlist_musica.findMany({ where: { musica_id: call.request.id }, include: { playlists: true } });
    callback(null, { playlists: d.map(x => x.playlists) });
  },
  CriarUsuario: async (call: any, callback: any) => {
    const { nome, idade } = call.request;
    const novo = await prisma.usuarios.create({ data: { nome, idade } });
    callback(null, novo);
  },
  CriarMusica: async (call: any, callback: any) => {
    const { nome, artista, album, compositor, ano_lancamento, genero, duracao } = call.request;
    const nova = await prisma.musicas.create({ data: { nome, artista, album: album || null, compositor: compositor || null, ano_lancamento: ano_lancamento || null, genero: genero || null, duracao: duracao || null } });
    callback(null, nova);
  },
  CriarPlaylist: async (call: any, callback: any) => {
    const { nome, usuario_id } = call.request;
    const nova = await prisma.playlists.create({ data: { nome, usuario_id } });
    callback(null, nova);
  },
  AtualizarUsuario: async (call: any, callback: any) => {
    const { id, nome, idade } = call.request;
    const atualizado = await prisma.usuarios.update({ where: { id }, data: { nome, idade } });
    callback(null, atualizado);
  },
  DeletarUsuario: async (call: any, callback: any) => {
    await prisma.usuarios.delete({ where: { id: call.request.id } });
    callback(null, {});
  },
  AtualizarMusica: async (call: any, callback: any) => {
    const { id, nome, artista, album, compositor, ano_lancamento, genero, duracao } = call.request;
    const atualizada = await prisma.musicas.update({ where: { id }, data: { nome, artista, album: album || null, compositor: compositor || null, ano_lancamento: ano_lancamento || null, genero: genero || null, duracao: duracao || null } });
    callback(null, atualizada);
  },
  DeletarMusica: async (call: any, callback: any) => {
    await prisma.musicas.delete({ where: { id: call.request.id } });
    callback(null, {});
  },
  AtualizarPlaylist: async (call: any, callback: any) => {
    const { id, nome, usuario_id } = call.request;
    const atualizada = await prisma.playlists.update({ where: { id }, data: { nome, usuario_id } });
    callback(null, atualizada);
  },
  DeletarPlaylist: async (call: any, callback: any) => {
    await prisma.playlists.delete({ where: { id: call.request.id } });
    callback(null, {});
  }
});

server.bindAsync('0.0.0.0:50052', grpc.ServerCredentials.createInsecure(), () => {
  server.start();
  console.log('TS gRPC rodando na 50052');
});