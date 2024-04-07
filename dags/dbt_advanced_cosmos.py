"""
Shows dynamic DAG configuration using Cosmos library
"""

from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig

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

dbt_cosmos_example = DbtDag(
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
    # ExecutionConfig is able to infer default dbt path from environment
    execution_config=ExecutionConfig(),
    # normal dag parameters
    dag_id="dbt_cosmos_example",
)
