📈 Stock Data ETL Pipeline with Airflow & Snowflake
This repository contains an Apache Airflow DAG that performs an end-to-end ETL (Extract, Transform, Load) process for Google stock data using the Alpha Vantage API. The transformed data is loaded into a Snowflake table for storage and analysis.

🚀 Project Overview
Source API: Alpha Vantage (TIME_SERIES_DAILY)

ETL Tool: Apache Airflow

Data Warehouse: Snowflake

Data Format: JSON → Pandas DataFrame → SQL

Schedule: Every 10 minutes (configurable via Airflow)

📂 File Structure
bash
.
├── stock_data_dag.py        # Main Airflow DAG for stock data ETL
└── README.md                # Project documentation

🔧 Prerequisites
Apache Airflow (2.5+ recommended)

Snowflake account with a configured connection in Airflow (snowflake_conn)

Alpha Vantage API key stored in Airflow Variables as alpha_vantage_api_key

🔁 ETL Flow
Extract:

Fetches the last 100 days of Google (GOOG) daily stock data via Alpha Vantage API.

Transform:

Converts JSON to a clean DataFrame.

Filters the last 90 days of stock records.

Load:

Creates or replaces a Snowflake table named STOCK_PRICES.

Inserts cleaned records into the STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES table using a transaction.

⚙️ Airflow Setup
Airflow Variable:

Add a variable:

makefile
Key: alpha_vantage_api_key  
Value: YOUR_ALPHA_VANTAGE_API_KEY
Airflow Connection:

Connection ID: snowflake_conn

Type: Snowflake

Include required credentials (account, user, password, database, schema, warehouse, role)

DAG Configuration:

The DAG is set to run every 10 minutes (*/10 * * * *)

Modify the schedule_interval or start_date as needed.

📊 Output Table Schema
Table: STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES

Column	Type	Description
date	DATE	Trading date (Primary)
open	FLOAT	Opening price
high	FLOAT	Highest price
low	FLOAT	Lowest price
close	FLOAT	Closing price
volume	FLOAT	Traded volume
symbol	STRING	Stock symbol (e.g., GOOG)

✅ Example Use Cases
Schedule automatic daily stock updates.

Analyze stock price trends using Snowflake SQL.

Extend DAG to include additional stocks.

📌 Notes
Ensure your Alpha Vantage API has enough quota.

Snowflake connector and provider must be installed in your Airflow environment:

bash
pip install snowflake-connector-python apache-airflow-providers-snowflake


📬 License
This project is for academic and educational use only.
