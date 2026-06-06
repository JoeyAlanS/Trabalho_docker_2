import express from 'express';
import * as soap from 'soap';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();

const wsdl = `
<definitions name="StreamingService" targetNamespace="http://streaming.soap" xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://streaming.soap" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  
  <types>
    <xsd:schema targetNamespace="http://streaming.soap">
      
      <xsd:complexType name="Usuario">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int"/>
          <xsd:element name="nome" type="xsd:string"/>
          <xsd:element name="idade" type="xsd:int" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="ArrayOfUsuario">
        <xsd:sequence>
          <xsd:element name="Usuario" type="tns:Usuario" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>

      <xsd:complexType name="Musica">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int"/>
          <xsd:element name="nome" type="xsd:string"/>
          <xsd:element name="artista" type="xsd:string"/>
          <xsd:element name="album" type="xsd:string" minOccurs="0"/>
          <xsd:element name="compositor" type="xsd:string" minOccurs="0"/>
          <xsd:element name="ano_lancamento" type="xsd:int" minOccurs="0"/>
          <xsd:element name="genero" type="xsd:string" minOccurs="0"/>
          <xsd:element name="duracao" type="xsd:int" minOccurs="0"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="ArrayOfMusica">
        <xsd:sequence>
          <xsd:element name="Musica" type="tns:Musica" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
      </xsd:complexType>

      <xsd:complexType name="Playlist">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int"/>
          <xsd:element name="nome" type="xsd:string"/>
          <xsd:element name="usuario_id" type="xsd:int"/>
        </xsd:sequence>
      </xsd:complexType>
      
      <xsd:complexType name="GenericMessage">
        <xsd:sequence>
          <xsd:element name="mensagem" type="xsd:string"/>
        </xsd:sequence>
      </xsd:complexType>

    </xsd:schema>
  </types>

  <message name="EmptyRequest"/>
  
  <message name="ListarUsuariosResponse"><part name="return" type="tns:ArrayOfUsuario"/></message>
  <message name="ListarMusicasResponse"><part name="return" type="tns:ArrayOfMusica"/></message>
  
  <message name="UsuarioResponse"><part name="return" type="tns:Usuario"/></message>
  <message name="MusicaResponse"><part name="return" type="tns:Musica"/></message>
  <message name="PlaylistResponse"><part name="return" type="tns:Playlist"/></message>
  <message name="GenericMsgResponse"><part name="return" type="tns:GenericMessage"/></message>

  <message name="CreateUsuarioRequest">
    <part name="nome" type="xsd:string"/>
    <part name="idade" type="xsd:int"/>
  </message>
  <message name="CreateMusicaRequest">
    <part name="nome" type="xsd:string"/>
    <part name="artista" type="xsd:string"/>
    <part name="album" type="xsd:string"/>
    <part name="compositor" type="xsd:string"/>
    <part name="ano_lancamento" type="xsd:int"/>
    <part name="genero" type="xsd:string"/>
    <part name="duracao" type="xsd:int"/>
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
    <part name="album" type="xsd:string"/>
    <part name="compositor" type="xsd:string"/>
    <part name="ano_lancamento" type="xsd:int"/>
    <part name="genero" type="xsd:string"/>
    <part name="duracao" type="xsd:int"/>
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
    <operation name="listar_usuarios"><input message="tns:EmptyRequest"/><output message="tns:ListarUsuariosResponse"/></operation>
    <operation name="listar_musicas"><input message="tns:EmptyRequest"/><output message="tns:ListarMusicasResponse"/></operation>
    
    <operation name="criar_usuario"><input message="tns:CreateUsuarioRequest"/><output message="tns:UsuarioResponse"/></operation>
    <operation name="criar_musica"><input message="tns:CreateMusicaRequest"/><output message="tns:MusicaResponse"/></operation>
    <operation name="criar_playlist"><input message="tns:CreatePlaylistRequest"/><output message="tns:PlaylistResponse"/></operation>
    
    <operation name="atualizar_usuario"><input message="tns:UpdateUsuarioRequest"/><output message="tns:UsuarioResponse"/></operation>
    <operation name="atualizar_musica"><input message="tns:UpdateMusicaRequest"/><output message="tns:MusicaResponse"/></operation>
    <operation name="atualizar_playlist"><input message="tns:UpdatePlaylistRequest"/><output message="tns:PlaylistResponse"/></operation>
    
    <operation name="deletar_usuario"><input message="tns:DeleteRequest"/><output message="tns:GenericMsgResponse"/></operation>
    <operation name="deletar_musica"><input message="tns:DeleteRequest"/><output message="tns:GenericMsgResponse"/></operation>
    <operation name="deletar_playlist"><input message="tns:DeleteRequest"/><output message="tns:GenericMsgResponse"/></operation>
  </portType>

  <binding name="StreamingBinding" type="tns:StreamingPort">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="listar_usuarios"><soap:operation soapAction="listar_usuarios"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="listar_musicas"><soap:operation soapAction="listar_musicas"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    
    <operation name="criar_usuario"><soap:operation soapAction="criar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="criar_musica"><soap:operation soapAction="criar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="criar_playlist"><soap:operation soapAction="criar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    
    <operation name="atualizar_usuario"><soap:operation soapAction="atualizar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="atualizar_musica"><soap:operation soapAction="atualizar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="atualizar_playlist"><soap:operation soapAction="atualizar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    
    <operation name="deletar_usuario"><soap:operation soapAction="deletar_usuario"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="deletar_musica"><soap:operation soapAction="deletar_musica"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
    <operation name="deletar_playlist"><soap:operation soapAction="deletar_playlist"/><input><soap:body use="literal"/></input><output><soap:body use="literal"/></output></operation>
  </binding>

  <service name="SOAPService">
    <port name="StreamingPort" binding="tns:StreamingBinding"><soap:address location="http://0.0.0.0:9002/"/></port>
  </service>
</definitions>`;

