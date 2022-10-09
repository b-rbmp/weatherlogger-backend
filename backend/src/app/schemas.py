
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from pydantic.main import BaseModel

from backend.src.app import models



class HashableBaseModel(BaseModel):
    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))

class WeatherStationBase(HashableBaseModel):
	api_key: Optional[str]
	name: Optional[str]
	city: Optional[str]
	country: Optional[str]
	latitude: Optional[Decimal]
	longitude: Optional[Decimal]
	altitude: Optional[Decimal]

class WeatherStationInDBBase(WeatherStationBase):
    id: int

    class Config:
        orm_mode = True

class WeatherStationCreateIn(WeatherStationBase):
	api_key: str
	name: str
	city: str
	country: str

class WeatherStationCreateOut(WeatherStationCreateIn):
    pass

class WeatherStationUpdateIn(WeatherStationBase):
    pass

class WeatherStationUpdateOut(WeatherStationUpdateIn):
    pass

class WeatherRecordBase(HashableBaseModel):
	weather_station_id: Optional[int]
	date: Optional[datetime]
	temperature: Optional[Decimal]
	heat_index: Optional[Decimal]
	dewpoint: Optional[Decimal]
	humidity: Optional[Decimal]
	pressure: Optional[Decimal]
	dioxide_carbon_ppm: Optional[Decimal]
	rain_presence: Optional[bool]


class WeatherRecordInDBBase(WeatherRecordBase):
    weather_station_id: int
    date: datetime
    weather_station: WeatherStationInDBBase
    class Config:
        orm_mode = True

class WeatherRecordCreateIn(WeatherRecordBase):
    pass

class WeatherRecordCreateOut(WeatherRecordBase):
    weather_station: models.WeatherStation

    class Config:
        arbitrary_types_allowed = True


class WeatherRecordUpdateIn(WeatherRecordBase):
    pass

class WeatherRecordUpdateOut(WeatherRecordBase):
    weather_station: models.WeatherStation

    class Config:
        arbitrary_types_allowed = True


class PreviewStation(HashableBaseModel):
	estacao: WeatherStationInDBBase
	record: WeatherRecordInDBBase

	class Config:
		arbitrary_types_allowed = True

class EvolucaoConectividadeData(HashableBaseModel):
	date: date
	connected: int

class GlobalData(HashableBaseModel):
	estacoes_registradas: int
	estacoes_conectadas: int
	numero_amostras: int
	ultima_amostra: str
	stations: List[WeatherStationInDBBase]
	preview_station: PreviewStation | str
	evolucao_conectividade: List[EvolucaoConectividadeData]

	class Config:
		arbitrary_types_allowed = True

class EstacaoRecordData(HashableBaseModel):
	date: datetime
	temperature: Decimal
	heat_index: Decimal
	dewpoint: Decimal
	humidity: Decimal
	pressure: Decimal
	dioxide_carbon_ppm: Decimal
	rain_presence: bool
	
class EstacaoData(HashableBaseModel):
	estacao_info: WeatherStationInDBBase
	start_date: datetime
	end_date: datetime
	condicoes_historicas: List[EstacaoRecordData]

