CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT
);

CREATE TABLE musicas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    artista VARCHAR(100) NOT NULL,
    album VARCHAR(150),
    compositor VARCHAR(255),
    ano_lancamento INT,
    genero VARCHAR(50),
    duracao INT
);

CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE playlist_musica (
    playlist_id INT REFERENCES playlists(id) ON DELETE CASCADE,
    musica_id INT REFERENCES musicas(id) ON DELETE CASCADE,
    PRIMARY KEY (playlist_id, musica_id)
);