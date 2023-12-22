FROM python:3.11-bullseye 

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# VARIABLES DE ENTORNO PARA EJECUTAR EL MODELO WHISPER
ARG API_KEY
ARG GOOGLE_KEY
ARG CORREO_PERSONAL
ARG CORREO_U

USER root
RUN apt-get update

COPY ./run.sh /opt
COPY ./requirements.txt /opt

CMD ["/bin/bash","/opt/run.sh"]