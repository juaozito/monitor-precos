from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 1. A URL: Onde o banco de dados "mora"
# Por enquanto vou usar o SQLITE (arquivo local) para facilitar meu desenvolvimento
SQLALCHEMY_DATABASE_URL = "sqlite://./precos.db"

# 2. O Motor (Engine): É quem realmente conversa com o arquivo do banco.
# o "Check_same_thread" é necessário apenas para o SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}

)

# 3. A Fábrica (SessionLocal): Cada vez que o site quiser salvar algo,
# ele pede uma "sessão" para essa fábrica
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. A Base: Todos os nossos modelos (Produto, Preço) vão herdade dessa classe.
# É ela quem avisa ao SQLAlchemy: "Ei, transforme essa classe Python em uma tabela!"
Base = declarative_base()

# 5. O Gerenciador (Dependência): Abre a conexão e garante que ela feche depois.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        