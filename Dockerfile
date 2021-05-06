FROM python:3.7
RUN apt-get update && apt-get install -y git python3-pip && \
	pip install rhasspy-hermes-app rhasspy-hermes && \
	git clone https://github.com/Daenara/rhasspy_weather.git && \
	pip install ./rhasspy_weather \
	git clone https://github.com/Daenara/rhasspy_datetime.git && \
	pip install ./rhasspy_datetime

COPY rhasspy_weather_config.ini /
COPY rhasspy_datetime_config.ini /
COPY SkillListener.py /
COPY config.ini /
	
WORKDIR /
ENTRYPOINT ["python", "-u", "SkillListener.py"]