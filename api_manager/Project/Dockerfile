FROM python:3.11

COPY requirements.txt /api_manager/requirements.txt

WORKDIR /api_manager

RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .

CMD ["python3", "test.py"]
