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
  }
});

server.bindAsync('0.0.0.0:50052', grpc.ServerCredentials.createInsecure(), () => {
  server.start();
  console.log('TS gRPC rodando na 50052');
});