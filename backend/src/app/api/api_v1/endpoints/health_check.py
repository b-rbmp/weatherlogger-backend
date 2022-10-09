from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.src.app import schemas

from backend.src.app.dependencies import get_db

router = APIRouter()

# Apenas verifica se esta funcionando para o Cluster
@router.get("/health-check/", tags=["health"], status_code=200)
async def root():
    return {"message": "OK"}
