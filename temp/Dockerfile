FROM postgres:alpine
ENV POSTGRES_DB fastapi_database
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD 2101
COPY init.sql /docker-entrypoint-initdb.d/