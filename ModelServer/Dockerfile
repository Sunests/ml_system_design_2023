FROM python:3.11

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

COPY requirements.txt /tg_bot/requirements.txt

WORKDIR /tg_bot

RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .

CMD ["python3", "main.py"]
