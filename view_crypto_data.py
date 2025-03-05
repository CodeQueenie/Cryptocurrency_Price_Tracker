"""
Cryptocurrency Data Viewer

A simple script to view the cryptocurrency data stored in your database.
"""

import pandas as pd
import os
from sqlalchemy import create_engine, text
from tabulate import tabulate
from dotenv import load_dotenv

def connect_to_database():
    """Connect to the crypto_tracker database."""
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        load_dotenv()
    
    # Get database configuration from environment variables or use defaults
    db_type = os.getenv("DB_TYPE", "postgresql")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")  # Standard PostgreSQL port
    db_name = os.getenv("DB_NAME", "crypto_tracker")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "your_password")  # Generic default
    
    # Create connection string
    conn_str = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(conn_str)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Successfully connected to database: {db_name}")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_latest_prices(engine):
    """Get the latest prices for all cryptocurrencies."""
    query = """
    SELECT coin_id, name, symbol, current_price, 
           price_change_percentage_24h, market_cap, 
           last_updated
    FROM crypto_prices
    WHERE (coin_id, timestamp) IN (
        SELECT coin_id, MAX(timestamp) 
        FROM crypto_prices 
        GROUP BY coin_id
    )
    ORDER BY market_cap DESC;
    """
    
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def get_price_history(engine, coin_id, limit=10):
    """Get price history for a specific cryptocurrency."""
    query = """
    SELECT coin_id, name, symbol, current_price, 
           price_change_percentage_24h, 
           timestamp, last_updated
    FROM crypto_prices
    WHERE coin_id = :coin_id
    ORDER BY timestamp DESC
    LIMIT :limit;
    """
    
    try:
        df = pd.read_sql(query, engine, params={"coin_id": coin_id, "limit": limit})
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def display_results(df, title):
    """Display query results in a formatted table."""
    print(f"\n{title}")
    print("=" * 80)
    
    if df.empty:
        print("No results found.")
        return
    
    # Format the output using tabulate
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

def main():
    """Main function to run the data viewer."""
    print("Cryptocurrency Data Viewer")
    print("=" * 80)
    
    # Connect to database
    engine = connect_to_database()
    if not engine:
        return
    
    while True:
        print("\nOptions:")
        print("1. View latest cryptocurrency prices")
        print("2. View price history for a specific cryptocurrency")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # View latest prices
            df = get_latest_prices(engine)
            display_results(df, "Latest Cryptocurrency Prices")
            
        elif choice == '2':
            # View price history
            coins = ["bitcoin", "ethereum", "ripple", "cardano", "solana", 
                     "dogecoin", "polkadot", "litecoin", "chainlink", "stellar"]
            
            print("\nAvailable cryptocurrencies:")
            for i, coin in enumerate(coins, 1):
                print(f"{i}. {coin}")
            
            coin_choice = input("\nEnter cryptocurrency number or name: ").strip()
            
            # Check if input is a number
            if coin_choice.isdigit() and 1 <= int(coin_choice) <= len(coins):
                coin_id = coins[int(coin_choice) - 1]
            else:
                coin_id = coin_choice.lower()
            
            limit = input("Enter number of records to show (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            
            df = get_price_history(engine, coin_id, limit)
            display_results(df, f"Price History for {coin_id.capitalize()}")
            
        elif choice == '3':
            # Exit
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
