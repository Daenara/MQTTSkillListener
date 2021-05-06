import logging
import configparser
import rhasspy_datetime

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp
from rhasspy_weather import weather

_LOGGER = logging.getLogger("SkillListener")


config = configparser.ConfigParser()
config.read('config.ini')
client = config["mqtt"]["client"]
server = config["mqtt"]["server"]
port = config["mqtt"].getint("port")
user = config["mqtt"]["user"]
password = config["mqtt"]["password"]

app = HermesApp(client, host=server, port=port, username=user, password=password)


@app.on_intent("GetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    return EndSession(rhasspy_datetime.get_time(config_path=config["rhasspy_datetime"]["config"]))


@app.on_intent("GetDate")
async def get_date(intent: NluIntent):
    """Tell the date."""
    return EndSession(rhasspy_datetime.get_date(config_path=config["rhasspy_datetime"]["config"]))


@app.on_intent("GetWeekday")
async def get_date(intent: NluIntent):
    """Tell the weekday."""
    return EndSession(rhasspy_datetime.get_weekday(config_path=config["rhasspy_datetime"]["config"]))


@app.on_intent("GetWeatherForecast")
@app.on_intent("GetWeatherForecastTemperature")
@app.on_intent("GetWeatherForecastCondition")
@app.on_intent("GetWeatherForecastItem")
async def get_weather(intent: NluIntent):
    """Get weather"""
    forecast = weather.get_weather_forecast(intent, config_path=config["rhasspy_weather"]["config"])
    return EndSession(forecast)


app.run()
