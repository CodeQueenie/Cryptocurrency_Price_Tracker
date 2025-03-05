"""
Database Query Tool for Cryptocurrency Price Tracker

This script provides an interactive way to query the cryptocurrency database.
It offers several preset queries and allows for custom SQL queries.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
from tabulate import tabulate

def get_connection_details():
    """Prompt the user for database connection details."""
    print("\n" + "=" * 50)
    print("DATABASE CONNECTION SETUP")
    print("=" * 50)
    
    # Default values from the error message
    defaults = {
        "DB_TYPE": "postgresql",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "crypto_tracker",
        "DB_USER": "postgres",
        "DB_PASSWORD": ""
    }
    
    print("Enter database connection details (press Enter to use default):")
    db_type = input(f"Database type (postgresql/mysql) [{defaults['DB_TYPE']}]: ").strip() or defaults['DB_TYPE']
    db_host = input(f"Database host [{defaults['DB_HOST']}]: ").strip() or defaults['DB_HOST']
    db_port = input(f"Database port [{defaults['DB_PORT']}]: ").strip() or defaults['DB_PORT']
    db_name = input(f"Database name [{defaults['DB_NAME']}]: ").strip() or defaults['DB_NAME']
    db_user = input(f"Database user [{defaults['DB_USER']}]: ").strip() or defaults['DB_USER']
    db_password = input(f"Database password []: ").strip() or defaults['DB_PASSWORD']
    
    return {
        "DB_TYPE": db_type,
        "DB_HOST": db_host,
        "DB_PORT": db_port,
        "DB_NAME": db_name,
        "DB_USER": db_user,
        "DB_PASSWORD": db_password
    }

def get_engine(connection_details):
    """Create and return a database engine."""
    try:
        db_type = connection_details["DB_TYPE"]
        db_host = connection_details["DB_HOST"]
        db_port = connection_details["DB_PORT"]
        db_name = connection_details["DB_NAME"]
        db_user = connection_details["DB_USER"]
        db_password = connection_details["DB_PASSWORD"]
        
        # Create connection string
        if db_type == "postgresql":
            conn_str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            conn_str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        engine = create_engine(conn_str)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(query, engine, params=None):
    """Execute a SQL query and return the results as a DataFrame."""
    try:
        return pd.read_sql(query, engine, params=params)
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def display_results(df, limit=None):
    """Display query results in a formatted table."""
    if df.empty:
        print("No results found.")
        return
    
    # Limit the number of rows if specified
    if limit and len(df) > limit:
        print(f"Displaying first {limit} of {len(df)} results:")
        df = df.head(limit)
    else:
        print(f"Found {len(df)} results:")
    
    # Format the output using tabulate
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

def get_table_schema(table_name, engine, db_type, db_name):
    """Get the schema for a specific table."""
    if db_type == "postgresql":
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position;
        """
    else:  # MySQL
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = :table_name AND table_schema = :db_name
        ORDER BY ordinal_position;
        """
        
    params = {"table_name": table_name}
    if db_type != "postgresql":
        params["db_name"] = db_name
        
    return execute_query(query, engine, params)

def list_tables(engine, db_type, db_name):
    """List all tables in the database."""
    if db_type == "postgresql":
        query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    else:  # MySQL
        query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = :db_name
        ORDER BY table_name;
        """
        
    params = {}
    if db_type != "postgresql":
        params["db_name"] = db_name
        
    return execute_query(query, engine, params)

def print_menu():
    """Print the main menu options."""
    print("\n" + "=" * 50)
    print("CRYPTOCURRENCY DATABASE QUERY TOOL")
    print("=" * 50)
    print("1. List all tables")
    print("2. View table schema")
    print("3. Latest cryptocurrency prices")
    print("4. Price history for a specific cryptocurrency")
    print("5. Price comparison (all cryptocurrencies)")
    print("6. Market cap ranking")
    print("7. 24-hour price change percentage")
    print("8. Custom SQL query")
    print("9. Exit")
    print("=" * 50)

def main():
    """Main function to run the interactive query tool."""
    print("Welcome to the Cryptocurrency Database Query Tool")
    
    # Get connection details
    connection_details = get_connection_details()
    
    print("Connecting to database...")
    engine = get_engine(connection_details)
    
    if not engine:
        print("Failed to connect to the database. Please check your connection details.")
        return
    
    print(f"Successfully connected to {connection_details['DB_TYPE']} database at {connection_details['DB_HOST']}:{connection_details['DB_PORT']}")
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == '1':
            # List all tables
            tables = list_tables(engine, connection_details["DB_TYPE"], connection_details["DB_NAME"])
            print("\nTables in database:")
            for index, row in tables.iterrows():
                print(f"- {row['table_name']}")
                
        elif choice == '2':
            # View table schema
            table_name = input("Enter table name: ").strip()
            schema = get_table_schema(table_name, engine, connection_details["DB_TYPE"], connection_details["DB_NAME"])
            if not schema.empty:
                print(f"\nSchema for table '{table_name}':")
                display_results(schema)
            
        elif choice == '3':
            # Latest cryptocurrency prices
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
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '4':
            # Price history for a specific cryptocurrency
            coin = input("Enter cryptocurrency ID (e.g., bitcoin): ").strip().lower()
            limit = input("Enter number of records to show (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            
            query = """
            SELECT coin_id, name, symbol, current_price, 
                   price_change_percentage_24h, 
                   timestamp, last_updated
            FROM crypto_prices
            WHERE coin_id = :coin_id
            ORDER BY timestamp DESC
            LIMIT :limit;
            """
            results = execute_query(query, engine, {"coin_id": coin, "limit": limit})
            display_results(results)
            
        elif choice == '5':
            # Price comparison
            query = """
            SELECT coin_id, name, symbol, current_price, 
                   price_change_percentage_24h, market_cap
            FROM crypto_prices
            WHERE (coin_id, timestamp) IN (
                SELECT coin_id, MAX(timestamp) 
                FROM crypto_prices 
                GROUP BY coin_id
            )
            ORDER BY current_price DESC;
            """
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '6':
            # Market cap ranking
            query = """
            SELECT coin_id, name, symbol, market_cap, current_price
            FROM crypto_prices
            WHERE (coin_id, timestamp) IN (
                SELECT coin_id, MAX(timestamp) 
                FROM crypto_prices 
                GROUP BY coin_id
            )
            ORDER BY market_cap DESC;
            """
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '7':
            # 24-hour price change percentage
            query = """
            SELECT coin_id, name, symbol, price_change_percentage_24h, 
                   current_price, market_cap
            FROM crypto_prices
            WHERE (coin_id, timestamp) IN (
                SELECT coin_id, MAX(timestamp) 
                FROM crypto_prices 
                GROUP BY coin_id
            )
            ORDER BY price_change_percentage_24h DESC;
            """
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '8':
            # Custom SQL query
            print("\nEnter your SQL query (press Enter twice to execute):")
            lines = []
            while True:
                line = input()
                if not line and lines:
                    break
                lines.append(line)
            
            if lines:
                query = "\n".join(lines)
                results = execute_query(query, engine)
                display_results(results, limit=20)  # Limit to 20 rows for custom queries
            
        elif choice == '9':
            # Exit
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
