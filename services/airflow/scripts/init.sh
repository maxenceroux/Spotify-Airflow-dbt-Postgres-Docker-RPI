#!/usr/bin/env bash

AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN

DBT_POSTGRESQL_CONN="postgresql+psycopg2://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:5432/${DBT_POSTGRES_DB}"

cd /services/airflow/dbt && echo "sndiqnd" dbt compile

rm /services/airflow/airflow/airflow-webserver.pid

airflow initdb
sleep 10
airflow connections --add --conn_id 'dbt_postgres_instance_raw_data' --conn_uri $DBT_POSTGRESQL_CONN
airflow connections --add --conn_id 'spotify' --conn_type 'HTTP' --conn_host 'web' --conn_port '8000'
airflow scheduler & airflow webserver

