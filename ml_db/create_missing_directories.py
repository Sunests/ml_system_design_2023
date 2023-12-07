import os

# Задайте путь к основной директории PostgreSQL (обычно /var/lib/pgsql/ или /usr/local/pgsql/data)
postgres_data_directory = "/var/lib/postgresql/data"

# Список поддиректорий для создания
directories_to_create = [
    "pg_notify",
    "pg_tblspc",
    "pg_replslot",
    "pg_twophase",
    "pg_stat_tmp",
    "pg_logical/snapshots",
    "pg_logical/mappings",
    "pg_commit_ts",
    "pg_snapshots",
    "pg_commit_ts"
]

# Создание поддиректорий
for directory in directories_to_create:
    path = os.path.join(postgres_data_directory, directory)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Создана директория: {path}")
        except Exception as e:
            print(f"Ошибка при создании директории {path}: {e}")
    else:
        print(f"Директория уже существует: {path}")
