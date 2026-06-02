import pandas as pd
import requests
import psycopg2
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'etl_db',
    'user': 'etl_user',
    'password': 'etl_pass',
    'port': 5432
}

def ingest_data(**kwargs):
    logger.info('Starting data ingestion...')
    url = 'https://api.example.com/sales'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    raw_path = '/tmp/raw_sales.csv'
    df.to_csv(raw_path, index=False)
    logger.info(f'Ingested {len(df)} records to {raw_path}')
    return raw_path

def transform_data(**kwargs):
    logger.info('Starting data transformation...')
    df = pd.read_csv('/tmp/raw_sales.csv')
    df.dropna(subset=['sale_id', 'amount', 'sale_date'], inplace=True)
    df['sale_date'] = pd.to_datetime(df['sale_date']).dt.date
    df['amount'] = df['amount'].astype(float).round(2)
    df['year'] = pd.to_datetime(df['sale_date']).dt.year
    df['month'] = pd.to_datetime(df['sale_date']).dt.month
    df['processed_at'] = datetime.utcnow()
    transformed_path = '/tmp/transformed_sales.csv'
    df.to_csv(transformed_path, index=False)
    logger.info(f'Transformed {len(df)} records')
    return transformed_path

def load_data(**kwargs):
    logger.info('Starting data load to PostgreSQL...')
    df = pd.read_csv('/tmp/transformed_sales.csv')
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO processed_sales
            (sale_id, product_name, amount, sale_date, year, month, region, processed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sale_id) DO UPDATE SET
                amount = EXCLUDED.amount,
                processed_at = EXCLUDED.processed_at;
        """, (row['sale_id'], row['product_name'], row['amount'],
              row['sale_date'], row['year'], row['month'],
              row.get('region', 'Unknown'), row['processed_at']))
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f'Loaded {len(df)} records into processed_sales table')
