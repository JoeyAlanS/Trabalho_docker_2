# Comparativo de APIs - Arquitetura de Microsserviços

## Sobre o Projeto

Este projeto tem como objetivo avaliar, comparar e demonstrar o funcionamento de quatro paradigmas diferentes de comunicação de APIs: **REST, GraphQL, SOAP e gRPC**. Para garantir uma base de comparação justa e ampla, cada um desses paradigmas foi implementado em duas linguagens/ambientes distintos: **Python** e **TypeScript (Node.js)**.

O domínio da aplicação simula um serviço de streaming básico, gerenciando entidades como Usuários, Músicas e Playlists. Todo o ecossistema é conteinerizado usando Docker, garantindo que o banco de dados, as APIs e as ferramentas de teste de carga (Locust) rodem de forma isolada e previsível.

---

## Estrutura do Projeto

```
Trabalho_docker_5/
├── docker-compose.yml          # Orquestração de containers
├── init.sql                    # Script inicial do banco de dados
├── streaming.proto             # Definição de mensagens gRPC
├── .gitignore                  # Configuração de versionamento
├── README.md                   # Este arquivo
│
├── python/                     # Implementações em Python
│   ├── Dockerfile              # Imagem Docker para APIs Python
│   ├── requirements.txt         # Dependências Python (pip)
│   ├── db.py                   # Utilitários de conexão com banco de dados
│   ├── seed.py                 # Script para popular banco com dados iniciais
│   ├── rest_app.py             # API REST (FastAPI)
│   ├── graphql_app.py          # API GraphQL (Strawberry)
│   ├── soap_app.py             # API SOAP (Spyne)
│   ├── grpc_app.py             # API gRPC (grpcio)
│   └── locustfile.py           # Testes de carga (Locust)
│
├── typescript/                 # Implementações em TypeScript
│   ├── Dockerfile              # Imagem Docker para APIs TypeScript
│   ├── package.json            # Dependências Node.js (npm)
│   ├── tsconfig.json           # Configuração do TypeScript
│   ├── prisma/
│   │   └── schema.prisma       # Schema de banco de dados (Prisma ORM)
│   └── src/
│       ├── rest_app.ts         # API REST (Express)
│       ├── graphql_app.ts      # API GraphQL (Apollo Server)
│       ├── soap_app.ts         # API SOAP (módulo soap)
│       └── grpc_app.ts         # API gRPC (@grpc/grpc-js)
│
└── data/                       # Pasta para dados (ex: banco SQLite se usado)
    └── streaming.db            # Banco de dados SQLite (gerado, não versionado)
```

---

## Arquitetura e Tecnologias

### Stack Tecnológico

- **Banco de Dados:** PostgreSQL 15 (com PgAdmin para interface gráfica)
- **Python:** FastAPI (REST), Strawberry (GraphQL), Spyne (SOAP), grpcio (gRPC)
- **TypeScript:** Express (REST), Apollo Server (GraphQL), módulo soap (SOAP), @grpc/grpc-js (gRPC)
- **Testes de Carga:** Locust (escrito em Python)
- **Infraestrutura:** Docker e Docker Compose

---

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter instalado:
- **Docker** (v20.10+)
- **Docker Compose** (v1.29+)

### Passos para Inicialização

1. Navegue até a pasta raiz do projeto (onde está o `docker-compose.yml`):

```bash
cd Trabalho_docker_6
```

2. Execute o comando de construção e inicialização:

```bash
docker-compose up -d --build
```

O parâmetro `-d` executa os containers em segundo plano. Aguarde a conclusão do download das imagens e a inicialização.

3. Popule o banco de dados com dados de teste:

```bash
docker-compose exec rest_py python seed.py
```

### Para Parar a Aplicação

```bash
docker-compose down
```

### Para Remover Volumes (Banco de Dados)

```bash
docker-compose down -v
```

---

## Mapeamento de Serviços e Portas

