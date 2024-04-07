FROM ghcr.io/doublecloud/airflow:2.8.1

# custom extensions to the base image
RUN pip install \
    dbt-core==1.7.11 \
    dbt-clickhouse==1.7.5 \
    airflow-clickhouse-plugin==1.2.0 \
    astronomer-cosmos==1.3.2

COPY --chown=airflow:root dbt /usr/app/dbt