import pandas as pd
from sqlalchemy import create_engine

# Connection string for your Dockerized PostgreSQL database
DB_CONNECTION_URL = "postgresql://postgres:mypassword@localhost:5432/decision_intelligence"

def explore_database():
    print("Connecting to PostgreSQL in Docker...")
    engine = create_engine(DB_CONNECTION_URL)

    # 1. Check total row count
    print("\n--- Total Row Count ---")
    row_count = pd.read_sql("SELECT COUNT(*) AS total_rows FROM store_sales;", con=engine)
    print(row_count)

    # 2. Check date range and unique stores/items
    print("\n--- Dataset Metadata & Date Range ---")
    metadata_query = """
        SELECT 
            MIN(sale_date) AS start_date, 
            MAX(sale_date) AS end_date,
            COUNT(DISTINCT store_id) AS total_stores,
            COUNT(DISTINCT item_id) AS total_items
        FROM store_sales;
    """
    metadata_df = pd.read_sql(metadata_query, con=engine)
    print(metadata_df)

    # 3. Check summary statistics for units sold
    print("\n--- Summary Statistics (Units Sold) ---")
    stats_query = """
        SELECT 
            ROUND(AVG(units_sold), 2) AS avg_units,
            MAX(units_sold) AS max_units,
            MIN(units_sold) AS min_units
        FROM store_sales;
    """
    stats_df = pd.read_sql(stats_query, con=engine)
    print(stats_df)

    # 4. Pull a small sample chunk to view the raw structure
    print("\n--- Sample Data Rows ---")
    sample_df = pd.read_sql("SELECT * FROM store_sales LIMIT 5;", con=engine)
    print(sample_df)

    print("\nData exploration complete!")

if __name__ == "__main__":
    explore_database()