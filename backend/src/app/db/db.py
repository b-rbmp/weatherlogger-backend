from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.config import settings

# Criação da conexão com o Banco de Dados, pega uma sessão para realizar as ações

# Retorna a URL Do banco de dados segundo as configurações definidas em /src/config.py
def get_db_url():
    return "{dbservice}://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
        dbservice=settings.DB_SERVICE,
        dbuser=settings.DB_USER,
        dbpass=settings.DB_PASS,
        dbhost=settings.DB_HOST,
        dbname=settings.DB_NAME)

# Cria o engine do SQL alchemy através da URL definida, com pool_pre_ping para evitar erros de timeout
engine = create_engine(get_db_url(), connect_args={'options': f'-csearch_path={settings.DB_SCHEMA}'}, pool_pre_ping=True)

# Cria uma sessão para efetuar modificações com a engine. Será usada por db_manager.py para operações CRUD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

