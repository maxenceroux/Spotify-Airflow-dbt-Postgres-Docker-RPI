FROM maxenceroux/airflow:latest

RUN mkdir /airflow
ADD airflow/ /airflow/

RUN mkdir /dbt
ADD dbt/ /dbt/

ADD scripts/ /project/scripts/
RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]