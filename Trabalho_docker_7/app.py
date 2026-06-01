import os
import random
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Modo não-interativo para rodar dentro do Docker
import matplotlib.pyplot as plt

app = FastAPI(title="Descentralized P2P Simulator")

class SearchRequest(BaseModel):
    node_id: str
    resource_id: str
    ttl: int
    algo: str  # flooding, informed_flooding, random_walk, informed_random_walk

class P2PNetwork:
    def __init__(self, config_path: str):
        self.graph = nx.Graph()
        self.num_nodes = 0
        self.min_neighbors = 0
        self.max_neighbors = 0
        self.resources = {}
        self._load_and_validate(config_path)

    def _load_and_validate(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at {path}")

        with open(path, 'r') as f:
            lines = f.readlines()

        mode = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("num_nodes:"):
                self.num_nodes = int(line.split(":")[1].strip())
            elif line.startswith("min_neighbors:"):
                self.min_neighbors = int(line.split(":")[1].strip())
            elif line.startswith("max_neighbors:"):
                self.max_neighbors = int(line.split(":")[1].strip())
            elif line.startswith("resources:"):
                mode = "resources"
            elif line.startswith("edges:"):
                mode = "edges"
            elif mode == "resources" and ":" in line:
                node, res_str = line.split(":", 1)
                res_list = [r.strip() for r in res_str.split(",") if r.strip()]
                self.resources[node.strip()] = res_list
            elif mode == "edges" and "," in line:
                u, v = line.split(",", 1)
                self.graph.add_edge(u.strip(), v.strip())

        # Adiciona nós isolados que possuem recursos mas podem não ter arestas inicialmente
        for node, res in self.resources.items():
            self.graph.add_node(node, resources=res, cache={})

        self._validate_constraints()

    def _validate_constraints(self):
        # 1. Verificação de arestas para si mesmo (Self-loops)
        if len(list(nx.selfloop_edges(self.graph))) > 0:
            raise ValueError("Validation Failed: Self-loops are not allowed.")

        # 2. Rede não pode estar particionada (Deve ser conexa)
        if not nx.is_connected(self.graph):
            raise ValueError("Validation Failed: The network is partitioned (disconnected).")

        # 3. Validação de recursos por nó
        for node in self.graph.nodes:
            res = self.graph.nodes[node].get('resources', [])
            if not res:
                raise ValueError(f"Validation Failed: Node {node} has no resources.")

        # 4. Limites de vizinhos (Grau dos nós)
        for node in self.graph.nodes:
            degree = self.graph.degree(node)
            if degree < self.min_neighbors or degree > self.max_neighbors:
                raise ValueError(f"Validation Failed: Node {node} degree ({degree}) out of bounds [{self.min_neighbors}, {self.max_neighbors}].")

    def simulate_search(self, start_node: str, resource_id: str, ttl: int, algo: str):
        if start_node not in self.graph:
            return {"error": "Start node not found"}

        # Verificação local imediata
        if resource_id in self.graph.nodes[start_node].get('resources', []):
            return {"found": True, "messages": 0, "nodes_involved": 1, "path_taken": [start_node]}

        # Inicialização de métricas
        messages_count = 0
        nodes_involved = {start_node}
        found = False
        found_at = None

        # Mecanismo de Busca Informada no nó de origem
        if "informed" in algo and resource_id in self.graph.nodes[start_node].get('cache', {}):
            target = self.graph.nodes[start_node]['cache'][resource_id]
            messages_count += 1
            nodes_involved.add(target)
            if resource_id in self.graph.nodes[target].get('resources', []):
                return {"found": True, "messages": messages_count, "nodes_involved": len(nodes_involved)}

        # Execução dos algoritmos estruturados
        if "flooding" in algo:
            # Queue para BFS: (nó_atual, pai, ttl_restante)
            queue = [(start_node, None, ttl)]
            seen_nodes = {start_node}

            while queue and not found:
                next_queue = []
                for curr, parent, current_ttl in queue:
                    if resource_id in self.graph.nodes[curr].get('resources', []):
                        found = True
                        found_at = curr
                        break

                    if "informed" in algo and resource_id in self.graph.nodes[curr].get('cache', {}):
                        target = self.graph.nodes[curr]['cache'][resource_id]
                        messages_count += 1
                        nodes_involved.add(target)
                        if resource_id in self.graph.nodes[target].get('resources', []):
                            found = True
                            found_at = target
                            break

                    if current_ttl <= 0:
                        continue

                    for neighbor in self.graph.neighbors(curr):
                        if neighbor == parent:
                            continue
                        messages_count += 1
                        nodes_involved.add(neighbor)

                        if neighbor not in seen_nodes:
                            seen_nodes.add(neighbor)
                            next_queue.append((neighbor, curr, current_ttl - 1))
                if found:
                    break
                queue = next_queue

        elif "random_walk" in algo:
            curr = start_node
            parent = None
            current_ttl = ttl

            while current_ttl > 0 and not found:
                neighbors = list(self.graph.neighbors(curr))
                available = [n for n in neighbors if n != parent]
                if not available: 
                    available = neighbors
                
                next_node = random.choice(available)
                messages_count += 1
                nodes_involved.add(next_node)

                if resource_id in self.graph.nodes[next_node].get('resources', []):
                    found = True
                    found_at = next_node
                    break

                if "informed" in algo and resource_id in self.graph.nodes[next_node].get('cache', {}):
                    target = self.graph.nodes[next_node]['cache'][resource_id]
                    messages_count += 1
                    nodes_involved.add(target)
                    if resource_id in self.graph.nodes[target].get('resources', []):
                        found = True
                        found_at = target
                        break

                parent = curr
                curr = next_node
                current_ttl -= 1

        # Atualização retroativa do cache local dos nós envolvidos
        if found and found_at:
            for node in nodes_involved:
                if node != found_at:
                    self.graph.nodes[node]['cache'][resource_id] = found_at

        return {
            "found": found,
            "messages": messages_count,
            "nodes_involved": len(nodes_involved),
            "target_node": found_at if found else None
        }

# Instanciação global da rede
p2p_net = P2PNetwork("network_config.txt")

@app.post("/search")
def run_p2p_search(req: SearchRequest):
    if req.algo not in ["flooding", "informed_flooding", "random_walk", "informed_random_walk"]:
        raise HTTPException(status_code=400, detail="Algoritmo inválido.")
    result = p2p_net.simulate_search(req.node_id, req.resource_id, req.ttl, req.algo)
    return result

@app.get("/graph")
def get_graph_image():
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(p2p_net.graph)
    nx.draw(p2p_net.graph, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', font_size=10, font_weight='bold')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return StreamingResponse(buf, media_type="image/png")