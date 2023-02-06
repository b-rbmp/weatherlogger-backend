from datetime import datetime
from typing import List, Optional

from fastapi.params import Depends
from fastapi import Query, HTTPException, APIRouter, Response, status

from sqlalchemy.orm import Session

from app import models, schemas
from app.db.db_manager import CRUDWeatherRecord, CRUDWeatherStation
from app.dependencies import get_db

# Definição dos Caminhos da API

# Cria o Roteador de API
router = APIRouter()

# Para todos os caminhos, Abre-se e fecha-se uma conexão com o banco a cada requisição (get_db, em dependencies)
@router.get("/weatherrecord/", tags=["weatherrecord"], response_model=List[schemas.WeatherRecordInDBBase])
def get_weatherrecord(
    response: Response,
    skip: Optional[int] = Query(None, ge=0, description="Offset da requisição"),
    limit: Optional[int] = Query(
        None, le=1000, description="Limite de weatherrecord retornadas por requisição"
    ),
    data_inicial: Optional[datetime] = Query(None, description="Data Inicial"),
    data_final: Optional[datetime] = Query(None, description="Data Final"),
    weather_station_id: Optional[int] = Query(None, description="ID de Weather Station"),
    db: Session = Depends(get_db),
):

    weatherrecord = CRUDWeatherRecord.get_list(skip=skip, limit=limit, db=db, data_inicial=data_inicial, data_final=data_final, weather_station_id=weather_station_id)

    response.headers["X-Total-Count"] = weatherrecord["total-count"]

    return weatherrecord["elements"]


@router.post("/weatherrecord/", tags=["weatherrecord"], response_model=schemas.WeatherRecordInDBBase)
def create_weatherrecord(
    weatherrecord: schemas.WeatherRecordCreateIn,
    db: Session = Depends(get_db),
):
    # db_weather_station = CRUDWeatherStation.get_by_id(db=db, id=weatherrecord.weather_station_id)
    # if db_weather_station is None:
    #     raise HTTPException(status_code=404, detail="Weather Station não encontrado")

    # db_weather_record_exists = CRUDWeatherRecord.get_by_weather_station_id_and_date(db=db, weather_station_id=weatherrecord.weather_station_id, date=weatherrecord.date)
    # if db_weather_record_exists is not None:
    #     raise HTTPException(status_code=409, detail="Weather Record com mesma data e estação já encontrado")
  
    # weatherrecord_out = schemas.WeatherRecordCreateOut(**weatherrecord.copy().dict(), weather_station=db_weather_station)
    # return CRUDWeatherRecord.create(db=db, item=weatherrecord_out)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

@router.get("/weatherrecord/{weather_station_id}&{date}", tags=["weatherrecord"], response_model=schemas.WeatherRecordInDBBase)
def get_weatherrecord_id(
    weather_station_id: int,
    date: datetime,
    db: Session = Depends(get_db),
):
    db_weatherrecord = CRUDWeatherRecord.get_by_weather_station_id_and_date(db=db, weather_station_id=weather_station_id, date=date)
    if db_weatherrecord is None:
        raise HTTPException(status_code=404, detail="WeatherRecord não encontrado")
    return db_weatherrecord

@router.put("/weatherrecord/{weather_station_id}&{date}", tags=["weatherrecord"], response_model=schemas.WeatherRecordInDBBase)
def update_weatherrecord(
    weather_station_id: int,
    date: datetime,
    weatherrecord: schemas.WeatherRecordUpdateIn,
    db: Session = Depends(get_db),
):
    # db_weatherrecord = CRUDWeatherRecord.get_by_weather_station_id_and_date(db=db, weather_station_id=weather_station_id, date=date)

    # if db_weatherrecord is None:
    #     raise HTTPException(status_code=404, detail="WeatherRecord não encontrado")
    # db_weather_station = None
    # if weatherrecord.weather_station_id is not None:
    #     db_weather_station = CRUDWeatherStation.get_by_id(db=db, id=weatherrecord.weather_station_id)
    #     if db_weather_station is None:
    #         raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    # else:
    #     db_weather_station = CRUDWeatherStation.get_by_id(db=db, id=weather_station_id)
    #     if db_weather_station is None:
    #         raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    # weatherrecord_out = schemas.WeatherRecordUpdateOut(**weatherrecord.copy().dict(), weather_station=db_weather_station)


    # return CRUDWeatherRecord.update(db=db, item=weatherrecord_out, db_item=db_weatherrecord)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")


@router.delete("/weatherrecord/{weather_station_id}&{date}", tags=["weatherrecord"], response_model=bool)
def delete(
    weather_station_id: int,
    date: datetime,
    db: Session = Depends(get_db),
):
    # db_weatherrecord = CRUDWeatherRecord.get_by_weather_station_id_and_date(db=db, weather_station_id=weather_station_id, date=date)
    # if db_weatherrecord is None:
    #     raise HTTPException(status_code=404, detail="WeatherRecord não encontrado")
    # return CRUDWeatherRecord.delete(db=db, db_item=db_weatherrecord)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

