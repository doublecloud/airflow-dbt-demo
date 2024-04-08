# Airflow DAGs for dbt

> The code in this repository is meant to demonstrate beginner and advanced implementation concepts
> at the intersection of dbt and Airflow.
> This repository complements this [presentation][presentation].

## dbt project setup

We are currently using [the jaffle_shop sample dbt project][jaffle_shop].
The only files required for the Airflow DAGs to run are `dbt_project.yml`, `profiles.yml` and `target/manifest.json`,
but we included the models for completeness. If you would like to try these DAGs with your own dbt workflow, feel free
to drop in your own project files.

## Services setup

### ClickHouse

This project uses ClickHouse Database, which can be spun up at Double
Cloud's [Managed ClickHouse](https://double.cloud/services/managed-clickhouse/) service free of charge as a trial
project.

### Airflow

CI/CD pipeline is designed with capabilities of Double
Cloud's [Managed Airflow](https://double.cloud/docs/en/managed-airflow/quickstart) custom images feature. Follow the
quick start guide to spin up a free Apache Airflow cluster and try out code examples provided.

## Notes

- To use these DAGs, Airflow 2.8+ is required. These DAGs have been tested with Airflow 2.8.1.
- If you make changes to the dbt project, you will need to run `dbt compile` in order to update the `manifest.json`
  file. This may be done manually during development, as part of a CI/CD pipeline. This has to be done prior the DAGs
  gets into Airflow as otherwise scheduler would not be able to build dynamic workflow out of dbt's manifest file.
- The sample dbt project contains the `profiles.yml`, which is configured to use environment variables. The
  database credentials from an Airflow connection are passed as environment variables to the `BashOperator`
  tasks running the dbt commands.
- Each DAG runs a `dbt_seed` task at the beginning that loads sample data into the database. This is simply for the
  purpose of this demo.

<!-- Links list -->

[presentation]: https://docs.google.com/presentation/d/1JcaIgGNmi2CRaM-fpxIb_7R1GsHFFKx1_cyL3YyUTkg/edit?usp=sharing

[jaffle_shop]: https://github.com/dbt-labs/jaffle_shop