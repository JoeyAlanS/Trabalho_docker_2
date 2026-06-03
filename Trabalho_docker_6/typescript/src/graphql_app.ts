import { ApolloServer, gql } from 'apollo-server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const typeDefs = gql`
  type Usuario { id: Int!, nome: String!, idade: Int }
  type Musica { id: Int!, nome: String!, artista: String! }
  type Playlist { id: Int!, nome: String!, usuario_id: Int! }

  type Query {
    usuarios: [Usuario]
    musicas: [Musica]
    playlistsUsuario(userId: Int!): [Playlist]
    musicasPlaylist(playlistId: Int!): [Musica]
    playlistsPorMusica(musicaId: Int!): [Playlist]
  }

  type Mutation {
    criarUsuario(nome: String!, idade: Int!): Usuario
    criarMusica(nome: String!, artista: String!): Musica
    criarPlaylist(nome: String!, usuario_id: Int!): Playlist
    atualizarUsuario(id: Int!, nome: String!, idade: Int!): Usuario
    deletarUsuario(id: Int!): Boolean
    atualizarMusica(id: Int!, nome: String!, artista: String!): Musica
    deletarMusica(id: Int!): Boolean
    atualizarPlaylist(id: Int!, nome: String!, usuario_id: Int!): Playlist
    deletarPlaylist(id: Int!): Boolean
  }
`;

const resolvers = {
  Query: {
    usuarios: () => prisma.usuarios.findMany(),
    musicas: () => prisma.musicas.findMany(),
    playlistsUsuario: (_: any, args: { userId: number }) => prisma.playlists.findMany({ where: { usuario_id: args.userId } }),
    musicasPlaylist: async (_: any, args: { playlistId: number }) => {
        const data = await prisma.playlist_musica.findMany({ where: { playlist_id: args.playlistId }, include: { musicas: true } });
        return data.map((d: any) => d.musicas);
    },
    playlistsPorMusica: async (_: any, args: { musicaId: number }) => {
        const data = await prisma.playlist_musica.findMany({ where: { musica_id: args.musicaId }, include: { playlists: true } });
        return data.map((d: any) => d.playlists);
    }
  },
  Mutation: {
    criarUsuario: async (_: any, args: { nome: string, idade: number }) => {
      return await prisma.usuarios.create({ data: { nome: args.nome, idade: args.idade } });
    },
    criarMusica: async (_: any, args: { nome: string, artista: string }) => {
      return await prisma.musicas.create({ data: { nome: args.nome, artista: args.artista } });
    },
    criarPlaylist: async (_: any, args: { nome: string, usuario_id: number }) => {
      return await prisma.playlists.create({ data: { nome: args.nome, usuario_id: args.usuario_id } });
    },
    atualizarUsuario: async (_: any, args: { id: number, nome: string, idade: number }) => {
      return await prisma.usuarios.update({ where: { id: args.id }, data: { nome: args.nome, idade: args.idade } });
    },
    deletarUsuario: async (_: any, args: { id: number }) => {
      await prisma.usuarios.delete({ where: { id: args.id } });
      return true;
    },
    atualizarMusica: async (_: any, args: { id: number, nome: string, artista: string }) => {
      return await prisma.musicas.update({ where: { id: args.id }, data: { nome: args.nome, artista: args.artista } });
    },
    deletarMusica: async (_: any, args: { id: number }) => {
      await prisma.musicas.delete({ where: { id: args.id } });
      return true;
    },
    atualizarPlaylist: async (_: any, args: { id: number, nome: string, usuario_id: number }) => {
      return await prisma.playlists.update({ where: { id: args.id }, data: { nome: args.nome, usuario_id: args.usuario_id } });
    },
    deletarPlaylist: async (_: any, args: { id: number }) => {
      await prisma.playlists.delete({ where: { id: args.id } });
      return true;
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 9001 }).then(({ url }) => {
  console.log(`TS GraphQL pronta em ${url}`);
});