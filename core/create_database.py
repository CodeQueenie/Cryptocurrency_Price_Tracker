"""
Script to create the crypto_tracker database
"""
import psycopg2
import os
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

def create_database():
    """Create the crypto_tracker database if it doesn't exist"""
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        load_dotenv()
    
    # Get database configuration from environment variables or use defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")  # Standard PostgreSQL port
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "your_password")  # Generic default
    
    # Connect to the default 'postgres' database to create our new database
    try:
        # Connect to PostgreSQL server
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database="postgres"  # Connect to the default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'crypto_tracker'")
        exists = cur.fetchone()
        
        if not exists:
            print("Creating 'crypto_tracker' database...")
            # Create the database
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('crypto_tracker')
            ))
            print("✅ Database 'crypto_tracker' created successfully!")
        else:
            print("✅ Database 'crypto_tracker' already exists.")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Cryptocurrency Price Tracker - Database Setup")
    print("=" * 50)
    
    success = create_database()
    
    if success:
        print("\nDatabase setup completed successfully.")
        print("You can now run the test_db_connection.py script to verify the connection.")
    else:
        print("\nDatabase setup failed.")
        print("Please check the error message above and try again.")
    
    print("\nPress Enter to exit...")
    input()
