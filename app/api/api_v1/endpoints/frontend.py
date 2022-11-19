from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple

from fastapi.params import Depends
from fastapi import Query, HTTPException, APIRouter, Response

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.db.db_manager import CRUDWeatherRecord, CRUDWeatherStation
from app import models, schemas

# Definição dos Caminhos da API

# Cria o Roteador de API
router = APIRouter()

# Para todos os caminhos, Abre-se e fecha-se uma conexão com o banco a cada requisição (get_db, em dependencies)
@router.get("/globaldata/", tags=["frontend"], response_model=schemas.GlobalData)
def get_global_data(
    db: Session = Depends(get_db),
):
    ultima_amostra_db = CRUDWeatherRecord.get_last_record(db=db)
    if ultima_amostra_db is not None:
        ultima_amostra_data: datetime = ultima_amostra_db.date
        ultima_amostra: str = ultima_amostra_data.strftime("%d-%m-%Y %H:%M:%S")
    else:
        ultima_amostra: str = "Sem dados"

    estacoes_registradas: int = CRUDWeatherStation.count_all(db=db)
    numero_horas_estacoes_conectadas = 24
    estacoes_conectadas: int = CRUDWeatherStation.count_connected(db=db, number_of_hours=numero_horas_estacoes_conectadas)
    numero_amostras: int = CRUDWeatherRecord.count_all(db=db)
    
    stations_db: List[models.WeatherStation] = CRUDWeatherStation.get_list(db=db, skip=0, limit=10000)["elements"]
    stations: List[schemas.WeatherStationInDBBase] = [schemas.WeatherStationInDBBase.from_orm(station_db) for station_db in stations_db]
    if ultima_amostra_db is not None:
        preview_station: schemas.PreviewStation = schemas.PreviewStation(estacao=schemas.WeatherStationInDBBase.from_orm(ultima_amostra_db.weather_station), record=schemas.WeatherRecordInDBBase.from_orm(ultima_amostra_db))
    
    numero_dias_conectividade = 7
    
    evolucao_conectividade_list: List[Tuple[date, int]] = CRUDWeatherStation.count_connected_daily(db=db, number_of_days=numero_dias_conectividade)
    evolucao_conectividade: List[schemas.EvolucaoConectividadeData] = []
    for evolucao_conectividade_item in evolucao_conectividade_list:
        evolucao_conectividade.append(schemas.EvolucaoConectividadeData(date=evolucao_conectividade_item[0], connected=evolucao_conectividade_item[1]))
    
    edate = datetime.now().date()
    sdate = (datetime.now()-timedelta(days=numero_dias_conectividade)).date()
    dates_1_week = [sdate+timedelta(days=x+1) for x in range((edate-sdate).days)]

    for data in dates_1_week:
        has_item = False
        for evolucao_conectividade_item in evolucao_conectividade:
            if evolucao_conectividade_item.date == data:
                has_item = True
                break
        if not has_item:
            evolucao_conectividade.append(schemas.EvolucaoConectividadeData(date=data, connected=0))
    
    def find_date(elem: schemas.EvolucaoConectividadeData):
        return elem.date
    evolucao_conectividade.sort(key=find_date, reverse=False)
    global_data = schemas.GlobalData(estacoes_registradas=estacoes_registradas, estacoes_conectadas=estacoes_conectadas, numero_amostras=numero_amostras, ultima_amostra=ultima_amostra, stations=stations, preview_station=preview_station, evolucao_conectividade=evolucao_conectividade)

    return global_data

@router.get("/estacaodata/{id}", tags=["frontend"], response_model=schemas.EstacaoData)
def get_estacao_data(
    id: int,
    db: Session = Depends(get_db),
):
    db_weatherstation = CRUDWeatherStation.get_by_id(db=db, id=id)
    if db_weatherstation is None:
        raise HTTPException(status_code=404, detail="WeatherStation não encontrado")
    weather_station_db = schemas.WeatherStationInDBBase.from_orm(db_weatherstation)

    weather_records: List[models.WeatherRecord] = CRUDWeatherRecord.get_list(db=db, skip=0, limit=100000, weather_station_id=weather_station_db.id)["elements"]
    if len(weather_records) == 0:
        raise HTTPException(status_code=404, detail="WeatherStation sem medições")

    weather_records_out = [schemas.EstacaoRecordData(**schemas.WeatherRecordInDBBase.from_orm(weather_record).copy().dict()) for weather_record in weather_records]
    last_record_date = weather_records[0].date
    first_record_date = weather_records[-1].date


    estacao_data = schemas.EstacaoData(estacao_info=weather_station_db, start_date=first_record_date, end_date=last_record_date, condicoes_historicas=weather_records_out)
    return estacao_data

