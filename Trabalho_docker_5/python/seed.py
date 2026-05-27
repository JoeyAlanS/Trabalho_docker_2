import random
from db import SessionLocal, Usuario, Musica, Playlist, engine, Base
from faker import Faker

Base.metadata.create_all(bind=engine)
db = SessionLocal()
fake = Faker()

if db.query(Usuario).count() == 0:
    usuarios = [Usuario(nome=fake.name(), idade=random.randint(18, 65)) for _ in range(300)]
    musicas = [Musica(nome=fake.catch_phrase(), artista=fake.name()) for _ in range(300)]
    db.add_all(usuarios)
    db.add_all(musicas)
    db.commit()

    all_users = db.query(Usuario).all()
    all_songs = db.query(Musica).all()

    for u in all_users:
        p = Playlist(nome=f"Hits de {fake.word()}", usuario_id=u.id)
        p.musicas = random.sample(all_songs, k=random.randint(5, 15))
        db.add(p)
    db.commit()
    print("Banco Populado com sucesso!")
db.close()