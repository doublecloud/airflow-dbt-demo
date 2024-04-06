# Airflow DAGs for dbt

> The code in this repository is meant to demonstrate beginner and advanced implementation concepts
> at the intersection of dbt and Airflow.

## dbt project setup

We are currently using [the jaffle_shop sample dbt project](https://github.com/fishtown-analytics/jaffle_shop).
The only files required for the Airflow DAGs to run are `dbt_project.yml`, `profiles.yml` and `target/manifest.json`,
but we included the models for completeness. If you would like to try these DAGs with your own dbt workflow, feel free
to drop in your own project files.

## Notes

- To use these DAGs, Airflow 2.2+ is required. These DAGs have been tested with Airflow 2.7.1.
- If you make changes to the dbt project, you will need to run `dbt compile` in order to update the `manifest.json`
  file.
  This may be done manually during development, as part of a CI/CD pipeline, or as a separate step in a production
  pipeline run *before* the Airflow DAG is triggered.
- The sample dbt project contains the `profiles.yml`, which is configured to use environment variables. The
  database credentials from an Airflow connection are passed as environment variables to the `BashOperator`
  tasks running the dbt commands.
- Each DAG runs a `dbt_seed` task at the beginning that loads sample data into the database. This is simply for the
  purpose of this demo.
