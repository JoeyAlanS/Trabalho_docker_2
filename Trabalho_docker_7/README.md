# P2P Descentralizado - Simulador de Rede

## Descrição

Simulador de rede **P2P (Peer-to-Peer) descentralizada** que implementa diferentes algoritmos de busca em uma rede de nós. O projeto testa como os nós encontram recursos distribuídos em uma topologia de rede usando estratégias como **flooding** (inundação) e **random walk** (caminho aleatório).

## Funcionalidades

- **4 Algoritmos de Busca:**
  - `flooding`: Propaga a busca para todos os vizinhos (BFS)
  - `informed_flooding`: Flooding com cache de informações
  - `random_walk`: Caminha aleatoriamente pela rede
  - `informed_random_walk`: Random walk com cache inteligente

- **Validações de Rede:**
  - Sem auto-conexões (self-loops)
  - Rede conectada (não particionada)
  - Cada nó possui recursos
  - Grau dos nós dentro dos limites configuráveis

- **Testes de Carga:** Integrado com Locust para simular até 50 usuários concorrentes

## Arquitetura da Rede

A rede é composta por **12 nós** com conexões predefinidas:

```
       n7
      /   \
    n5      n9
   / |      |
 n2  |      n11
 |   |     /
n1-n3-n6  /
 |     | /
n12----n10
 |
n4
 |
n8
```

**Configuração:**
- Nós: n1 a n12
- Grau mínimo: 2 | Grau máximo: 4
- Recursos distribuídos: r1 a r10

## Como Usar

### Opção 1: Docker Compose (Recomendado)

```bash
docker-compose up --build
```

Isso iniciará:
- Servidor P2P na porta `8000`
- Interface Locust na porta `8089`

### Opção 2: Execução Local

```bash
pip install fastapi uvicorn networkx matplotlib pydantic locust
python app.py
```

## API Endpoints

### POST `/search` - Buscar um Recurso

**Request:**
```json
{
  "node_id": "n1",
  "resource_id": "r5",
  "ttl": 3,
  "algo": "flooding"
}
```

**Response:**
```json
{
  "found": true,
  "messages": 4,
  "nodes_involved": 3,
  "target_node": "n7"
}
```

### GET `/graph` - Visualizar a Rede

Retorna uma imagem PNG do grafo da rede.

## Resultados de Performance

Teste com **50 usuários concorrentes** (0.5s ramp-up, 2 minutos):
- **Requisições totais:** 6.438
- **Tempo mediano:** 4ms
- **Taxa de erro:** 0%

## Estrutura do Projeto

```
├── app.py                    # Servidor FastAPI e lógica P2P
├── locustfile.py             # Testes de carga com Locust
├── network_config.txt        # Configuração da topologia
├── docker-compose.yml        # Orquestração de containers
├── Dockerfile                # Build da imagem
├── csv/                      # Resultados dos testes
├── graph/                    # Imagens dos grafos gerados
└── README.md                 # Este arquivo
```

## Configuração da Rede

Edite `network_config.txt`:

```
num_nodes: 12
min_neighbors: 2
max_neighbors: 4
resources:
  n1: r1, r2, r3
  n2: r4, r5
  ...
edges:
  n1, n2
  n1, n3
  ...
```

## Métricas Coletadas

Para cada busca, o sistema retorna:
- `found`: Se o recurso foi localizado
- `messages`: Número de mensagens trocadas
- `nodes_involved`: Quantidade de nós visitados
- `target_node`: Nó onde o recurso foi encontrado