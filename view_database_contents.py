#!/usr/bin/env python3
"""
View Database Contents
----------------------
A simple utility to view the contents of the cryptocurrency database.
This script displays the most recent cryptocurrency prices stored in the database.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tabulate import tabulate
import re

# Load environment variables
load_dotenv()

# Helper function to clean environment variables
def clean_env_value(value):
    if value is None:
        return None
    # Remove quotes and trailing comments
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    # Remove any trailing comments
    value = re.sub(r'\s+#.*$', '', value)
    return value.strip()

# Database configuration
DB_TYPE = clean_env_value(os.getenv("DB_TYPE", "postgresql"))  # postgresql or mysql
DB_HOST = clean_env_value(os.getenv("DB_HOST", "localhost"))
DB_PORT_STR = clean_env_value(os.getenv("DB_PORT", "5432" if DB_TYPE == "postgresql" else "3306"))
# Extract just the numeric part for the port
DB_PORT = int(re.sub(r'[^0-9]', '', DB_PORT_STR))
DB_NAME = clean_env_value(os.getenv("DB_NAME", "crypto_tracker"))
DB_USER = clean_env_value(os.getenv("DB_USER", "postgres" if DB_TYPE == "postgresql" else "root"))
DB_PASSWORD = clean_env_value(os.getenv("DB_PASSWORD", ""))

# Remove any quotes from the password
if DB_PASSWORD.startswith('"') and DB_PASSWORD.endswith('"'):
    DB_PASSWORD = DB_PASSWORD[1:-1]
if DB_PASSWORD.startswith("'") and DB_PASSWORD.endswith("'"):
    DB_PASSWORD = DB_PASSWORD[1:-1]

def create_db_engine():
    """Create and return a SQLAlchemy engine for database operations."""
    if DB_TYPE == "postgresql":
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:  # mysql
        connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Print connection string with password masked
    masked_connection = connection_string.replace(DB_PASSWORD, "********") if DB_PASSWORD else connection_string
    print(f"DEBUG: Connection string: {masked_connection}")
    
    return create_engine(connection_string)

def get_latest_prices():
    """Get the latest prices for all cryptocurrencies in the database."""
    engine = create_db_engine()
    
    if DB_TYPE == "postgresql":
        query = """
        WITH latest_prices AS (
            SELECT 
                coin_id,
                MAX(timestamp) as latest_timestamp
            FROM 
                crypto_prices
            GROUP BY 
                coin_id
        )
        SELECT 
            cp.coin_id,
            cp.coin_name,
            cp.price_usd,
            cp.market_cap,
            cp.price_change_percentage_24h,
            cp.timestamp
        FROM 
            crypto_prices cp
        JOIN 
            latest_prices lp ON cp.coin_id = lp.coin_id AND cp.timestamp = lp.latest_timestamp
        ORDER BY 
            cp.market_cap DESC;
        """
    else:  # MySQL
        query = """
        SELECT cp.coin_id, cp.coin_name, cp.price_usd, cp.market_cap, 
               cp.price_change_percentage_24h, cp.timestamp
        FROM crypto_prices cp
        INNER JOIN (
            SELECT coin_id, MAX(timestamp) as latest_timestamp
            FROM crypto_prices
            GROUP BY coin_id
        ) latest ON cp.coin_id = latest.coin_id AND cp.timestamp = latest.latest_timestamp
        ORDER BY cp.market_cap DESC;
        """
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

def get_price_history(coin_id, days=7):
    """Get price history for a specific coin for the last N days."""
    engine = create_db_engine()
    
    if DB_TYPE == "postgresql":
        query = f"""
        SELECT 
            coin_id,
            coin_name,
            price_usd,
            timestamp,
            price_change_percentage_24h
        FROM 
            crypto_prices
        WHERE 
            coin_id = '{coin_id}'
            AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '{days} days'
        ORDER BY 
            timestamp;
        """
    else:  # MySQL
        query = f"""
        SELECT 
            coin_id,
            coin_name,
            price_usd,
            timestamp,
            price_change_percentage_24h
        FROM 
            crypto_prices
        WHERE 
            coin_id = '{coin_id}'
            AND timestamp >= CURRENT_TIMESTAMP - INTERVAL {days} DAY
        ORDER BY 
            timestamp;
        """
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

def display_table(df, title):
    """Display a DataFrame as a formatted table."""
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80)
    
    if df.empty:
        print("No data available.")
        return
    
    # Format numeric columns
    if 'price_usd' in df.columns:
        df['price_usd'] = df['price_usd'].apply(lambda x: f"${x:,.2f}")
    
    if 'market_cap' in df.columns:
        df['market_cap'] = df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A")
    
    if 'price_change_percentage_24h' in df.columns:
        df['price_change_percentage_24h'] = df['price_change_percentage_24h'].apply(
            lambda x: f"{x:+.2f}%" if pd.notnull(x) else "N/A"
        )
    
    # Format timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    print("\n")

def main():
    """Main function to display database contents."""
    try:
        # Install tabulate if not already installed
        try:
            import tabulate
        except ImportError:
            import subprocess
            print("Installing required package: tabulate...")
            subprocess.check_call(["pip", "install", "tabulate"])
            from tabulate import tabulate
        
        print("\n" + "=" * 80)
        print("Cryptocurrency Price Tracker - Database Viewer")
        print("=" * 80)
        
        # Get and display latest prices
        latest_prices = get_latest_prices()
        display_table(latest_prices, "Latest Cryptocurrency Prices")
        
        # Ask if user wants to see price history for a specific coin
        if not latest_prices.empty:
            print("Available coins:")
            for i, (coin_id, coin_name) in enumerate(zip(latest_prices['coin_id'], latest_prices['coin_name']), 1):
                print(f"{i}. {coin_name} ({coin_id})")
            
            choice = input("\nEnter coin number to view price history (or press Enter to exit): ")
            if choice.strip() and choice.isdigit() and 1 <= int(choice) <= len(latest_prices):
                idx = int(choice) - 1
                coin_id = latest_prices.iloc[idx]['coin_id']
                coin_name = latest_prices.iloc[idx]['coin_name']
                
                days = input(f"Enter number of days of history to view for {coin_name} (default: 7): ")
                days = int(days) if days.strip() and days.isdigit() else 7
                
                history = get_price_history(coin_id, days)
                display_table(history, f"Price History for {coin_name} (Last {days} days)")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
