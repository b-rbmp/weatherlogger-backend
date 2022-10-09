import secrets, os, json

from typing import List, Optional

from dotenv import load_dotenv

from pydantic import AnyHttpUrl, BaseSettings, EmailStr

# Carrega variaveis de ambiente com o .env
load_dotenv(verbose=True)

# Configuração de Base, valido tanto para Development ou Production
class SettingsBase(BaseSettings):
    MODE: str = os.getenv("PROD_OR_DEV")
    API_V1_STR: str = "/weatherlogger/api/v1"
    PROJECT_NAME: str = "API WeatherLogger"
    DESCRIPTION: str = "WeatherLogger API Service."
    VERSION: str = "0.0.1"

    # Permissão Super Admin que da acesso a todas os modulos do sistema:
    SUPER_USER_PERMISSION: str = "superuser"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


# Configurações Ambiente de Desenvolvimento - Definidos todos no .env ou sobrepostos por variáveis de ambiente
class SettingsDev(SettingsBase):
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    DB_SERVICE: str = os.getenv("DB_DEV_SERVICE")
    DB_USER: str = os.getenv("DB_DEV_USER")
    DB_PASS: str = os.getenv("DB_DEV_PASS")
    DB_HOST: str = os.getenv("DB_DEV_HOST")
    DB_NAME: str = os.getenv("DB_DEV_NAME")
    DB_SCHEMA: str = os.getenv("DB_DEV_SCHEMA")



# Configurações Ambiente de Produção - Definidos todos no .env ou sobrepostos por variáveis de ambiente
class SettingsProd(SettingsBase):
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    DB_SERVICE: str = os.getenv("DB_PROD_SERVICE")
    DB_USER: str = os.getenv("DB_PROD_USER")
    DB_PASS: str = os.getenv("DB_PROD_PASS")
    DB_HOST: str = os.getenv("DB_PROD_HOST")
    DB_NAME: str = os.getenv("DB_PROD_NAME")
    DB_SCHEMA: str = os.getenv("DB_PROD_SCHEMA")


# Seleciona as configurações baseados no modo de funcionamento (production ou development)
settings = (
    SettingsProd()
    if os.getenv("PROD_OR_DEV") == "PROD"
    else SettingsDev()
)
