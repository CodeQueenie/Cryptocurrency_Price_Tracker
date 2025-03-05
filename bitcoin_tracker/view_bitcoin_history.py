#!/usr/bin/env python3
"""
Bitcoin Price History Viewer
---------------------------
A simple tool to view Bitcoin's price history.
This script automatically displays Bitcoin's price history without requiring user input.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tabulate import tabulate
from datetime import datetime, timedelta
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
    
    return create_engine(connection_string)

def get_latest_bitcoin_price():
    """Get the latest Bitcoin price from the database."""
    engine = create_db_engine()
    
    if DB_TYPE == "postgresql":
        query = """
        WITH latest_prices AS (
            SELECT 
                coin_id,
                MAX(timestamp) as latest_timestamp
            FROM 
                crypto_prices
            WHERE
                coin_id = 'bitcoin'
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
            latest_prices lp ON cp.coin_id = lp.coin_id AND cp.timestamp = lp.latest_timestamp;
        """
    else:  # MySQL
        query = """
        SELECT cp.coin_id, cp.coin_name, cp.price_usd, cp.market_cap, 
               cp.price_change_percentage_24h, cp.timestamp
        FROM crypto_prices cp
        INNER JOIN (
            SELECT coin_id, MAX(timestamp) as latest_timestamp
            FROM crypto_prices
            WHERE coin_id = 'bitcoin'
            GROUP BY coin_id
        ) latest ON cp.coin_id = latest.coin_id AND cp.timestamp = latest.latest_timestamp;
        """
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

def get_bitcoin_price_history(days=7):
    """Get Bitcoin price history for the last N days."""
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
            coin_id = 'bitcoin'
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
            coin_id = 'bitcoin'
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
    """Main function to display Bitcoin price history."""
    try:
        print("\n" + "=" * 80)
        print("Bitcoin Price Tracker")
        print("=" * 80)
        
        # Get and display latest Bitcoin price
        latest_price = get_latest_bitcoin_price()
        display_table(latest_price, "Current Bitcoin Price")
        
        # Get and display Bitcoin price history for the last 7 days
        print("\nShowing Bitcoin price history for the last 7 days:")
        history = get_bitcoin_price_history(days=7)
        
        if history.empty:
            print("No historical data available for Bitcoin.")
        else:
            display_table(history, "Bitcoin Price History (Last 7 Days)")
            
            # Calculate price change
            if len(history) >= 2:
                first_price = history.iloc[0]['price_usd'].replace('$', '').replace(',', '')
                last_price = history.iloc[-1]['price_usd'].replace('$', '').replace(',', '')
                try:
                    first_price = float(first_price)
                    last_price = float(last_price)
                    change = last_price - first_price
                    change_pct = (change / first_price) * 100
                    
                    print(f"Price Change Summary:")
                    print(f"Starting Price: ${first_price:,.2f}")
                    print(f"Current Price: ${last_price:,.2f}")
                    print(f"Change: ${change:,.2f} ({change_pct:+.2f}%)")
                    
                    if change > 0:
                        print("\n🚀 Bitcoin price has increased over the last 7 days! 🚀")
                    elif change < 0:
                        print("\n📉 Bitcoin price has decreased over the last 7 days. 📉")
                    else:
                        print("\nBitcoin price has remained stable over the last 7 days.")
                except:
                    pass
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
