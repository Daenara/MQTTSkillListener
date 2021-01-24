import logging
from datetime import datetime
import configparser

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
    hours = datetime.now().hour
    minutes = datetime.now().minute
    if minutes == 0:
        return EndSession(f"Es ist {hours} Uhr.")
    return EndSession(f"Es ist {hours} Uhr {minutes}.")


@app.on_intent("GetWeatherForecast")
@app.on_intent("GetWeatherForecastTemperature")
@app.on_intent("GetWeatherForecastCondition")
@app.on_intent("GetWeatherForecastItem")
async def get_weather(intent: NluIntent):
    """Get weather"""
    forecast = weather.get_weather_forecast(intent, config_path=config["rhasspy_weather"]["config"])
    return EndSession(forecast)


app.run()