| Serviço                     | Linguagem | Porta Local | Host Interno (Docker)      | Descrição |
| ---------------------------- | --------- | ------------ | -------------------------- | --------- |
| **Banco de Dados**          | -         | 5432         | `db:5432`                 | PostgreSQL 15 |
| **PgAdmin**                 | -         | 5050         | `http://localhost:5050`   | Interface gráfica do PostgreSQL |
| **Locust**                  | Python    | 8089         | `http://localhost:8089`   | Ferramenta de testes de carga |
| **API REST**                | Python    | 8000         | `http://rest_py:8000`     | FastAPI |
| **API GraphQL**             | Python    | 8001         | `http://graphql_py:8001`  | Strawberry GraphQL |
| **API SOAP**                | Python    | 8002         | `http://soap_py:8002`     | Spyne SOAP |
| **API gRPC**                | Python    | 50051        | `grpc_py:50051`           | gRPC (Protocol Buffers) |
| **API REST**                | TypeScript| 9000         | `http://rest_ts:9000`     | Express.js |
| **API GraphQL**             | TypeScript| 9001         | `http://graphql_ts:9001`  | Apollo Server |
| **API SOAP**                | TypeScript| 9002         | `http://soap_ts:9002`     | módulo soap |
| **API gRPC**                | TypeScript| 50052        | `grpc_ts:50052`           | @grpc/grpc-js |

---

## Documentação dos Endpoints

### 1. APIs REST

As APIs REST retornam dados em formato JSON. Podem ser acessadas pelo navegador, Postman, cURL ou qualquer cliente HTTP.

#### Endpoints Base

- **Python:** `http://localhost:8000`
- **TypeScript:** `http://localhost:9000`

#### Endpoints Principais

```http
GET /usuarios
```
Retorna lista de todos os usuários.

**Response:**
```json
[
  { "id": 1, "nome": "João", "idade": 30 },
  { "id": 2, "nome": "Maria", "idade": 28 }
]
```

```http
GET /musicas
```
Retorna lista de todas as músicas.

```http
GET /playlists
```
Retorna lista de todas as playlists.

```http
GET /playlists/:id/musicas
```
Retorna músicas de uma playlist específica.

---

### 2. APIs GraphQL

O GraphQL opera em um único endpoint, recebendo queries customizadas para retornar apenas os dados solicitados.

#### Endpoints

- **Python:** `POST http://localhost:8001/graphql`
- **TypeScript:** `POST http://localhost:9001/`

#### Exemplos de Queries

**Listar Usuários:**
```graphql
query {
  usuarios {
    id
    nome
    idade
  }
}
```

**Listar Playlists com Músicas:**
```graphql
query {
  playlists {
    id
    nome
    usuarioId
    musicas {
      id
      nome
      artista
    }
  }
}
```

**Payload JSON a enviar:**
```json
{
  "query": "query { usuarios { id nome idade } }"
}
```

---

### 3. APIs SOAP

As APIs SOAP utilizam formato XML para comunicação e requerem cabeçalhos específicos.

#### Endpoints

- **Python:** `POST http://localhost:8002/`
- **TypeScript:** `POST http://localhost:9002/`

#### Cabeçalhos Necessários

```http
Content-Type: text/xml; charset=utf-8
SOAPAction: "listar_usuarios"
```

#### Exemplo de Envelope SOAP

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://streaming.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:listar_usuarios/>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Operações Disponíveis

- `listar_usuarios`
- `listar_musicas`
- `listar_playlists_usuario` (requer `usuario_id`)
- `listar_musicas_playlist` (requer `playlist_id`)

---

### 4. APIs gRPC

O gRPC utiliza HTTP/2 e Protocol Buffers para serialização binária. Não opera sobre HTTP/1.1 tradicional.

#### Endpoints

- **Python:** `localhost:50051`
- **TypeScript:** `localhost:50052`

#### Definição de Serviço (streaming.proto)

```protobuf
service StreamingService {
  rpc ListarUsuarios(Empty) returns (UsuarioList);
  rpc ListarMusicas(Empty) returns (MusicaList);
  rpc ListarPlaylistsUsuario(IdRequest) returns (PlaylistList);
  rpc ListarMusicasPlaylist(IdRequest) returns (MusicaList);
  rpc ListarPlaylistsPorMusica(IdRequest) returns (PlaylistList);
}
```

