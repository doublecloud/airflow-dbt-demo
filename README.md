# Airflow DAGs for dbt

> The code in this repository demonstrates beginner and advanced implementation concepts
> at the intersection of dbt and Airflow.
> This repository complements this [presentation][presentation].

## dbt project setup

We are currently using [the jaffle_shop sample dbt project][jaffle_shop].
Airflow DAGs only need the `dbt_project.yml`, `profiles.yml`, and `target/manifest.json` files to run,
but we also included the models for completeness. If you would like to try these DAGs with your own dbt workflow,
feel free to add your own project files.

## Service setup

### ClickHouse

This project uses ClickHouse. You can deploy a [Managed ClickHouse](https://double.cloud/services/managed-clickhouse/) 
cluster on DoubleCloud for free using trial period credits.

### Airflow

The CI/CD pipeline uses the custom images feature available in DoubleCloud's 
[Managed Airflow](https://double.cloud/docs/en/managed-airflow/quickstart) service.
Follow the quick start guide to run a free Apache Airflow cluster and try out the provided code examples.

## Notes

- Airflow 2.8+ is required to use these DAGs. They have been tested with Airflow 2.8.1.
- If you make changes to the dbt project, you need to run `dbt compile` to update the `manifest.json` file. 
   You can do it manually during development or in a CI/CD pipeline. This has to be done before the DAGs
   get into Airflow — otherwise the scheduler wouldn't be able to build dynamic workflow from dbt's manifest file.
- The example dbt project contains `profiles.yml` that is configured to use environment variables. The
  database credentials from an Airflow connection are passed as environment variables to the `BashOperator`
  tasks running the dbt commands.
- Each DAG runs a `dbt_seed` task at the beginning that loads sample data into the database. This is simply for the
  purpose of this demo.

<!-- Links list -->

[presentation]: https://docs.google.com/presentation/d/1JcaIgGNmi2CRaM-fpxIb_7R1GsHFFKx1_cyL3YyUTkg/edit?usp=sharing

[jaffle_shop]: https://github.com/dbt-labs/jaffle_shop
