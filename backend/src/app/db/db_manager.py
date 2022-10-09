import decimal
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, tuple_
from sqlalchemy import func, distinct
from datetime import date, datetime, timedelta


from backend.src.app import models, schemas
from backend.src.app.db.db import engine

class CRUDWeatherStation:

    @staticmethod
    def get_by_id(db: Session, id: int) -> models.WeatherStation | None:
        return db.query(models.WeatherStation).filter(models.WeatherStation.id == id).first()

    @staticmethod
    def get_by_api_key(db: Session, api_key: str) -> models.WeatherStation | None:
        return db.query(models.WeatherStation).filter(models.WeatherStation.api_key == api_key).first()


    @staticmethod
    def create(db: Session, item: schemas.WeatherStationCreateOut):

        db_item = models.WeatherStation()
        # Update model class variable from requested fields
        for var, value in vars(item).items():
            setattr(db_item, var, value) if value is not None else None
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_list(

        db: Session,
        skip: Optional[int],
        limit: Optional[int],
        api_key: Optional[str] = None,
        name: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Dict[List[models.WeatherStation], int]:

        response_get = {"elements": List[models.WeatherStation], "count-total": int}

        query_result = db.query(models.WeatherStation)

        # Filters
        if api_key is not None:
            query_result = query_result.filter(models.WeatherStation.api_key == api_key)

        if name is not None:
            query_result = query_result.filter(models.WeatherStation.name == name)
    
        if city is not None:
            query_result = query_result.filter(models.WeatherStation.city == city)

        if country is not None:
            query_result = query_result.filter(models.WeatherStation.country == country)

        response_get["total-count"] = str(query_result.count())

        if skip is not None and limit is not None:
            query_result = query_result.offset(skip).limit(limit)
        
        response_get["elements"] = query_result.all()

        return response_get

    @staticmethod
    def update(
        db: Session, item: schemas.WeatherStationUpdateIn, db_item: models.WeatherStation
    ):

        # Update model class variable from requested fields
        for var, value in vars(item).items():
            setattr(db_item, var, value) if value is not None else None

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete(db: Session, db_item: models.WeatherStation) -> bool:
        db.delete(db_item)
        db.commit()
        return True

    @staticmethod
    def count_all(db: Session) -> int:
        return db.query(distinct(models.WeatherStation.id)).count()

    @staticmethod
    def count_connected(db: Session, number_of_hours: int) -> int:
        time_now = datetime.now()
        time_start = time_now - timedelta(hours=number_of_hours)
        num_estacoes_conectadas = db.query(models.WeatherRecord).filter(models.WeatherRecord.date >= time_start).distinct(models.WeatherRecord.weather_station_id).count()

        return num_estacoes_conectadas

    @staticmethod
    def count_connected_daily(db: Session, number_of_days: int) -> List[schemas.EvolucaoConectividadeData]:
        time_now = datetime.now()
        time_start = time_now - timedelta(days=number_of_days)
        query = db.query(func.date(models.WeatherRecord.date), func.count(distinct(tuple_(models.WeatherRecord.weather_station_id, models.WeatherRecord.date)))).filter(models.WeatherRecord.date >= time_start).group_by(func.date(models.WeatherRecord.date))

        response = query.all()

        return response

class CRUDWeatherRecord:

    @staticmethod
    def get_by_weather_station_id_and_date(db: Session, weather_station_id: int, date: datetime):
        return db.query(models.WeatherRecord).filter(and_(models.WeatherRecord.weather_station_id == weather_station_id, models.WeatherRecord.date == date)).first()

    @staticmethod
    def create(db: Session, item: schemas.WeatherRecordCreateOut):

        db_item = models.WeatherRecord()
        # Update model class variable from requested fields
        for var, value in vars(item).items():
            setattr(db_item, var, value) if value is not None else None
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_list(

        db: Session,
        skip: Optional[int],
        limit: Optional[int],
        weather_station_id: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Dict[List[models.WeatherRecord], int]:

        response_get = {"elements": List[models.WeatherRecord], "count-total": int}

        query_result = db.query(models.WeatherRecord)

        # Filters
        if weather_station_id is not None:
            query_result = query_result.filter(models.WeatherRecord.weather_station_id == weather_station_id)

        if data_inicial:
            query_result = query_result.filter(models.WeatherRecord.date >= data_inicial)

        if data_final:
            query_result = query_result.filter(models.WeatherRecord.date <= data_final)


        response_get["total-count"] = str(query_result.count())

        query_result = query_result.order_by(models.WeatherRecord.date.desc())

        if skip is not None and limit is not None:
            query_result = query_result.offset(skip).limit(limit)
        
        response_get["elements"] = query_result.all()

        return response_get

    @staticmethod
    def update(
        db: Session, item: schemas.WeatherRecordUpdateIn, db_item: models.WeatherRecord
    ):

        # Update model class variable from requested fields
        for var, value in vars(item).items():
            setattr(db_item, var, value) if value is not None else None

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete(db: Session, db_item: models.WeatherRecord) -> bool:
        db.delete(db_item)
        db.commit()
        return True

    @staticmethod
    def count_all(db: Session) -> int:
        return db.query(distinct(tuple_(models.WeatherRecord.weather_station_id, models.WeatherRecord.date))).count()

    @staticmethod
    def get_last_record(db: Session) -> models.WeatherRecord:

        return db.query(models.WeatherRecord).order_by(models.WeatherRecord.date.desc()).first()