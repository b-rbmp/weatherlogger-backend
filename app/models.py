

from sqlalchemy import Column, Integer, String, Boolean, Numeric, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .db.base_class import Base

# Modelo representando uma Estação meteorologica
class WeatherStation(Base):
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	api_key = Column(String(20), nullable=False, index=True, unique=True)
	name = Column(String(50), nullable=False, index=True)
	city = Column(String(50), nullable=False, index=True)
	country = Column(String(50), nullable=False, index=True)
	latitude = Column(Numeric(12,6), nullable=True)
	longitude = Column(Numeric(12,6), nullable=True)
	altitude = Column(Numeric(12,6), nullable=True)

	weather_records = relationship("WeatherRecord", back_populates="weather_station", cascade="all, delete-orphan")

	# Função de Hasheamento para uso em Sets, por exemplo, de forma a representar unicamente o objeto
	def __hash__(self):
		return hash((self.id))

	# Função de comparação para saber se uma account é igual a outra
	def __eq__(self, other):
		if not isinstance(other, type(self)): return NotImplemented
		return self.id == other.id

# Modelo representando uma Medição
class WeatherRecord(Base):
	weather_station_id = Column(Integer, ForeignKey("weatherstation.id"), index=True, primary_key=True, autoincrement=False)
	date = Column(DateTime(), nullable=False, index=True, primary_key=True, autoincrement=False)
	temperature = Column(Numeric(12,4), nullable=True)
	heat_index = Column(Numeric(12,4), nullable=True)
	dewpoint = Column(Numeric(12,4), nullable=True)
	humidity = Column(Numeric(12,4), nullable=True)
	pressure = Column(Numeric(12,4), nullable=True)
	dioxide_carbon_ppm = Column(Numeric(12,4), nullable=True)
	rain_presence = Column(Boolean, nullable=True)

	weather_station = relationship("WeatherStation")

	# Função de Hasheamento para uso em Sets, por exemplo, de forma a representar unicamente o objeto
	def __hash__(self):
		return hash((self.id))

	# Função de comparação para saber se uma account é igual a outra
	def __eq__(self, other):
		if not isinstance(other, type(self)): return NotImplemented
		return self.id == other.id

