"""
Database Utilities for Cryptocurrency Price Tracker
--------------------------------------------------
Provides optimized SQL queries and database functions for analyzing cryptocurrency data.

This module contains utility functions for interacting with the database,
including fetching latest prices, historical data, and calculating
rolling averages using SQL WINDOW FUNCTIONS.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "postgresql")  # postgresql or mysql
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT_STR = os.getenv("DB_PORT", "5432" if DB_TYPE == "postgresql" else "3306")
# Clean the DB_PORT to handle comments
DB_PORT = DB_PORT_STR.split('#')[0].strip().strip('"\'')
DB_NAME = os.getenv("DB_NAME", "crypto_tracker")
DB_USER = os.getenv("DB_USER", "postgres" if DB_TYPE == "postgresql" else "root")
DB_PASSWORD_STR = os.getenv("DB_PASSWORD", "")
# Clean the DB_PASSWORD to handle quotes and comments
DB_PASSWORD = DB_PASSWORD_STR.split('#')[0].strip().strip('"\'')

def create_db_engine():
    """
    Create and return a SQLAlchemy engine for database operations.
    
    Returns:
        Engine: SQLAlchemy engine connected to the specified database.
        
    Raises:
        Exception: If there's an error connecting to the database.
    """
    try:
        # Determine the connection string based on DB_TYPE
        if DB_TYPE.lower() == "sqlite":
            # SQLite connection (file-based)
            db_path = os.path.abspath(DB_NAME)
            connection_string = f"sqlite:///{db_path}"
        elif DB_TYPE.lower() == "postgresql":
            # PostgreSQL connection
            connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        elif DB_TYPE.lower() == "mysql":
            # MySQL connection
            connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            raise ValueError(f"Unsupported database type: {DB_TYPE}")
        
        # Create and return the engine
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        return None

def get_db_connection():
    """
    Create and return a SQLAlchemy engine for database operations.
    
    Returns:
        Engine: SQLAlchemy engine connected to the configured database.
        
    Raises:
        Exception: If there's an error connecting to the database.
    """
    try:
        if DB_TYPE == "postgresql":
            connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:  # mysql
            connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        return create_engine(connection_string)
    except Exception as e:
        raise Exception(f"Failed to create database connection: {e}")

def get_latest_prices():
    """
    Get the latest prices for all tracked cryptocurrencies.
    
    Uses a Common Table Expression (CTE) to find the most recent price
    entry for each cryptocurrency in the database.
    
    Returns:
        DataFrame: Pandas DataFrame containing the latest price data.
        
    Raises:
        Exception: If there's an error executing the query.
    """
    try:
        engine = get_db_connection()
        
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
                cp.*
            FROM 
                crypto_prices cp
            JOIN 
                latest_prices lp ON cp.coin_id = lp.coin_id AND cp.timestamp = lp.latest_timestamp
            ORDER BY 
                cp.market_cap DESC;
            """
        else:  # MySQL
            query = """
            SELECT cp.*
            FROM crypto_prices cp
            INNER JOIN (
                SELECT coin_id, MAX(timestamp) as latest_timestamp
                FROM crypto_prices
                GROUP BY coin_id
            ) latest ON cp.coin_id = latest.coin_id AND cp.timestamp = latest.latest_timestamp
            ORDER BY cp.market_cap DESC;
            """
        
        return pd.read_sql(query, engine)
    except Exception as e:
        raise Exception(f"Error fetching latest prices: {e}")

def get_price_history(coin_id, days=30):
    """
    Get price history for a specific coin over the specified number of days.
    
    Args:
        coin_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
        days (int, optional): Number of days of history to retrieve. Defaults to 30.
        
    Returns:
        DataFrame: Pandas DataFrame containing the price history.
        
    Raises:
        Exception: If there's an error executing the query.
    """
    try:
        engine = get_db_connection()
        
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
        
        # Adjust syntax for MySQL if needed
        if DB_TYPE == "mysql":
            query = query.replace("INTERVAL '{days} days'", f"INTERVAL {days} DAY")
        
        return pd.read_sql(query, engine)
    except Exception as e:
        raise Exception(f"Error fetching price history for {coin_id}: {e}")

