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
    wait_time = between(1, 2)

    @task  #<--- Remova o '#' no início desta linha para ativar o REST
    def rest(self):
        self.client.get(f"{HOST_REST_PY}/musicas", name="1. REST (PY) - Músicas")
        #self.client.get(f"{HOST_REST_TS}/musicas", name="1. REST (TS) - Músicas")

# ==========================================
# 2. TESTE GRAPHQL
# ==========================================
class Teste_2_GraphQL(HttpUser):
    wait_time = between(1, 2)

    #@task  #<--- Remova o '#' no início desta linha para ativar o GraphQL
    def graphql(self):
        payload = {"query": "query { musicas { id nome artista album compositor anoLancamento genero duracao } }"}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        with self.client.post(f"{HOST_GRAPHQL_PY}/graphql", json=payload, headers=headers, name="2. GraphQL (PY) - Músicas", catch_response=True) as res_py:
            if res_py.status_code != 200:
                res_py.failure(f"Erro PY {res_py.status_code}: {res_py.text}")
                
        with self.client.post(f"{HOST_GRAPHQL_TS}/", json=payload, headers=headers, name="2. GraphQL (TS) - Músicas", catch_response=True) as res_ts:
            if res_ts.status_code != 200:
                res_ts.failure(f"Erro TS {res_ts.status_code}: {res_ts.text}")

# ==========================================
# 3. TESTE SOAP
# ==========================================
class Teste_3_SOAP(HttpUser):
    wait_time = between(1, 2)

    #@task  # <--- Este está ativo! O Locust rodará apenas o SOAP agora.
    def soap(self):
        # Python (Spyne)
        body_py = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="streaming.soap">
           <soapenv:Header/>
           <soapenv:Body><tns:listar_musicas/></soapenv:Body>
        </soapenv:Envelope>"""
        
        # Correção do erro 500: aspas duplas adicionadas no SOAPAction
        headers_py = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '"listar_musicas"'}
        
        with self.client.post(f"{HOST_SOAP_PY}/", data=body_py, headers=headers_py, name="3. SOAP (PY) - Músicas", catch_response=True) as res_py:
            if res_py.status_code != 200:
                res_py.failure(f"Erro PY {res_py.status_code}: {res_py.text}")

        # TypeScript
        body_ts = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://streaming.soap">
           <soapenv:Header/>
           <soapenv:Body><tns:listar_musicas/></soapenv:Body>
        </soapenv:Envelope>"""
        
        headers_ts = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '"listar_musicas"'}
        
        with self.client.post(f"{HOST_SOAP_TS}/", data=body_ts, headers=headers_ts, name="3. SOAP (TS) - Músicas", catch_response=True) as res_ts:
            if res_ts.status_code != 200:
                res_ts.failure(f"Erro TS {res_ts.status_code}: {res_ts.text}")

# ==========================================
# 4. TESTE gRPC
# ==========================================
class Teste_4_gRPC(HttpUser):
    wait_time = between(1, 2)

    #@task  #<--- Remova o '#' no início desta linha para ativar o gRPC
    def grpc_test(self):
        self.disparar_grpc(HOST_GRPC_PY, "4. gRPC (PY)")
        self.disparar_grpc(HOST_GRPC_TS, "4. gRPC (TS)")

    def disparar_grpc(self, host, name):
        start_time = time.time()
        try:
            with grpc.insecure_channel(host) as channel:
                stub = streaming_pb2_grpc.StreamingServiceStub(channel)
                response = stub.ListarMusicas(streaming_pb2.Empty())
            events.request.fire(request_type="gRPC", name=name, response_time=int((time.time() - start_time)*1000), response_length=0, exception=None)
        except Exception as e:
            events.request.fire(request_type="gRPC", name=name, response_time=int((time.time() - start_time)*1000), response_length=0, exception=e)