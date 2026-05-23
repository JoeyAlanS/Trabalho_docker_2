from locust import HttpUser, task, between

class TesteDesempenho(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def teste_rest(self):
        # Chama REST (assumindo host apontado para porta 8000)
        self.client.get("/usuarios", name="REST /usuarios")

    @task(3)
    def teste_graphql(self):
        # Chama GraphQL (assumindo host apontado para porta 8001)
        query = {"query": "{ usuarios { id nome } }"}
        self.client.post("/graphql", json=query, name="GraphQL /usuarios")

    @task(1)
    def teste_soap(self):
        # Chama SOAP (assumindo host apontado para porta 8002)
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:str="streaming.soap">
           <soapenv:Header/>
           <soapenv:Body><str:listar_usuarios/></soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/", data=soap_body, headers={"Content-Type": "text/xml"}, name="SOAP /listar_usuarios")