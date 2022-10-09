from fastapi.testclient import TestClient

from backend.src.main import app
from backend.src.config import settings
from backend.src.app.dependencies import has_permissions, override_has_permissions_dev

# Cria o cliente de teste
client = TestClient(app)

# Prefixo do caminho. Atualmente na versão V1, definido em /src/config.py
prefix = settings.API_V1_STR

# Retira a necessidade de permissoes
app.dependency_overrides[has_permissions] = override_has_permissions_dev

# Garante modo dev
settings.MODE = 'DEV'

def test_healthcheck():
    response = client.get(prefix+"/health-check/")
    assert response.status_code == 200