const service = {
  SOAPService: {
    StreamingPort: {
      // 100% livre de promises perdidas: utilizando callbacks diretos com .then()
      listar_usuarios: (args: any, cb: any) => {
        prisma.usuarios.findMany()
            .then(res => cb({ return: { Usuario: res } }))
            .catch(cb);
      },
listar_musicas: (args: any, cb: any) => {
        prisma.musicas.findMany()
          .then(res => {
            console.log(`[SOAP TS] Músicas encontradas no banco DB: ${res.length}`);
            
            if (res.length === 0) {
              console.log("[SOAP TS] ALERTA: O banco está vazio! O Locust vai falhar porque não tem a tag <nome>.");
            }

            // Limpeza obrigatória: transformando 'null' do banco em 'undefined' para o SOAP
            const musicasLimpas = res.map(m => ({
              id: m.id,
              nome: m.nome,
              artista: m.artista,
              album: m.album !== null ? m.album : undefined,
              compositor: m.compositor !== null ? m.compositor : undefined,
              ano_lancamento: m.ano_lancamento !== null ? m.ano_lancamento : undefined,
              genero: m.genero !== null ? m.genero : undefined,
              duracao: m.duracao !== null ? m.duracao : undefined
            }));

            // O SEGREDO ESTÁ AQUI: Usando a mesma estrutura de map que funcionou no Mock!
            cb({ return: musicasLimpas.map(m => ({ Musica: m })) });
          })
          .catch(err => {
            console.error("[SOAP TS] Erro ao buscar músicas:", err);
            cb(err);
          });
      },
      criar_usuario: (args: any, cb: any) => {
        prisma.usuarios.create({ data: { nome: args.nome, idade: Number(args.idade) } })
            .then(res => cb({ return: res })).catch(cb);
      },
      criar_musica: (args: any, cb: any) => {
        prisma.musicas.create({ 
          data: { 
            nome: args.nome, artista: args.artista, album: args.album || null, 
            compositor: args.compositor || null, ano_lancamento: args.ano_lancamento ? Number(args.ano_lancamento) : null, 
            genero: args.genero || null, duracao: args.duracao ? Number(args.duracao) : null 
          } 
        }).then(res => cb({ return: res })).catch(cb);
      },
      criar_playlist: (args: any, cb: any) => {
        prisma.playlists.create({ data: { nome: args.nome, usuario_id: Number(args.usuario_id) } })
            .then(res => cb({ return: res })).catch(cb);
      },
      atualizar_usuario: (args: any, cb: any) => {
        prisma.usuarios.update({ 
            where: { id: Number(args.id) }, 
            data: { nome: args.nome, idade: Number(args.idade) } 
        }).then(res => cb({ return: res })).catch(cb);
      },
      deletar_usuario: (args: any, cb: any) => {
        prisma.usuarios.delete({ where: { id: Number(args.id) } })
            .then(() => cb({ return: { mensagem: "Deletado com sucesso" } })).catch(cb);
      },
      atualizar_musica: (args: any, cb: any) => {
        prisma.musicas.update({ 
            where: { id: Number(args.id) }, 
            data: { 
              nome: args.nome, artista: args.artista, album: args.album || null, 
              compositor: args.compositor || null, ano_lancamento: args.ano_lancamento ? Number(args.ano_lancamento) : null, 
              genero: args.genero || null, duracao: args.duracao ? Number(args.duracao) : null 
            } 
        }).then(res => cb({ return: res })).catch(cb);
      },
      deletar_musica: (args: any, cb: any) => {
        prisma.musicas.delete({ where: { id: Number(args.id) } })
            .then(() => cb({ return: { mensagem: "Deletado com sucesso" } })).catch(cb);
      },
      atualizar_playlist: (args: any, cb: any) => {
        prisma.playlists.update({ 
            where: { id: Number(args.id) }, 
            data: { nome: args.nome, usuario_id: Number(args.usuario_id) } 
        }).then(res => cb({ return: res })).catch(cb);
      },
      deletar_playlist: (args: any, cb: any) => {
        prisma.playlists.delete({ where: { id: Number(args.id) } })
            .then(() => cb({ return: { mensagem: "Deletado com sucesso" } })).catch(cb);
      }
    }
  }
};

const server = app.listen(9002, () => {
  soap.listen(server, '/', service, wsdl);
  console.log('TS SOAP Server rodando na 9002 (Resolvido Falso Positivo)');
});