-- ETL Sales Pipeline - Database Schema
-- Author: Narendra
-- Date: June 1, 2026

CREATE DATABASE etl_db;

-- Raw staging table for ingested records
CREATE TABLE IF NOT EXISTS raw_sales (
    id SERIAL PRIMARY KEY,
    sale_id VARCHAR(50),
    product_name VARCHAR(200),
    amount NUMERIC(12, 2),
    sale_date DATE,
    region VARCHAR(100),
    customer_id VARCHAR(50),
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Processed/transformed sales data
CREATE TABLE IF NOT EXISTS processed_sales (
    id SERIAL PRIMARY KEY,
    sale_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200),
    amount NUMERIC(12, 2),
    sale_date DATE,
    year INT,
    month INT,
    region VARCHAR(100),
    processed_at TIMESTAMP DEFAULT NOW()
);

-- Pipeline audit log
CREATE TABLE IF NOT EXISTS pipeline_logs (
    id SERIAL PRIMARY KEY,
    dag_id VARCHAR(100),
    run_id VARCHAR(200),
    status VARCHAR(50),
    records_processed INT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Sample processed data
INSERT INTO processed_sales (sale_id, product_name, amount, sale_date, year, month, region, processed_at) VALUES
('S001', 'Widget A', 250.00, '2026-05-01', 2026, 5, 'North', NOW()),
('S002', 'Widget B', 175.50, '2026-05-02', 2026, 5, 'South', NOW()),
('S003', 'Gadget X', 499.99, '2026-05-03', 2026, 5, 'East', NOW()),
('S004', 'Gadget Y', 320.75, '2026-05-04', 2026, 5, 'West', NOW()),
('S005', 'Widget A', 250.00, '2026-05-05', 2026, 5, 'North', NOW());
