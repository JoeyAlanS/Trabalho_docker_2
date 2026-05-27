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
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 9001 }).then(({ url }) => {
  console.log(`TS GraphQL pronta em ${url}`);
});