from fastapi import APIRouter

from .endpoints import health_check


# Cria um router de API e inclui o router com as rotas definidas em endpoints.<servico>.router
api_router = APIRouter()
api_router.include_router(health_check.router, tags=["health"])