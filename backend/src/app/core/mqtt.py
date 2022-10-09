
import datetime
from decimal import Decimal
import json
import time
import paho.mqtt.client as paho
from paho import mqtt
from sqlalchemy.orm import Session
from backend.src.app import schemas
from backend.src.app.db.db_manager import CRUDWeatherRecord, CRUDWeatherStation
from backend.src.app.dependencies import get_db_standalone
from backend.src.config import settings

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):

    topic: str = msg.topic
    if topic.startswith("weatherlogger/medidas"):
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        m_in=json.loads(m_decode) #decode json data
        if "api_key" not in m_in:
            print("Mensagem MQTT Recebida sem weather_station_id")
        elif "date" not in m_in:
            print("Mensagem MQTT Recebida sem date")
        elif "temperature" not in m_in:
            print("Mensagem MQTT Recebida sem temperature")
        elif "heat_index" not in m_in:
            print("Mensagem MQTT Recebida sem heat_index")
        elif "dewpoint" not in m_in:
            print("Mensagem MQTT Recebida sem dewpoint")
        elif "humidity" not in m_in:
            print("Mensagem MQTT Recebida sem humidity")
        elif "pressure" not in m_in:
            print("Mensagem MQTT Recebida sem pressure")
        elif "dioxide_carbon_ppm" not in m_in:
            print("Mensagem MQTT Recebida sem dioxide_carbon_ppm")
        elif "rain_presence" not in m_in:
            print("Mensagem MQTT Recebida sem rain_presence")
        else:
            
            try:
                db: Session = get_db_standalone()
                
                api_key: str = m_in["api_key"]
                date: datetime = datetime.datetime.strptime(m_in["date"], "%Y-%m-%d %H:%M:%S")
                temperature: Decimal = Decimal(m_in["temperature"])
                heat_index: Decimal = Decimal(m_in["heat_index"])
                dewpoint: Decimal = Decimal(m_in["dewpoint"])
                humidity: Decimal = Decimal(m_in["humidity"])
                pressure: Decimal = Decimal(m_in["pressure"])
                dioxide_carbon_ppm: Decimal = Decimal(m_in["dioxide_carbon_ppm"])
                rain_presence: bool = True if m_in["rain_presence"] == "True" or m_in["rain_presence"] == "true" or m_in["rain_presence"] == True else False

                db_weather_station = CRUDWeatherStation.get_by_api_key(db=db, api_key=api_key)
                if db_weather_station is None:
                    print("Weather Station não encontrado")

                db_weather_record_exists = CRUDWeatherRecord.get_by_weather_station_id_and_date(db=db, weather_station_id=db_weather_station.id, date=date)
                if db_weather_record_exists is not None:
                    print("Weather Record com mesma data e estação já encontrado")
            
                weatherrecord_out = schemas.WeatherRecordCreateOut(weather_station_id=db_weather_station.id, weather_station=db_weather_station, date=date, temperature=temperature, heat_index=heat_index, dewpoint=dewpoint, humidity=humidity, pressure=pressure, dioxide_carbon_ppm=dioxide_carbon_ppm, rain_presence=rain_presence)
                CRUDWeatherRecord.create(db=db, item=weatherrecord_out)
            except Exception as e:
                print("Error: " + e)
            finally:
                db.close()

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASS)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("weatherlogger/medidas/#", qos=0)