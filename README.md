# ETL Sales Pipeline

> **Week 2 Submission** | Automated ETL Data Pipeline | Apache Airflow + PostgreSQL

**Author:** Narendra | narendra@hashclicksolutions.com  
**Date:** June 1, 2026

---

## Repository Structure

```
etl-sales-pipeline/
├── README.md                    <- This file
├── dags/
│   ├── etl_pipeline_dag.py      <- Airflow DAG definition (Deliverable 1)
│   └── pipeline.py              <- ETL functions: ingest, transform, load (Deliverable 2)
├── sql/
│   └── schema.sql               <- DB schema + 5 sample rows (Deliverable 3)
└── docs/
    └── README.md                <- Full project documentation (Deliverable 4)
```

---

## Quick Start

```bash
pip install apache-airflow pandas psycopg2-binary requests
airflow db init
psql -f sql/schema.sql
cp dags/*.py $AIRFLOW_HOME/dags/
airflow scheduler & airflow webserver --port 8080
```

Enable the `etl_sales_pipeline` DAG in the Airflow UI at http://localhost:8080

---

## Pipeline Flow

```
[REST API] --> ingest_data --> [raw_sales.csv]
           --> transform_data --> [transformed_sales.csv]
           --> load_data --> [PostgreSQL: processed_sales]
```

| DAG Property | Value |
|---|---|
| DAG ID | etl_sales_pipeline |
| Schedule | @daily |
| Retries | 2 (5-min delay) |
| Catchup | Disabled |

---

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Apache Airflow DAG | `dags/etl_pipeline_dag.py` |
| 2 | ETL Pipeline Code | `dags/pipeline.py` |
| 3 | Database Schema | `sql/schema.sql` |
| 4 | Documentation | `docs/README.md` |

---

For full documentation see [docs/README.md](docs/README.md)
