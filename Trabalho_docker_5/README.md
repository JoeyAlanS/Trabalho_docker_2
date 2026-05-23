Resolve over-fetching/under-fetching, fortemente tipado, excelente para front-ends complexos.
* **Desvantagens:** Caching HTTP é difícil (tudo é POST), consultas maliciosas ou complexas podem derrubar o servidor se não houver limites.

### gRPC (gRPC Remote Procedure Calls)
* **Origem:** Desenvolvido pelo Google em 2015 (baseado em sua infraestrutura interna chamada Stubby).
* **Características:** Framework RPC de alta performance. Usa HTTP/2 por padrão e Protocol Buffers (Protobuf) como linguagem de descrição de interface (IDL) e formato de serialização binária.
* **Vantagens:** Extremamente rápido (binário vs texto do JSON/XML), suporte nativo a streaming bidirecional, código do cliente/servidor gerado automaticamente.
* **Desvantagens:** Não é legível por humanos (dados binários), difícil de testar diretamente do navegador (requer gRPC-Web), acoplamento mais forte entre cliente/servidor via `.proto`.

---

## 2. Análise Crítica e Testes de Carga

Na implementação deste serviço de streaming (Usuários, Músicas, Playlists), observamos as seguintes nuances:

1.  **Desenvolvimento:** REST foi o mais rápido de prototipar. GraphQL exigiu a criação de schemas explícitos, mas facilitou consultas aninhadas (ex: Playlists e suas Músicas). gRPC exigiu a compilação prévia do arquivo `.proto`. SOAP exigiu uma biblioteca robusta (Spyne) e a tipagem estrita pode ser engessada.
2.  **Testes de Carga (Locust):**
    * **gRPC** apresenta a menor latência e maior Throughput sob alta carga devido à serialização binária (Protobuf) e multiplexação do HTTP/2.
    * **REST e GraphQL** apresentam desempenho similar em chamadas simples, mas GraphQL sofre um leve overhead de validação do schema no servidor. Para consultas complexas que em REST exigiriam múltiplos GETs, GraphQL é muito superior.
    * **SOAP** apresenta o pior desempenho sob carga máxima devido ao peso do payload XML e ao processamento de parse no servidor.

---

## 3. Como rodar o projeto

O projeto utiliza Docker Compose para subir os 4 serviços e o banco de dados SQLite (compartilhado em volume).