import asyncio
import random
from sqlalchemy.future import select
from db import SessionLocal, Usuario, Musica, Playlist, engine, Base
from faker import Faker

fake = Faker()

async def seed_db():
    # 1. Criação das tabelas de forma assíncrona usando run_sync
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with SessionLocal() as db:
        # Verifica se já existem usuários (para não duplicar em múltiplas execuções)
        result = await db.execute(select(Usuario))
        usuarios_existentes = result.scalars().all()
        
        if len(usuarios_existentes) == 0:
            print("Iniciando a inserção de dados falsos...")
            
            usuarios = [Usuario(nome=fake.name(), idade=random.randint(18, 65)) for _ in range(300)]
            
            generos = ["Rock", "Pop", "Hip-Hop", "Jazz", "Classical", "Electronic", "R&B", "Country", "Reggae", "Blues"]
            
            musicas = [
                Musica(
                    nome=fake.catch_phrase(),
                    artista=fake.name(),
                    album=fake.word().title(),
                    compositor=fake.name(),
                    ano_lancamento=random.randint(1990, 2024),
                    genero=random.choice(generos),
                    duracao=random.randint(120, 360)  # 2-6 minutos em segundos
                ) for _ in range(300)
            ]
            
            db.add_all(usuarios)
            db.add_all(musicas)
            await db.commit()

            # Buscar os dados inseridos para montar as playlists
            res_users = await db.execute(select(Usuario))
            all_users = res_users.scalars().all()
            
            res_songs = await db.execute(select(Musica))
            all_songs = res_songs.scalars().all()

            for u in all_users:
                p = Playlist(nome=f"Hits de {fake.word()}", usuario_id=u.id)
                p.musicas = random.sample(all_songs, k=random.randint(5, 15))
                db.add(p)
                
            await db.commit()
            print("Banco populado com sucesso!")
        else:
            print("O banco já possui dados. Seed ignorado.")

if __name__ == "__main__":
    # Roda a função assíncrona principal
    asyncio.run(seed_db())