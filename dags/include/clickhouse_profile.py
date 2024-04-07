"""
Maps Airflow SQLite connections using user + password authentication to dbt clickhouse profile.
"""

from __future__ import annotations

from typing import Any

from cosmos.profiles.base import BaseProfileMapping


class ClickhouseUserPasswordProfileMapping(BaseProfileMapping):
    """
    Maps Airflow SQLite connections using user + password authentication to dbt Clickhouse profiles.
    https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup
    """

    airflow_connection_type: str = "sqlite"
    dbt_profile_type: str = "clickhouse"
    default_port = 9443

    required_fields = [
        "host",
        "login",
        "schema",
        "clickhouse",
    ]
    secret_fields = [
        "password",
    ]
    airflow_param_mapping = {
        "host": "host",
        "login": "login",
        "password": "password",
        "port": "port",
        "schema": "schema",
        "clickhouse": "extra.clickhouse",
    }

    @property
    def profile(self) -> dict[str, Any | None]:
        """
        Gets profile. The password is stored in an environment variable
        """
        profile = {
            "type": self.dbt_profile_type,
            "schema": self.conn.schema,
            "user": self.conn.login,
            # password should always get set as env var
            "password": self.get_env_var_format("password"),
            "driver": self.conn.extra_dejson.get("driver") or "http",
            "port": self.conn.port or self.default_port,
            "host": self.conn.host,
            "secure": self.conn.extra_dejson.get("secure") or True,
            "verify": self.conn.extra_dejson.get("verify") or False,
            **self.profile_args,
        }

        return self.filter_null(profile)
