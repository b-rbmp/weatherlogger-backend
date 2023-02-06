from typing import List, Optional

from fastapi.params import Depends
from fastapi import Query, HTTPException, APIRouter, Response, status

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.db.db_manager import CRUDWeatherStation
from app import models, schemas

# Definição dos Caminhos da API

# Cria o Roteador de API
router = APIRouter()

# Para todos os caminhos, Abre-se e fecha-se uma conexão com o banco a cada requisição (get_db, em dependencies)
@router.get("/weatherstation/", tags=["weatherstation"], response_model=List[schemas.WeatherStationInDBBase])
def get_weatherstation(
    response: Response,
    skip: Optional[int] = Query(None, ge=0, description="Offset da requisição"),
    limit: Optional[int] = Query(
        None, le=1000, description="Limite de weatherstation retornadas por requisição"
    ),
    api_key: Optional[str] = Query(None, description="API Key da Estação"),
    name: Optional[str] = Query(None, description="Nome da Estação"),
    city: Optional[str] = Query(None, description="Cidade da Estação"),
    country: Optional[str] = Query(None, description="País da Estação"),
    db: Session = Depends(get_db),
):
    weatherstation = CRUDWeatherStation.get_list(skip=skip, limit=limit, db=db, api_key=api_key, name=name, city=city, country=country)

    response.headers["X-Total-Count"] = weatherstation["total-count"]

    return weatherstation["elements"]


@router.post("/weatherstation/", tags=["weatherstation"], response_model=schemas.WeatherStationInDBBase)
def create_weatherstation(
    weather_station: schemas.WeatherStationCreateIn,
    db: Session = Depends(get_db),
):
    # db_weatherstation = CRUDWeatherStation.get_list(skip=0, limit=10, db=db, api_key=weather_station.api_key)
    # if len(db_weatherstation["elements"]):
    #     raise HTTPException(status_code=409, detail="WeatherStation com mesma api_key já registrada")

    # weatherstation_out = schemas.WeatherStationCreateOut(**weather_station.copy().dict())
    # return CRUDWeatherStation.create(db=db, item=weatherstation_out)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

@router.get("/weatherstation/{id}", tags=["weatherstation"], response_model=schemas.WeatherStationInDBBase)
def get_weatherstation_id(
    id: int,
    db: Session = Depends(get_db),
):
    db_weatherstation = CRUDWeatherStation.get_by_id(db=db, id=id)
    if db_weatherstation is None:
        raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    return db_weatherstation

@router.put("/weatherstation/{id}", tags=["weatherstation"], response_model=schemas.WeatherStationInDBBase)
def update_weatherstation(
    id: int,
    weather_station: schemas.WeatherStationUpdateIn,
    db: Session = Depends(get_db),
):
    # db_weatherstation = CRUDWeatherStation.get_by_id(db=db, id=id)
    # if db_weatherstation is None:
    #     raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    
    # weatherstation_out = schemas.WeatherStationUpdateOut(**weather_station.copy().dict())

    # return CRUDWeatherStation.update(db=db, item=weatherstation_out, db_item=db_weatherstation)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")


@router.delete("/weatherstation/{id}", tags=["weatherstation"], response_model=bool)
def delete(
    id: int,
    db: Session = Depends(get_db),
):
    # db_weatherstation = CRUDWeatherStation.get_by_id(db=db, id=id)
    # if db_weatherstation is None:
    #     raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    # return CRUDWeatherStation.delete(db=db, db_item=db_weatherstation)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
