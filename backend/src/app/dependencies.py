from fastapi import HTTPException, status, Security
from fastapi.security import SecurityScopes, HTTPBearer, HTTPAuthorizationCredentials
from typing import Generator
from backend.src.app.db.db import SessionLocal

# Cria uma conexão com o banco de dados de forma independente em cada request. Fecha a conexão no fim de cada request
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

