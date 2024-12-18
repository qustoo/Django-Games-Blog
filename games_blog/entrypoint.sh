#!/bin/sh
echo "Проверка работы базы данных..."
if [ "$DATABASE" = "postgres" ]
then
    echo "Postgres еще не запущен..."

    # Проверяем доступность хоста и порта
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 10
    done

    echo "PostgreSQL запущен"
fi

exec "$@"


