FROM ghcr.io/doublecloud/airflow:2.8.1

# custom extensions to the base image
COPY requirements.txt /usr/local/

# Make sure to define airflow version explicitly upon update
# to avoid unintentional version downgrade
# Ref: https://airflow.apache.org/docs/docker-stack/build.html#example-of-adding-packages-from-requirements-txt
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /usr/local/requirements.txt

# copy your dbt project into the image
COPY --chown=airflow:root dbt /usr/app/dbt
