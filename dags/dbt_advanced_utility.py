"""
Shows how to parse a dbt manifest file to "explode" the dbt DAG into Airflow

Each dbt model is run as a bash command.
"""

from pendulum import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
# $AIRFLOW_HOME/dags is added to sys.path so we can use modules relative to `dags` root
from include.dbt_dag_parser import DbtDagParser

# We're hardcoding these values here for the purpose of the demo, but in a production environment these
# would probably come from a config file and/or environment variables!
DBT_PROJECT_DIR = "/usr/app/dbt"
DBT_BINARY = "/home/airflow/.local/bin/dbt"
DBT_GLOBAL_CLI_FLAGS = "--no-write-json --log-level=debug --no-quiet --debug"
DBT_TARGET = "dev"
DBT_TAG = "tag_staging"
DBT_CONNECTION_ENV = {
    "DBT_USER": "{{ conn.clickhouse_dwh.login }}",
    "DBT_ENV_SECRET_PASSWORD": "{{ conn.clickhouse_dwh.password }}",
    "DBT_HOST": "{{ conn.clickhouse_dwh.host }}",
    "DBT_SCHEMA": "{{ conn.clickhouse_dwh.schema }}",
    "DBT_PORT": "{{ conn.clickhouse_dwh.port }}",
}

with DAG(
        "dbt_advanced_dag_utility",
        start_date=datetime(2024, 4, 11),
        description="A dbt wrapper for Airflow using a utility class to map the dbt DAG to Airflow tasks",
        schedule_interval=None,
        catchup=False,
        doc_md=__doc__
) as dag:
    start_dummy = DummyOperator(task_id="start")
    # We're using the dbt seed command here to populate the database for the purpose of this demo
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=(
            f"{DBT_BINARY} {DBT_GLOBAL_CLI_FLAGS} seed "
            f"--profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}"
        ),
        env=DBT_CONNECTION_ENV,
    )
    end_dummy = DummyOperator(task_id="end")

    # The parser parses out a dbt manifest.json file and dynamically creates tasks for "dbt run" and "dbt test"
    # commands for each individual model. It groups them into task groups which we can retrieve and use in the DAG.
    dag_parser = DbtDagParser(
        dbt_global_cli_flags=DBT_GLOBAL_CLI_FLAGS,
        dbt_project_dir=DBT_PROJECT_DIR,
        dbt_profiles_dir=DBT_PROJECT_DIR,
        dbt_target=DBT_TARGET,
        dbt_binary=DBT_BINARY,
        dbt_env=DBT_CONNECTION_ENV,
    )
    dbt_run_group = dag_parser.get_dbt_run_group()
    dbt_test_group = dag_parser.get_dbt_test_group()

    start_dummy >> dbt_seed >> dbt_run_group >> dbt_test_group >> end_dummy
