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
  
  <message name="CreateUsuarioRequest">
    <part name="nome" type="xsd:string"/>
    <part name="idade" type="xsd:int"/>
  </message>
  <message name="CreateMusicaRequest">
    <part name="nome" type="xsd:string"/>
    <part name="artista" type="xsd:string"/>
  </message>
  <message name="CreatePlaylistRequest">
    <part name="nome" type="xsd:string"/>
    <part name="usuario_id" type="xsd:int"/>
  </message>
  <message name="UpdateUsuarioRequest">
    <part name="id" type="xsd:int"/>
    <part name="nome" type="xsd:string"/>
    <part name="idade" type="xsd:int"/>
  </message>
  <message name="UpdateMusicaRequest">
    <part name="id" type="xsd:int"/>
    <part name="nome" type="xsd:string"/>
    <part name="artista" type="xsd:string"/>
  </message>
  <message name="UpdatePlaylistRequest">
    <part name="id" type="xsd:int"/>
    <part name="nome" type="xsd:string"/>
    <part name="usuario_id" type="xsd:int"/>
  </message>
  <message name="DeleteRequest">
    <part name="id" type="xsd:int"/>
  </message>

  <portType name="StreamingPort">
    <operation name="listar_usuarios"><input message="tns:EmptyRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="listar_musicas"><input message="tns:EmptyRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="criar_usuario"><input message="tns:CreateUsuarioRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="criar_musica"><input message="tns:CreateMusicaRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="criar_playlist"><input message="tns:CreatePlaylistRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="atualizar_usuario"><input message="tns:UpdateUsuarioRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="deletar_usuario"><input message="tns:DeleteRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="atualizar_musica"><input message="tns:UpdateMusicaRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="deletar_musica"><input message="tns:DeleteRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="atualizar_playlist"><input message="tns:UpdatePlaylistRequest"/><output message="tns:GenericResponse"/></operation>
    <operation name="deletar_playlist"><input message="tns:DeleteRequest"/><output message="tns:GenericResponse"/></operation>
  </portType>

  <binding name="StreamingBinding" type="tns:StreamingPort">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="listar_usuarios"><soap:operation soapAction="listar_usuarios"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="listar_musicas"><soap:operation soapAction="listar_musicas"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="criar_usuario"><soap:operation soapAction="criar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="criar_musica"><soap:operation soapAction="criar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="criar_playlist"><soap:operation soapAction="criar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="atualizar_usuario"><soap:operation soapAction="atualizar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="deletar_usuario"><soap:operation soapAction="deletar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="atualizar_musica"><soap:operation soapAction="atualizar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="deletar_musica"><soap:operation soapAction="deletar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="atualizar_playlist"><soap:operation soapAction="atualizar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="deletar_playlist"><soap:operation soapAction="deletar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
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
      },
      criar_usuario: async (args: any, callback: any) => {
        const res = await prisma.usuarios.create({ data: { nome: args.nome, idade: Number(args.idade) } });
        callback({ return: JSON.stringify(res) });
      },
      criar_musica: async (args: any, callback: any) => {
        const res = await prisma.musicas.create({ data: { nome: args.nome, artista: args.artista } });
        callback({ return: JSON.stringify(res) });
      },
      criar_playlist: async (args: any, callback: any) => {
        const res = await prisma.playlists.create({ data: { nome: args.nome, usuario_id: Number(args.usuario_id) } });
        callback({ return: JSON.stringify(res) });
      },
      atualizar_usuario: async (args: any, callback: any) => {
        const res = await prisma.usuarios.update({ 
            where: { id: Number(args.id) }, 
            data: { nome: args.nome, idade: Number(args.idade) } 
        });
        callback({ return: JSON.stringify(res) });
      },
      deletar_usuario: async (args: any, callback: any) => {
        await prisma.usuarios.delete({ where: { id: Number(args.id) } });
        callback({ return: "Deletado com sucesso" });
      },
      atualizar_musica: async (args: any, callback: any) => {
        const res = await prisma.musicas.update({ 
            where: { id: Number(args.id) }, 
            data: { nome: args.nome, artista: args.artista } 
        });
        callback({ return: JSON.stringify(res) });
      },
      deletar_musica: async (args: any, callback: any) => {
        await prisma.musicas.delete({ where: { id: Number(args.id) } });
        callback({ return: "Deletado com sucesso" });
      },
      atualizar_playlist: async (args: any, callback: any) => {
        const res = await prisma.playlists.update({ 
            where: { id: Number(args.id) }, 
            data: { nome: args.nome, usuario_id: Number(args.usuario_id) } 
        });
        callback({ return: JSON.stringify(res) });
      },
      deletar_playlist: async (args: any, callback: any) => {
        await prisma.playlists.delete({ where: { id: Number(args.id) } });
        callback({ return: "Deletado com sucesso" });
      }
    }
  }
};

const server = app.listen(9002, () => {
  soap.listen(server, '/', service, wsdl);
  console.log('TS SOAP Server rodando na 9002');
});