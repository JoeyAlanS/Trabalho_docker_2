import time
import grpc
from locust import HttpUser, task, between, events
import streaming_pb2
import streaming_pb2_grpc

# ==========================================
# CONFIGURAÇÃO DE HOSTS
# ==========================================
HOST_REST_PY = "http://rest_py:8000"     
HOST_REST_TS = "http://rest_ts:9000"       
HOST_GRAPHQL_PY = "http://graphql_py:8001"
HOST_GRAPHQL_TS = "http://graphql_ts:9001"
HOST_SOAP_PY = "http://soap_py:8002"
HOST_SOAP_TS = "http://soap_ts:9002"
HOST_GRPC_PY = "grpc_py:50051"
HOST_GRPC_TS = "grpc_ts:50052"            

# ==========================================
# 1. TESTE REST
# ==========================================
class Teste_1_REST(HttpUser):
    abstract = True  # Descomente esta linha para desativar o REST
    wait_time = between(0.1, 0.5)

    #@task
    def rest_python(self):
        with self.client.get(f"{HOST_REST_PY}/musicas", name="1. REST (PY) - Músicas", catch_response=True) as res:
            if res.status_code == 200:
                res.success()
                res.request_meta["response_length"] = len(res.content)
            else:
                res.failure(f"Erro PY HTTP {res.status_code}")

    #@task
    def rest_typescript(self):
        with self.client.get(f"{HOST_REST_TS}/musicas", name="1. REST (TS) - Músicas", catch_response=True) as res:
            if res.status_code == 200:
                res.success()
                res.request_meta["response_length"] = len(res.content)
            else:
                res.failure(f"Erro TS HTTP {res.status_code}")


# ==========================================
# 2. TESTE GRAPHQL
# ==========================================
class Teste_2_GraphQL(HttpUser):
    abstract = True  # Comente esta linha para ATIVAR o GraphQL
    wait_time = between(0.1, 0.5)
    
    payload = {"query": "query { musicas { id nome artista album compositor anoLancamento genero duracao } }"}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    @task
    def graphql_python(self):
        with self.client.post(f"{HOST_GRAPHQL_PY}/graphql", json=self.payload, headers=self.headers, name="2. GraphQL (PY) - Músicas", catch_response=True) as res_py:
            if res_py.status_code != 200:
                res_py.failure(f"Erro PY {res_py.status_code}: {res_py.text}")
            else:
                try:
                    json_data = res_py.json()
                    if "errors" in json_data:
                        res_py.failure(f"Erro GraphQL PY: {json_data['errors'][0]['message']}")
                    else:
                        res_py.success()
                        res_py.request_meta["response_length"] = len(res_py.content)
                except Exception as e:
                    res_py.failure(f"Erro JSON PY: {str(e)}")

    #@task
    def graphql_typescript(self):
        with self.client.post(f"{HOST_GRAPHQL_TS}/graphql", json=self.payload, headers=self.headers, name="2. GraphQL (TS) - Músicas", catch_response=True) as res_ts:
            if res_ts.status_code != 200:
                res_ts.failure(f"Erro TS {res_ts.status_code}: {res_ts.text}")
            else:
                try:
                    json_data = res_ts.json()
                    if "errors" in json_data:
                        res_ts.failure(f"Erro GraphQL TS: {json_data['errors'][0]['message']}")
                    else:
                        res_ts.success()
                        res_ts.request_meta["response_length"] = len(res_ts.content)
                except Exception as e:
                    res_ts.failure(f"Erro JSON TS: {str(e)}")


# ==========================================
# 3. TESTE SOAP
# ==========================================
class Teste_3_SOAP(HttpUser):
    abstract = True # Deixe comentado para rodar o SOAP
    wait_time = between(0.1, 0.5)

    #@task  
    def soap_python(self):
        body = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="streaming.soap">
           <soapenv:Header/>
           <soapenv:Body><tns:listar_musicas/></soapenv:Body>
        </soapenv:Envelope>"""
        headers = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '"listar_musicas"'}
        
        with self.client.post(f"{HOST_SOAP_PY}/", data=body, headers=headers, name="3. SOAP (PY) - Músicas", catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Erro PY HTTP {res.status_code}: {res.text}")
            # Verificação relaxada para aceitar tanto <nome> do TS quanto <s0:nome> do PY
            elif "nome" not in res.text:
                res.failure(f"Falso Positivo PY! XML vazio ou quebrado: {res.text[:100]}...")
            else:
                res.success()
                res.request_meta["response_length"] = len(res.content)

    #@task  
    def soap_typescript(self):
        body = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://streaming.soap">
           <soapenv:Header/>
           <soapenv:Body><tns:listar_musicas/></soapenv:Body>
        </soapenv:Envelope>"""
        headers = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '"listar_musicas"'}
        
        with self.client.post(f"{HOST_SOAP_TS}/", data=body, headers=headers, name="3. SOAP (TS) - Músicas", catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Erro TS HTTP {res.status_code}: {res.text}")
            elif "nome" not in res.text:
                res.failure(f"Falso Positivo TS! XML vazio ou quebrado: {res.text[:100]}...")
            else:
                res.success()
                res.request_meta["response_length"] = len(res.content)

# ==========================================
# 4. TESTE gRPC
# ==========================================
class Teste_4_gRPC(HttpUser):
    #abstract = True  # Comente esta linha para ATIVAR o gRPC
    wait_time = between(0.1, 0.5)

    #@task  
    def grpc_python(self):
        self._disparar_grpc(HOST_GRPC_PY, "4. gRPC (PY) - Músicas")

    @task  
    def grpc_typescript(self):
        self._disparar_grpc(HOST_GRPC_TS, "4. gRPC (TS) - Músicas")

    def _disparar_grpc(self, host, name):
        start_time = time.time()
        try:
            with grpc.insecure_channel(host) as channel:
                stub = streaming_pb2_grpc.StreamingServiceStub(channel)
                response = stub.ListarMusicas(streaming_pb2.Empty())
                tamanho_bytes = response.ByteSize()
            
            events.request.fire(
                request_type="gRPC", 
                name=name, 
                response_time=int((time.time() - start_time)*1000), 
                response_length=tamanho_bytes, 
                exception=None
            )
        except Exception as e:
            events.request.fire(
                request_type="gRPC", 
                name=name, 
                response_time=int((time.time() - start_time)*1000), 
                response_length=0, 
                exception=e
            )