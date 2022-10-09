from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware



#from .dependencies import get_query_token
from .app.api.api_v1.api import api_router
from backend.src.config import settings

# Inicialização do API com as suas configurações
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f"{settings.API_V1_STR}/openapi.json", docs_url=f"{settings.API_V1_STR}/docs", redoc_url=f"{settings.API_V1_STR}/redoc")

# Permite todo tipo de comunicação CORS através das origens definidas nas configurações em settings.BACKEND_CORS_ORIGINS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-total-count"],
    )

# Inclui o Router do API, com o prefixo definido nas configurações
app.include_router(api_router, prefix=settings.API_V1_STR)

