"""
Shows dynamic DAG configuration using Cosmos library
"""

from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

# We're hardcoding this value here for the purpose of the demo, but in a production environment this
# would probably come from a config file and/or environment variables!
DBT_PROJECT_DIR = Path("/usr/app/dbt")
DBT_CONNECTION_ENV = {
    "DBT_USER": "{{ conn.clickhouse_dwh.login }}",
    "DBT_ENV_SECRET_PASSWORD": "{{ conn.clickhouse_dwh.password }}",
    "DBT_HOST": "{{ conn.clickhouse_dwh.host }}",
    "DBT_SCHEMA": "{{ conn.clickhouse_dwh.schema }}",
    "DBT_PORT": "{{ conn.clickhouse_dwh.port }}",
}

with DAG(
        "dbt_advanced_cosmos",
        start_date=datetime(2024, 4, 11),
        description="A dbt DAG execution using Cosmos library",
        schedule_interval=None,
        catchup=False,
        doc_md=__doc__
) as dag:
    """
    The simplest example of using Cosmos to render a dbt project as a TaskGroup.
    """
    pre_dbt = EmptyOperator(task_id="start")

    jaffle_shop = DbtTaskGroup(
        group_id="my_jaffle_shop_project",
        project_config=ProjectConfig(
            dbt_project_path=DBT_PROJECT_DIR,
            env_vars=DBT_CONNECTION_ENV,
        ),
        profile_config=ProfileConfig(
            # these map to dbt/profiles.yml
            profile_name="jaffle_shop",
            target_name="dev",
            profiles_yml_filepath=DBT_PROJECT_DIR / "profiles.yml",
        ),
        execution_config=ExecutionConfig(),
    )

    post_dbt = EmptyOperator(task_id="end")

    pre_dbt >> jaffle_shop >> post_dbt
