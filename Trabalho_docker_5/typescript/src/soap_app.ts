import express from 'express';
import * as soap from 'soap';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();

const wsdl = `
<definitions name="StreamingService" targetNamespace="http://streaming.soap" xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://streaming.soap" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <message name="EmptyRequest"/>
  <message name="IdRequest"><part name="id" type="xsd:int"/></message>
  <message name="GenericResponse"><part name="return" type="xsd:string"/></message>
  <portType name="StreamingPort">
    <operation name="listar_usuarios"><input message="tns:EmptyRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="listar_musicas"><input message="tns:EmptyRequest"/><output message="tns:GenericResponse"/></operation>
  </portType>
  <binding name="StreamingBinding" type="tns:StreamingPort">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="listar_usuarios"><soap:operation soapAction="listar_usuarios"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="listar_musicas"><soap:operation soapAction="listar_musicas"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
  </binding>
  <service name="SOAPService">
    <port name="StreamingPort" binding="tns:StreamingBinding"><soap:address location="http://0.0.0.0:9002/"/></port>
  </service>
</definitions>`;

const service = {
  SOAPService: {
    StreamingPort: {
      listar_usuarios: async (args: any, callback: any) => {
        const res = await prisma.usuarios.findMany();
        callback({ return: JSON.stringify(res) });
      },
      listar_musicas: async (args: any, callback: any) => {
        const res = await prisma.musicas.findMany();
        callback({ return: JSON.stringify(res) });
      }
    }
  }
};

const server = app.listen(9002, () => {
  soap.listen(server, '/', service, wsdl);
  console.log('TS SOAP Server rodando na 9002');
});