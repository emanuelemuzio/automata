FROM postgres:16

RUN apt-get update && apt-get install -y \
    postgresql-16-pgvector \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432