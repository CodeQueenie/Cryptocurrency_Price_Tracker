"""
Database Setup Script for Cryptocurrency Price Tracker

This script creates the necessary database and tables for the Cryptocurrency Price Tracker.
It will:
1. Connect to PostgreSQL
2. Create the crypto_tracker database if it doesn't exist
3. Create the required tables
"""

import sys
import time
import os
from sqlalchemy import create_engine, text, exc
from dotenv import load_dotenv

def setup_database():
    """Set up the database for the Cryptocurrency Price Tracker."""
    print("Setting up database for Cryptocurrency Price Tracker...")
    
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        load_dotenv()
    
    # PostgreSQL connection details from environment variables or defaults
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "your_password")  # Generic default
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")  # Standard PostgreSQL port
    
    # First, connect to the default 'postgres' database to create our database
    try:
        print("Connecting to PostgreSQL...")
        postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
        engine = create_engine(postgres_url)
        
        # Check if crypto_tracker database exists
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='crypto_tracker'"))
            exists = result.scalar() == 1
            
            if not exists:
                print("Creating crypto_tracker database...")
                # Close all connections to postgres database before creating a new database
                conn.execute(text("COMMIT"))
                conn.execute(text("CREATE DATABASE crypto_tracker"))
                print("Database 'crypto_tracker' created successfully!")
            else:
                print("Database 'crypto_tracker' already exists.")
    
    except exc.SQLAlchemyError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False
    
    # Now connect to the crypto_tracker database to create tables
    try:
        print("\nConnecting to crypto_tracker database...")
        crypto_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/crypto_tracker"
        crypto_engine = create_engine(crypto_url)
        
        # Create tables
        with crypto_engine.connect() as conn:
            print("Creating tables...")
            
            # Create crypto_prices table
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id SERIAL PRIMARY KEY,
                coin_id VARCHAR(50) NOT NULL,
                name VARCHAR(100) NOT NULL,
                symbol VARCHAR(20) NOT NULL,
                current_price NUMERIC(24, 8) NOT NULL,
                market_cap NUMERIC(24, 2),
                market_cap_rank INTEGER,
                total_volume NUMERIC(24, 2),
                price_change_percentage_24h NUMERIC(10, 2),
                price_change_percentage_7d NUMERIC(10, 2),
                price_change_percentage_30d NUMERIC(10, 2),
                last_updated TIMESTAMP,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """))
            
            # Create index on coin_id and timestamp for faster queries
            conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_crypto_prices_coin_id ON crypto_prices(coin_id)
            """))
            
            conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_crypto_prices_timestamp ON crypto_prices(timestamp)
            """))
            
            # Create a combined index for efficient retrieval of latest prices
            conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_crypto_prices_coin_timestamp ON crypto_prices(coin_id, timestamp)
            """))
            
            conn.execute(text("COMMIT"))
            print("Tables created successfully!")
        
        # Test the connection and tables
        with crypto_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM crypto_prices"))
            count = result.scalar()
            print(f"\nDatabase setup complete! Current record count: {count}")
        
        return True
        
    except exc.SQLAlchemyError as e:
        print(f"Error setting up crypto_tracker database: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    
    if success:
        print("\n" + "=" * 50)
        print("DATABASE SETUP SUCCESSFUL!")
        print("=" * 50)
        print("You can now run the Cryptocurrency Price Tracker.")
        print("To start tracking prices, run: python -m core.crypto_tracker")
        print("To view the Bitcoin dashboard, run: python -m bitcoin_tracker.bitcoin_dashboard_standalone")
    else:
        print("\n" + "=" * 50)
        print("DATABASE SETUP FAILED!")
        print("=" * 50)
        print("Please check the error messages above and try again.")
        sys.exit(1)
