import pandas as pd
from sqlalchemy import create_engine

# Connection string for your Dockerized PostgreSQL database
DB_CONNECTION_URL = "postgresql://postgres:mypassword@localhost:5432/decision_intelligence"

def ingest_sales_data(csv_file_path):
    print("Reading Kaggle CSV file...")
    df = pd.read_csv(csv_file_path)
    
    # Rename columns to match PostgreSQL schema
    df.columns = ['sale_date', 'store_id', 'item_id', 'units_sold']
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    print("Connecting to PostgreSQL in Docker...")
    engine = create_engine(DB_CONNECTION_URL)

    print("Uploading data into PostgreSQL (this may take a minute)...")
    df.to_sql('store_sales', con=engine, if_exists='replace', index=False, chunksize=10000)
    
    print("Data ingestion complete!")

if __name__ == "__main__":
    ingest_sales_data("train.csv")