"""
Improved Database Query Tool for Cryptocurrency Price Tracker

This script provides an interactive way to query the cryptocurrency database,
using direct string formatting for PostgreSQL compatibility.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os
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
    
    print(f"Connecting to {db_type} database at {db_host}:{db_port}...")
    
    # Create connection string
    conn_str = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(conn_str)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Successfully connected to {db_type} database!")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(query, engine):
    """Execute a SQL query and return the results as a DataFrame."""
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def display_results(df):
    """Display query results in a formatted table."""
    if df.empty:
        print("No results found.")
        return
    
    print(f"Found {len(df)} results:")
    
    # Format the output using tabulate
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

def get_table_schema(table_name, engine):
    """Get the schema for a specific table."""
    query = f"""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position;
    """
    return execute_query(query, engine)

def list_tables(engine):
    """List all tables in the database."""
    query = """
    SELECT table_name 
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """
    return execute_query(query, engine)

def describe_table_contents(table_name, engine):
    """Show the first few rows of a table to understand its structure."""
    query = f"""
    SELECT * FROM {table_name} LIMIT 5;
    """
    return execute_query(query, engine)

def print_menu():
    """Print the main menu options."""
    print("\n" + "=" * 50)
    print("CRYPTOCURRENCY DATABASE QUERY TOOL")
    print("=" * 50)
    print("1. List all tables")
    print("2. View table schema")
    print("3. View sample data from a table")
    print("4. View all cryptocurrency data")
    print("5. View data for a specific cryptocurrency")
    print("6. Run a custom SQL query")
    print("7. Exit")
    print("=" * 50)

def main():
    """Main function to run the interactive query tool."""
    print("Welcome to the Improved Cryptocurrency Database Query Tool")
    
    # Connect to database
    engine = connect_to_database()
    if not engine:
        return
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            # List all tables
            tables = list_tables(engine)
            print("\nTables in database:")
            for index, row in tables.iterrows():
                print(f"- {row['table_name']}")
                
        elif choice == '2':
            # View table schema
            table_name = input("Enter table name: ").strip()
            if not table_name:
                print("Table name cannot be empty.")
                continue
                
            schema = get_table_schema(table_name, engine)
            if not schema.empty:
                print(f"\nSchema for table '{table_name}':")
                display_results(schema)
            
        elif choice == '3':
            # View sample data
            table_name = input("Enter table name: ").strip()
            if not table_name:
                print("Table name cannot be empty.")
                continue
                
            sample = describe_table_contents(table_name, engine)
            if not sample.empty:
                print(f"\nSample data from table '{table_name}':")
                display_results(sample)
            
        elif choice == '4':
            # View all cryptocurrency data
            query = """
            SELECT * FROM crypto_prices
            ORDER BY timestamp DESC
            LIMIT 20;
            """
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '5':
            # View data for a specific cryptocurrency
            coin = input("Enter cryptocurrency ID (e.g., bitcoin): ").strip().lower()
            if not coin:
                print("Cryptocurrency ID cannot be empty.")
                continue
                
            limit = input("Enter number of records to show (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            
            query = f"""
            SELECT * FROM crypto_prices
            WHERE coin_id = '{coin}'
            ORDER BY timestamp DESC
            LIMIT {limit};
            """
            results = execute_query(query, engine)
            display_results(results)
            
        elif choice == '6':
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
                display_results(results)
            
        elif choice == '7':
            # Exit
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
