"""
Script to create the crypto_tracker database
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the crypto_tracker database if it doesn't exist"""
    # Connect to the default 'postgres' database to create our new database
    try:
        # Connect to PostgreSQL server
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            port="5434",
            user="postgres",
            password="admin123",
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
