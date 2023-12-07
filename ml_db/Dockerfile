FROM postgres:15

# Установка переменных окружения
ENV POSTGRES_DB ml_db
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD 1234
ENV PGDATA /var/lib/postgresql/data

COPY create_missing_directories.py /scripts/create_missing_directories.py

RUN apt-get update && apt-get install -y python3

CMD ["bash", "-c", "python3 /scripts/create_missing_directories.py && tail -f /dev/null"]