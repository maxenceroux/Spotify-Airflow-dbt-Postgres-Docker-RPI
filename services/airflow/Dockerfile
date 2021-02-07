FROM maxenceroux/airflow:latest

RUN mkdir /airflow
COPY airflow/ /airflow/

RUN mkdir /dbt
COPY dbt/ /dbt/

COPY scripts/ /project/scripts/

RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]