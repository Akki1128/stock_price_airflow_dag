Stock Data ETL Pipeline
An automated data pipeline that extracts stock data from Alpha Vantage, transforms it, and loads it into Snowflake using Apache Airflow.
Overview
This project implements an ETL (Extract, Transform, Load) pipeline for stock market data using Apache Airflow as the orchestration tool. The pipeline fetches daily stock prices from the Alpha Vantage API, performs necessary transformations, and loads the data into a Snowflake database for further analysis.
Features

Automated Data Extraction: Fetches daily stock data from Alpha Vantage API
Data Transformation: Processes and formats the stock data for database loading
Snowflake Integration: Loads the transformed data into a Snowflake data warehouse
Scheduled Execution: Runs automatically on a configurable schedule (currently set to every 10 minutes)

Pipeline Architecture
The DAG consists of three main tasks:

Extract: Retrieves stock data from the Alpha Vantage API
Transform: Converts the raw JSON data into a structured DataFrame and filters for the last 90 days
Load: Inserts the transformed data into a Snowflake database

Prerequisites

Python 3.7+
Apache Airflow 2.0+
Snowflake account
Alpha Vantage API key

Required Python Packages

apache-airflow
apache-airflow-providers-snowflake
pandas
requests
snowflake-connector-python

Setup Instructions
1. Clone the Repository
bashgit clone https://github.com/yourusername/stock-data-etl.git
cd stock-data-etl
2. Install Dependencies
bashpip install apache-airflow apache-airflow-providers-snowflake pandas requests snowflake-connector-python
3. Configure Airflow
Set up Airflow connections and variables:

Snowflake Connection:

Connection ID: snowflake_conn
Connection Type: Snowflake
Host: your-snowflake-account.snowflakecomputing.com
Schema: STOCK_DATA_SCHEMA
Login: your_username
Password: your_password
Database: STOCK_DATA_DATABASE
Warehouse: your_warehouse
Role: your_role


Alpha Vantage API Key:

Variable Key: alpha_vantage_api_key
Variable Value: your_alpha_vantage_api_key



4. Deploy the DAG
Place the stock_data_dag.py file in your Airflow DAGs folder:
bashcp stock_data_dag.py ~/airflow/dags/
Snowflake Setup
The DAG will automatically create the necessary table in Snowflake. However, ensure that the database and schema already exist:
sql-- Create database and schema if they don't exist
CREATE DATABASE IF NOT EXISTS STOCK_DATA_DATABASE;
CREATE SCHEMA IF NOT EXISTS STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA;
Configuration Options
You can modify the following parameters in the DAG file:

schedule_interval: Frequency of pipeline execution (currently set to every 10 minutes)
symbol: Stock symbol to track (currently set to "GOOG")
Time range for historical data (currently set to last 90 days)

Usage
Once deployed, the DAG will run automatically based on the schedule_interval. You can also trigger it manually from the Airflow UI.
The data will be available in the STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES table in Snowflake.
Sample Query
After the pipeline has run, you can query the data in Snowflake:
sqlSELECT 
    date,
    symbol,
    open,
    high,
    low,
    close,
    volume
FROM STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES
ORDER BY date DESC
LIMIT 10;
Future Improvements

Add support for multiple stock symbols
Implement data quality checks
Add visualization dashboard
Configure email notifications for pipeline failures
Implement incremental loading to avoid duplicate data