def get_bitcoin_history(days=7):
    """
    Get Bitcoin price history for the specified number of days.
    
    Args:
        days (int, optional): Number of days of history to retrieve. Defaults to 7.
        
    Returns:
        DataFrame: Pandas DataFrame containing the Bitcoin price history.
        
    Raises:
        Exception: If there's an error executing the query.
    """
    return get_price_history('bitcoin', days)

def get_rolling_averages(coin_id, window_size=7):
    """
    Get rolling averages for a specific coin using SQL WINDOW FUNCTIONS.
    
    This demonstrates the use of advanced SQL features like WINDOW FUNCTIONS
    for calculating moving averages directly in the database.
    
    Args:
        coin_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
        window_size (int, optional): Size of the rolling window in days. Defaults to 7.
        
    Returns:
        DataFrame: Pandas DataFrame containing the price data with rolling averages.
        
    Raises:
        Exception: If there's an error executing the query.
    """
    try:
        engine = get_db_connection()
        
        if DB_TYPE == "postgresql":
            query = f"""
            SELECT 
                coin_id,
                timestamp,
                price_usd,
                AVG(price_usd) OVER (
                    PARTITION BY coin_id 
                    ORDER BY timestamp 
                    ROWS BETWEEN {window_size-1} PRECEDING AND CURRENT ROW
                ) as rolling_avg_price,
                price_change_percentage_24h,
                AVG(price_change_percentage_24h) OVER (
                    PARTITION BY coin_id 
                    ORDER BY timestamp 
                    ROWS BETWEEN {window_size-1} PRECEDING AND CURRENT ROW
                ) as rolling_avg_change
            FROM 
                crypto_prices
            WHERE 
                coin_id = '{coin_id}'
            ORDER BY 
                timestamp;
            """
        else:  # MySQL
            query = f"""
            SELECT 
                coin_id,
                timestamp,
                price_usd,
                AVG(price_usd) OVER (
                    PARTITION BY coin_id 
                    ORDER BY timestamp 
                    ROWS {window_size-1} PRECEDING
                ) as rolling_avg_price,
                price_change_percentage_24h,
                AVG(price_change_percentage_24h) OVER (
                    PARTITION BY coin_id 
                    ORDER BY timestamp 
                    ROWS {window_size-1} PRECEDING
                ) as rolling_avg_change
            FROM 
                crypto_prices
            WHERE 
                coin_id = '{coin_id}'
            ORDER BY 
                timestamp;
            """
        
        return pd.read_sql(query, engine)
    except Exception as e:
        raise Exception(f"Error calculating rolling averages for {coin_id}: {e}")

