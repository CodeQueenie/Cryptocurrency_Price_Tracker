"""
Test Database Connection
-----------------------
A simple script to test the database connection and verify that the environment is set up correctly.
"""

import os
import sys
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def test_db_connection():
    """
    Test the database connection using the credentials in the .env file.
    
    This function attempts to connect to the database using the credentials
    specified in the .env file. It also checks if the crypto_prices table
    exists and contains data.
    
    Returns:
        bool: True if the connection was successful, False otherwise.
    """
    try:
        print("Testing database connection...")
        
        # Check if .env file exists
        if not os.path.exists(".env"):
            print("❌ .env file not found!")
            print("   Please copy .env.example to .env and edit it with your database credentials.")
            return False
        
        # Load environment variables
        load_dotenv()
        
        # Get database configuration
        db_type = os.getenv("DB_TYPE", "postgresql")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432" if db_type == "postgresql" else "3306")
        db_name = os.getenv("DB_NAME", "crypto_tracker")
        db_user = os.getenv("DB_USER", "postgres" if db_type == "postgresql" else "root")
        db_password = os.getenv("DB_PASSWORD", "")
        
        # Create connection string
        if db_type == "postgresql":
            connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:  # mysql
            connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Mask password in displayed connection string
        display_conn_string = connection_string.replace(db_password, "*****" if db_password else "")
        print(f"Connection string: {display_conn_string}")
        
        # Create engine
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            # Try a simple query
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            
            print("✅ Successfully connected to the database!")
            
            # Check if crypto_prices table exists
            try:
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'crypto_prices')"
                    if db_type == "postgresql" else
                    f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{db_name}' AND table_name = 'crypto_prices'"
                ))
                table_exists = result.scalar()
                
                if table_exists:
                    print("✅ 'crypto_prices' table exists")
                    
                    # Check if table has data
                    result = conn.execute(text("SELECT COUNT(*) FROM crypto_prices"))
                    count = result.scalar()
                    
                    if count > 0:
                        print(f"✅ 'crypto_prices' table contains {count} records")
                    else:
                        print("ℹ️ 'crypto_prices' table exists but contains no data yet")
                else:
                    print("ℹ️ 'crypto_prices' table does not exist yet (it will be created when you run the tracker)")
            except Exception as e:
                print(f"ℹ️ Could not check table status: {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        
        # Provide helpful troubleshooting tips
        if "Connection refused" in str(e):
            print("\nTroubleshooting tips:")
            print("1. Make sure your database server is running")
            print("2. Check that the host and port are correct")
            print("3. Verify that your firewall allows connections to the database port")
        elif "password authentication failed" in str(e):
            print("\nTroubleshooting tips:")
            print("1. Check that your username and password are correct")
            print("2. Verify that the user has permission to access the database")
        elif "database" in str(e) and "does not exist" in str(e):
            print("\nTroubleshooting tips:")
            print(f"1. Create the '{db_name}' database manually:")
            if db_type == "postgresql":
                print(f"   CREATE DATABASE {db_name};")
            else:  # mysql
                print(f"   CREATE DATABASE {db_name};")
        
        return False

def main():
    """
    Main function to test database connection.
    
    This function runs the database connection test and provides
    feedback to the user about the results.
    
    Returns:
        None
    """
    try:
        print("=" * 50)
        print("Cryptocurrency Price Tracker - Database Test")
        print("=" * 50)
        
        # Test database connection
        success = test_db_connection()
        
        if success:
            print("\n🎉 Your database connection is working correctly!")
            print("You can now run the Cryptocurrency Price Tracker.")
        else:
            print("\n❌ Database connection test failed.")
            print("Please fix the issues and try again.")
        
        # Keep console open on Windows
        if sys.platform == "win32":
            print("\nPress Enter to exit...")
            input()
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
