#!/usr/bin/env python3
"""
Cryptocurrency Price Tracker
----------------------------
Fetches real-time cryptocurrency prices using the CoinGecko API
and stores them in a database.

This module handles the core functionality of fetching cryptocurrency data
from the CoinGecko API and storing it in a PostgreSQL or MySQL database.
It includes scheduling capabilities for automated data collection.
"""

import os
import time
import logging
import schedule
import pandas as pd
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crypto_tracker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "postgresql")  # postgresql or mysql
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432" if DB_TYPE == "postgresql" else "3306")
DB_NAME = os.getenv("DB_NAME", "crypto_tracker")
DB_USER = os.getenv("DB_USER", "postgres" if DB_TYPE == "postgresql" else "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# CoinGecko API configuration
COINS_TO_TRACK = os.getenv("COINS_TO_TRACK", "bitcoin,ethereum,cardano,solana,ripple,polkadot,dogecoin").split(",")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "3600"))  # Default: 1 hour

class CryptoTracker:
    """
    Main class for the Cryptocurrency Price Tracker application.
    
    This class handles the connection to the CoinGecko API and the database,
    fetches cryptocurrency data, and stores it in the database.
    
    Attributes:
        cg (CoinGeckoAPI): Instance of the CoinGecko API client.
        engine (Engine): SQLAlchemy engine for database operations.
    """
    
    def __init__(self):
        """
        Initialize the CryptoTracker with API and database connections.
        
        Sets up the CoinGecko API client and database connection,
        and creates necessary database tables if they don't exist.
        
        Raises:
            Exception: If there's an error connecting to the database or setting up tables.
        """
        try:
            self.cg = CoinGeckoAPI()
            self.engine = self._create_db_engine()
            self._setup_database()
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def _create_db_engine(self):
        """
        Create and return a SQLAlchemy engine for database operations.
        
        Returns:
            Engine: SQLAlchemy engine connected to the specified database.
            
        Raises:
            Exception: If there's an error connecting to the database.
        """
        try:
            if DB_TYPE == "postgresql":
                connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            else:  # mysql
                connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            
            engine = create_engine(connection_string)
            logger.info(f"Successfully connected to {DB_TYPE} database")
            return engine
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def _setup_database(self):
        """
        Create necessary database tables if they don't exist.
        
        Creates the crypto_prices table and necessary indexes
        for efficient querying.
        
        Raises:
            Exception: If there's an error creating the tables or indexes.
        """
        try:
            with self.engine.connect() as conn:
                if DB_TYPE == "postgresql":
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS crypto_prices (
                            id SERIAL PRIMARY KEY,
                            coin_id VARCHAR(50) NOT NULL,
                            coin_name VARCHAR(100) NOT NULL,
                            price_usd NUMERIC(24, 12) NOT NULL,
                            market_cap NUMERIC(24, 2),
                            volume_24h NUMERIC(24, 2),
                            price_change_24h NUMERIC(12, 6),
                            price_change_percentage_24h NUMERIC(12, 6),
                            last_updated TIMESTAMP NOT NULL,
                            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                        
                        CREATE INDEX IF NOT EXISTS idx_coin_timestamp ON crypto_prices(coin_id, timestamp);
                    """))
                else:  # mysql
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS crypto_prices (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            coin_id VARCHAR(50) NOT NULL,
                            coin_name VARCHAR(100) NOT NULL,
                            price_usd DECIMAL(24, 12) NOT NULL,
                            market_cap DECIMAL(24, 2),
                            volume_24h DECIMAL(24, 2),
                            price_change_24h DECIMAL(12, 6),
                            price_change_percentage_24h DECIMAL(12, 6),
                            last_updated TIMESTAMP NOT NULL,
                            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                    """))
                    
                    # MySQL requires separate statements for indexes
                    try:
                        conn.execute(text("""
                            CREATE INDEX idx_coin_timestamp ON crypto_prices(coin_id, timestamp);
                        """))
                    except Exception as e:
                        # Index might already exist
                        logger.warning(f"Index creation warning (may already exist): {e}")
                
                conn.commit()
                logger.info("Database tables created/verified successfully")
        except Exception as e:
            logger.error(f"Database setup error: {e}")
            raise
    
    def fetch_crypto_data(self):
        """
        Fetch cryptocurrency data from CoinGecko API.
        
        Retrieves current market data for the specified cryptocurrencies
        and stores it in the database.
        
        Raises:
            Exception: If there's an error fetching or processing the data.
        """
        try:
            logger.info(f"Fetching data for: {', '.join(COINS_TO_TRACK)}")
            
            # Get market data for the specified coins
            market_data = self.cg.get_coins_markets(
                vs_currency="usd",
                ids=COINS_TO_TRACK,
                order="market_cap_desc",
                per_page=100,
                page=1,
                sparkline=False,
                price_change_percentage="24h"
            )
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(market_data)
            
            if df.empty:
                logger.warning("No data received from CoinGecko API")
                return
            
            # Prepare data for database insertion
            records = []
            for _, row in df.iterrows():
                try:
                    last_updated = datetime.strptime(row["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    record = {
                        "coin_id": row["id"],
                        "coin_name": row["name"],
                        "price_usd": row["current_price"],
                        "market_cap": row["market_cap"],
                        "volume_24h": row["total_volume"],
                        "price_change_24h": row["price_change_24h"],
                        "price_change_percentage_24h": row["price_change_percentage_24h"],
                        "last_updated": last_updated,
                        "timestamp": datetime.now()
                    }
                    records.append(record)
                except Exception as e:
                    logger.error(f"Error processing row for {row.get('id', 'unknown')}: {e}")
                    continue
            
            if records:
                # Insert data into database
                self._store_crypto_data(records)
                logger.info(f"Successfully fetched and stored data for {len(records)} cryptocurrencies")
            else:
                logger.warning("No valid records to store after processing")
            
        except Exception as e:
            logger.error(f"Error fetching crypto data: {e}")
    
    def _store_crypto_data(self, records):
        """
        Store cryptocurrency data in the database.
        
        Args:
            records (list): List of dictionaries containing cryptocurrency data.
            
        Raises:
            Exception: If there's an error storing the data.
        """
        try:
            df = pd.DataFrame(records)
            df.to_sql("crypto_prices", self.engine, if_exists="append", index=False)
        except Exception as e:
            logger.error(f"Error storing data in database: {e}")
            raise
    
    def run_scheduled(self):
        """
        Run the tracker with a schedule.
        
        Fetches data immediately and then schedules regular updates
        based on the UPDATE_INTERVAL setting.
        
        Raises:
            Exception: If there's an error in the scheduling process.
        """
        try:
            logger.info(f"Starting Cryptocurrency Price Tracker with {UPDATE_INTERVAL} seconds interval")
            
            # Fetch data immediately on startup
            self.fetch_crypto_data()
            
            # Schedule regular updates
            schedule.every(UPDATE_INTERVAL).seconds.do(self.fetch_crypto_data)
            
            # Keep the script running and execute scheduled tasks
            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            logger.error(f"Scheduling error: {e}")
            raise

def main():
    """
    Main entry point for the application.
    
    Creates a CryptoTracker instance and runs it with scheduling.
    
    Handles keyboard interrupts and other exceptions gracefully.
    """
    try:
        tracker = CryptoTracker()
        tracker.run_scheduled()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
