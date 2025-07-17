#!/bin/bash
export TEMP_DB_CONTAINER="tmp-db-migration"
export DB_PORT=11500
export VICTORIA_DATABASE_URL="postgresql://user:pass@localhost:$DB_PORT/migration_db"

docker run --rm -d \
    --name $TEMP_DB_CONTAINER \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_DB=migration_db \
    -p $DB_PORT:5432 \
    postgres:16

until docker exec $TEMP_DB_CONTAINER pg_isready -U user > /dev/null 2>&1; do
    sleep 0.5;
done

cd victoria-backend
poetry run alembic upgrade head && 
poetry run alembic revision --autogenerate -m "$1"

docker stop $TEMP_DB_CONTAINER