#### Ferramentas Recomendadas para Testar

- **BloomRPC** - Interface gráfica para gRPC
- **Postman** (v9.7+) - Suporte experimental para gRPC
- **grpcurl** - Cliente CLI para gRPC
- **Insomnia** - Alternative com suporte gRPC

---

## Testes de Desempenho (Locust)

O projeto inclui o Locust para testes de carga, permitindo analisar a performance, latência e taxa de erros de cada API.

### Acesso ao Painel

```
http://localhost:8089
```

### Fluxo de Execução

1. Abra o navegador em `http://localhost:8089`
2. Configure:
   - **Number of users:** total de usuários virtuais
   - **Spawn rate:** usuários criados por segundo
   - **Host:** deixe em branco (URLs já estão configuradas no `locustfile.py`)
3. Clique em **Start swarming**
4. Monitore as métricas em tempo real

### Personalizando os Testes

O arquivo `python/locustfile.py` define as requisições usando decorators `@task`. Para testar apenas endpoints específicos:

```python
# Descomente apenas os testes desejados
@task
def test_rest():
    pass

# @task
# def test_graphql():
#     pass
```

Reinicie o container do Locust após fazer alterações:

```bash
docker-compose restart locust
```

---

## Análise de Resultados

### Comparativo Esperado

Com base na arquitetura, esperamos observar:

#### Tempo de Resposta (Latência)

| Paradigma | Python (ms) | TypeScript (ms) | Observações |
| --------- | ----------- | --------------- | ----------- |
| **REST**  | ~50         | ~40             | Mais rápido em consultas simples |
| **GraphQL**| ~60        | ~45             | Overhead de validação do schema |
| **SOAP**  | ~80         | ~70             | Parsing de XML adiciona latência |
| **gRPC**  | ~30         | ~25             | Mais rápido (binário + HTTP/2) |

#### Taxa de Transferência (Throughput)

- **gRPC:** Melhor performance sob alta carga
- **REST/GraphQL:** Performance similar
- **SOAP:** Menor throughput

#### Tamanho do Payload

Para recuperar 100 usuários:

| Formato | Tamanho (KB) |
| ------- | ------------ |
| REST (JSON) | ~2.5 |
| GraphQL (JSON) | ~2.5 |
| SOAP (XML) | ~8.0 |
| gRPC (Protobuf) | ~0.8 |

#### Consumo de Recursos

- **CPU:** gRPC < REST < GraphQL < SOAP
- **Memória:** Similares entre REST e GraphQL; SOAP consome mais

---

## Análise Crítica e Testes de Carga

Na implementação deste serviço de streaming (Usuários, Músicas, Playlists), observamos as seguintes nuances:

1.  **Desenvolvimento:** REST foi o mais rápido de prototipar. GraphQL exigiu a criação de schemas explícitos, mas facilitou consultas aninhadas (ex: Playlists e suas Músicas). gRPC exigiu a compilação prévia do arquivo `.proto`. SOAP exigiu uma biblioteca robusta (Spyne) e a tipagem estrita pode ser engessada.
2.  **Testes de Carga (Locust):**
    * **gRPC** apresenta a menor latência e maior Throughput sob alta carga devido à serialização binária (Protobuf) e multiplexação do HTTP/2.
    * **REST e GraphQL** apresentam desempenho similar em chamadas simples, mas GraphQL sofre um leve overhead de validação do schema no servidor. Para consultas complexas que em REST exigiriam múltiplos GETs, GraphQL é muito superior.
    * **SOAP** apresenta o pior desempenho sob carga máxima devido ao peso do payload XML e ao processamento de parse no servidor.

---

## Banco de Dados

### Schema

O banco é inicializado automaticamente com o arquivo `init.sql`:

- **usuarios** - Usuários do sistema
- **musicas** - Catálogo de músicas
- **playlists** - Playlists de usuários
- **playlist_musica** - Relação N-para-N entre playlists e músicas

### Acesso ao PgAdmin

- **URL:** `http://localhost:5050`
- **Email:** `admin@admin.com`
- **Senha:** `password`

---

