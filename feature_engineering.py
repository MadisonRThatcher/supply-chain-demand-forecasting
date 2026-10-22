import pandas as pd
from sqlalchemy import create_engine

DB_CONNECTION_URL = "postgresql://postgres:mypassword@localhost:5432/decision_intelligence"

def build_features():
    print("Connecting to PostgreSQL to pull training data...")
    engine = create_engine(DB_CONNECTION_URL)

    # Pull data ordered chronologically by store, item, and date
    query = """
        SELECT sale_date, store_id, item_id, units_sold 
        FROM store_sales 
        ORDER BY store_id, item_id, sale_date;
    """
    df = pd.read_sql(query, con=engine)
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    print("Engineering time-series features...")
    
    # 1. Date-part extractions (helps the model learn seasonality)
    df['year'] = df['sale_date'].dt.year
    df['month'] = df['sale_date'].dt.month
    df['day'] = df['sale_date'].dt.day
    df['day_of_week'] = df['sale_date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

    # 2. Lag features (sales from 1 day prior, grouped by store and item)
    # This tells the model what the item sold for yesterday
    df['lag_1'] = df.groupby(['store_id', 'item_id'])['units_sold'].shift(1)
    
    # 3. Rolling window features (e.g., 7-day moving average of sales)
    df['rolling_mean_7'] = (
        df.groupby(['store_id', 'item_id'])['units_sold']
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    # Drop rows with NaN values created by shifts/rolling windows at the start of timelines
    df = df.dropna()

    print(f"Feature engineering complete! Final dataset shape: {df.shape}")
    
    # Save the engineered features back to a new table in PostgreSQL so we can train on it later
    print("Saving engineered features back to PostgreSQL...")
    df.to_sql('store_sales_features', con=engine, if_exists='replace', index=False, chunksize=10000)
    print("Engineered feature table 'store_sales_features' successfully created!")

if __name__ == "__main__":
    build_features()