from airflow.decorators import dag, task  
from airflow.models import Variable
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime, timedelta
import requests
import pandas as pd
import snowflake.connector


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    description='Stock data ETL with Snowflake and Alpha Vantage',
    schedule_interval='*/10 * * * *',  # Set to None to trigger manually at the start_date
    start_date=datetime(2024, 10, 10),  # Run at 8:15 PM today (24-hour format)
    #end_date=datetime(2024, 10, 10),  # Prevent it from running again after today
    catchup=False,  # Disable catchup
)


def stock_data_etl():
    @task
    def extract_stock_data():
        """Extract stock data from Alpha Vantage API."""

        symbol = "GOOG"
        api_key = Variable.get("alpha_vantage_api_key")  # Fetch Alpha Vantage API key from Airflow Variables  
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact"
        response = requests.get(url)
        data = response.json()
        return data

    @task
    def transform_stock_data(stock_data):
        """Transform the extracted stock data."""

        symbol = "GOOG"
        time_series = stock_data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index').reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)
        df_90 = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=90))]
        df_90['symbol'] = symbol
        return df_90

    @task
    def load_stock_data_into_snowflake(stock_data_frame):
        """Load the transformed stock data into Snowflake."""

        hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")  # Use Snowflake connection from Airflow
        conn = hook.get_conn()
        cur = conn.cursor()

        create_table_query = """
        CREATE OR REPLACE TABLE STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES (
            date DATE PRIMARY KEY,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT,
            symbol STRING
        )
        """
        cur.execute(create_table_query)

        insert_query = """
        INSERT INTO STOCK_DATA_DATABASE.STOCK_DATA_SCHEMA.STOCK_PRICES (date, open, high, low, close, volume, symbol)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        try:
            stock_data_frame['date'] = stock_data_frame['date'].dt.strftime('%Y-%m-%d')
            cur.execute("BEGIN")

            for index, row in stock_data_frame.iterrows():
                #formatted_date = row['date'].strftime('%Y-%m-%d')
                cur.execute(insert_query, (row['date'], row['open'], row['high'], row['low'], row['close'], row['volume'], row['symbol']))

            cur.execute("COMMIT")
        except Exception as e:
            cur.execute("ROLLBACK")
            print(f"Error: {e}")
        finally:
            cur.close()

    # Define task order
    stock_data = extract_stock_data()
    df_stock = transform_stock_data(stock_data)
    load_stock_data_into_snowflake(df_stock)

stock_data_etl_dag = stock_data_etl()