def detect_market_trend(coin_id, days=30):
    """
    Detect market trend (bullish/bearish) based on price movement patterns.
    Uses SQL window functions for analysis.
    
    Args:
        coin_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
        days (int, optional): Number of days to analyze. Defaults to 30.
        
    Returns:
        DataFrame: Pandas DataFrame containing trend analysis.
        
    Raises:
        Exception: If there's an error executing the query.
    """
    try:
        engine = get_db_connection()
        
        if DB_TYPE == "postgresql":
            query = f"""
            WITH daily_prices AS (
                SELECT 
                    coin_id,
                    DATE(timestamp) as date,
                    AVG(price_usd) as avg_daily_price
                FROM 
                    crypto_prices
                WHERE 
                    coin_id = '{coin_id}'
                    AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '{days} days'
                GROUP BY 
                    coin_id, DATE(timestamp)
            ),
            price_changes AS (
                SELECT 
                    coin_id,
                    date,
                    avg_daily_price,
                    LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as prev_day_price,
                    avg_daily_price - LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as daily_change,
                    AVG(avg_daily_price) OVER (
                        PARTITION BY coin_id 
                        ORDER BY date 
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                    ) as rolling_7day_avg
                FROM 
                    daily_prices
            )
            SELECT 
                coin_id,
                date,
                avg_daily_price,
                daily_change,
                CASE 
                    WHEN daily_change > 0 THEN 'up'
                    WHEN daily_change < 0 THEN 'down'
                    ELSE 'unchanged'
                END as daily_direction,
                rolling_7day_avg,
                CASE 
                    WHEN avg_daily_price > rolling_7day_avg THEN 'above_average'
                    ELSE 'below_average'
                END as avg_comparison,
                CASE 
                    WHEN COUNT(*) FILTER (WHERE daily_change > 0) OVER (
                        PARTITION BY coin_id 
                        ORDER BY date 
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                    ) >= 4 THEN 'bullish'
                    WHEN COUNT(*) FILTER (WHERE daily_change < 0) OVER (
                        PARTITION BY coin_id 
                        ORDER BY date 
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                    ) >= 4 THEN 'bearish'
                    ELSE 'neutral'
                END as market_trend
            FROM 
                price_changes
            WHERE 
                prev_day_price IS NOT NULL
            ORDER BY 
                date;
            """
        else:  # MySQL (simplified as MySQL has different window function syntax)
            query = f"""
            WITH daily_prices AS (
                SELECT 
                    coin_id,
                    DATE(timestamp) as date,
                    AVG(price_usd) as avg_daily_price
                FROM 
                    crypto_prices
                WHERE 
                    coin_id = '{coin_id}'
                    AND timestamp >= CURRENT_TIMESTAMP - INTERVAL {days} DAY
                GROUP BY 
                    coin_id, DATE(timestamp)
            ),
            price_changes AS (
                SELECT 
                    coin_id,
                    date,
                    avg_daily_price,
                    LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as prev_day_price,
                    avg_daily_price - LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as daily_change,
                    AVG(avg_daily_price) OVER (
                        PARTITION BY coin_id 
                        ORDER BY date 
                        ROWS 6 PRECEDING
                    ) as rolling_7day_avg
                FROM 
                    daily_prices
            )
            SELECT 
                coin_id,
                date,
                avg_daily_price,
                daily_change,
                CASE 
                    WHEN daily_change > 0 THEN 'up'
                    WHEN daily_change < 0 THEN 'down'
                    ELSE 'unchanged'
                END as daily_direction,
                rolling_7day_avg,
                CASE 
                    WHEN avg_daily_price > rolling_7day_avg THEN 'above_average'
                    ELSE 'below_average'
                END as avg_comparison
            FROM 
                price_changes
            WHERE 
                prev_day_price IS NOT NULL
            ORDER BY 
                date;
            """
        
        return pd.read_sql(query, engine)
    except Exception as e:
        raise Exception(f"Error detecting market trend for {coin_id}: {e}")

def export_data_for_visualization(output_file="crypto_data_export.csv"):
    """
    Export data in a format suitable for Power BI or Tableau.
    
    Args:
        output_file (str, optional): Path to the output CSV file. 
                                     Defaults to "crypto_data_export.csv".
        
    Returns:
        str: Message indicating the export status.
        
    Raises:
        Exception: If there's an error exporting the data.
    """
    try:
        engine = get_db_connection()
        
        query = """
        SELECT 
            cp.coin_id,
            cp.coin_name,
            cp.price_usd,
            cp.market_cap,
            cp.volume_24h,
            cp.price_change_24h,
            cp.price_change_percentage_24h,
            cp.timestamp
        FROM 
            crypto_prices cp
        ORDER BY 
            cp.timestamp, cp.market_cap DESC;
        """
        
        df = pd.read_sql(query, engine)
        df.to_csv(output_file, index=False)
        return f"Data exported to {output_file}"
    except Exception as e:
        raise Exception(f"Error exporting data for visualization: {e}")

if __name__ == "__main__":
    try:
        # Example usage
        latest_prices = get_latest_prices()
        print(f"Latest prices for {len(latest_prices)} cryptocurrencies:")
        print(latest_prices[["coin_id", "coin_name", "price_usd", "price_change_percentage_24h"]])
        
        # Export data for visualization
        export_result = export_data_for_visualization()
        print(export_result)
    except Exception as e:
        print(f"Error in example usage: {e}")
