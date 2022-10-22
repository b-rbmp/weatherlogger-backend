from fastapi import APIRouter

from .endpoints import health_check, weather_record, weather_station, frontend


# Cria um router de API e inclui o router com as rotas definidas em endpoints.<servico>.router
api_router = APIRouter()
api_router.include_router(health_check.router, tags=["health"])
api_router.include_router(weather_record.router, tags=["weatherrecord"])
api_router.include_router(weather_station.router, tags=["weatherstation"])
api_router.include_router(frontend.router, tags=["frontend"])