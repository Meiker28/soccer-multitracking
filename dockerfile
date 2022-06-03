FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/main.py"]