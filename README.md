# Trabalho Docker - Projetos em Container

Este repositório contém uma coleção de projetos Docker, cada um abordando diferentes aspectos de containerização, orquestração, testes de carga e arquitetura de microsserviços.

## Estrutura do Repositório

### Trabalho_docker_2
**WordPress com Balanceamento de Carga (Nginx)**

Implementação de uma arquitetura balanceada com:
- 1 container **Nginx** como balanceador de carga
- 3 containers **WordPress** com PHP 7.2 Apache
- 1 container **MySQL** 5.7 como banco de dados compartilhado

O Nginx distribui as requisições entre as instâncias do WordPress usando round-robin, com todos os containers compartilhando o mesmo banco de dados. O cabeçalho `X-Upstream` alterna entre os IP dos containers (172.18.0.3:80, 172.18.0.4:80, 172.18.0.5:80), comprovando o funcionamento do balanceamento.

```bash
cd Trabalho_docker_2
docker-compose up -d
curl -I http://localhost/
```

---

### Trabalho_docker_3
**Análise de Performance - Testes de Carga com Locust**

Projeto focado em testes de carga abrangentes de uma aplicação WordPress usando **Locust** (framework Python). Avalia comportamento sob diferentes cargas variando:
- Número de instâncias: 1, 2 ou 3
- Quantidade de usuários: 100, 300, 450 ou 600
- Tamanho de conteúdo: 4 cenários diferentes (imagens 1MB, 400KB, 300KB, híbrido)

**Métricas coletadas:**
- RPS (Requisições por Segundo)
- Tempo de resposta (mediano e P95)
- Taxa de falha (%)

**Resultados:**
- Cenário 3 (imagem 300KB) oferece melhor relação qualidade/performance
- Cenário 1 (imagem 1MB) não recomendado em produção
- 3 instâncias suportam até 700 usuários com performance aceitável

```bash
cd Trabalho_docker_3
docker-compose up -d
# Testes de carga com Locust em locust/
```

---

### Trabalho_docker_4
**Link Extractor - Testes de Desempenho (Python vs Ruby com Redis)**

Comparação de performance entre implementações em **Python (Flask)** e **Ruby (Sinatra)**, com e sem cache **Redis**.

**4 Cenários de teste:**
1. Python + Redis (cache)
2. Python sem cache
3. Ruby + Redis (cache)
4. Ruby sem cache

**Parâmetros dos testes:**
- Ramp-up: 3 segundos
- Cargas: 100, 200, 600 usuários virtuais
- Duração: 5 minutos por teste
- Ferramenta: K6

**Conclusões principais:**
- Cache Redis reduz taxa de falha de 36% (Ruby sem cache) para 6% (Ruby com cache)
- Python com cache mantém taxa de falha ~0%
- Python mais eficiente em saturação

```bash
cd Trabalho_docker_4
docker-compose -f docker-compose.python-cache.yml up -d
# Outras variantes: docker-compose.python-no-cache.yml, docker-compose.ruby-*.yml
```

---

### Trabalho_docker_6
**Comparativo de APIs - Arquitetura de Microsserviços**

Implementação de 4 paradigmas diferentes de comunicação de APIs em 2 linguagens:
- **Linguagens:** Python e TypeScript (Node.js)
- **Paradigmas:** REST, GraphQL, SOAP, gRPC

Simula um serviço de streaming (Usuários, Músicas, Playlists) totalmente containerizado com:
- **Python:** FastAPI (REST), Strawberry (GraphQL), Spyne (SOAP), grpcio (gRPC)
- **TypeScript:** Express (REST), Apollo Server (GraphQL), soap (SOAP), @grpc/grpc-js (gRPC)
- **Banco de dados:** MySQL
- **Testes:** Locust para carga

```bash
cd Trabalho_docker_6
docker-compose up -d
# APIs rodam em portas diferentes conforme paradigma
```

---

### Trabalho_docker_7
**P2P Descentralizado - Simulador de Rede**

Simulador de rede **Peer-to-Peer descentralizada** com diferentes algoritmos de busca:
- **flooding:** Propaga busca para todos os vizinhos (BFS)
- **informed_flooding:** Flooding com cache inteligente
- **random_walk:** Caminha aleatoriamente pela rede
- **informed_random_walk:** Random walk com cache

**Características:**
- 12 nós na rede com topologia pré-definida
- Algoritmos de busca de recursos distribuídos
- Testes de carga com Locust (até 50 usuários simultâneos)
- Validação de conectividade e ausência de partições

```bash
cd Trabalho_docker_7
docker-compose up -d
python locustfile.py
```

---

## Requisitos Gerais

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 1.29+)
- **Python 3.8+** (para testes de carga com Locust)

## Como Executar Cada Projeto

Cada pasta possui seu próprio `docker-compose.yml` e pode ser executada independentemente:

```bash
# Entrar na pasta do projeto
cd Trabalho_docker_X

# Iniciar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Parar containers
docker-compose down
```

## Visualização de Dados

Alguns projetos geram gráficos e relatórios:
- **Trabalho_docker_3:** Gráficos em `csv/` e `output_graphs/`
- **Trabalho_docker_4:** Gráficos de comparação em `output_graphs/`
- **Trabalho_docker_6:** Relatórios de teste em `results/`

## Notas Importantes

- Cada projeto é **independente** e pode rodar isoladamente
- Alguns projetos compartilham portas (ex: 5000, 3000) - não execute em paralelo
- Volumes e dados persistem após `docker-compose down` (verificar em `data/`)
- Para limpar completamente: `docker-compose down -v`
