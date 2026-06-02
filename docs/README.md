# Week 2 - Automated ETL Data Pipeline

**Author:** Narendra  
**Email:** narendra@hashclicksolutions.com  
**Date:** June 1, 2026  
**Tools:** Apache Airflow 2.x + PostgreSQL

---

## Overview

A fully automated ETL pipeline using Apache Airflow for workflow orchestration. The pipeline ingests raw sales data from an external REST API, applies data quality transformations, and loads cleaned records into a PostgreSQL database on a daily schedule.

---

## Architecture

```
[API Source] --> [ingest_data Task] --> [raw_sales.csv]
     --> [transform_data Task] --> [transformed_sales.csv]
     --> [load_data Task] --> [PostgreSQL: processed_sales]
```

---

## DAG Details

| Property | Value |
|----------|-------|
| DAG ID | etl_sales_pipeline |
| Schedule | @daily (runs every day automatically) |
| Retries | 2 (5-minute delay between retries) |
| Catchup | Disabled |

---

## Task Breakdown

1. **ingest_data** - Pulls JSON from REST API, saves to `/tmp/raw_sales.csv`
2. **transform_data** - Cleans nulls, standardizes dates/amounts, adds year/month columns, saves to `/tmp/transformed_sales.csv`
3. **load_data** - Upserts records into PostgreSQL `processed_sales` table using `sale_id` as unique key

---

## Database Tables

| Table | Description |
|-------|-------------|
| raw_sales | Staging table for raw ingested records |
| processed_sales | Final cleaned and transformed sales data (5 sample rows included) |
| pipeline_logs | Audit log for each pipeline run |

---

## Setup Instructions

```bash
# 1. Install dependencies
pip install apache-airflow pandas psycopg2-binary requests

# 2. Initialize Airflow database
airflow db init

# 3. Create database schema
psql -f sql/schema.sql

# 4. Place DAG files
cp dags/etl_pipeline_dag.py $AIRFLOW_HOME/dags/
cp dags/pipeline.py $AIRFLOW_HOME/dags/

# 5. Start Airflow
airflow scheduler &
airflow webserver --port 8080
```

6. Enable the DAG in Airflow UI at http://localhost:8080

---

## Code Structure

```
/dags/
  etl_pipeline_dag.py  - Airflow DAG definition
  pipeline.py          - ETL functions (ingest, transform, load)
/sql/
  schema.sql           - Database schema and sample data
/docs/
  README.md            - This documentation
```

---

## Summary

All Week 2 tasks have been completed. The pipeline is fully automated with:
- Daily scheduling via Apache Airflow
- Retry logic (2 retries, 5-min delay)
- Structured ETL code (ingest, transform, load)
- PostgreSQL storage with upsert logic
- Proper audit logging via pipeline_logs table
