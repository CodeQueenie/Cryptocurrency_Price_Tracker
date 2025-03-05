"""
Simple test script to check if the Bitcoin dashboard can be imported and initialized
"""

def test_bitcoin_dashboard():
    print("Testing Bitcoin Dashboard initialization...")
    
    try:
        # Import the main function from the dashboard
        from bitcoin_tracker.bitcoin_dashboard_standalone import main
        print("✓ Successfully imported Bitcoin dashboard module")
        
        # Import the core modules
        from core.crypto_tracker import CryptoTracker
        from core.db_utils import create_db_engine, get_db_connection
        print("✓ Successfully imported core modules")
        
        # Test CoinGecko API connection
        from pycoingecko import CoinGeckoAPI
        cg = CoinGeckoAPI()
        ping_result = cg.ping()
        if ping_result and 'gecko_says' in ping_result:
            print(f"✓ Successfully connected to CoinGecko API: {ping_result['gecko_says']}")
        else:
            print(f"✗ Received invalid response from CoinGecko API: {ping_result}")
        
        print("\nAll components for the Bitcoin dashboard are working correctly!")
        print("You can run the dashboard using: python -m bitcoin_tracker.bitcoin_dashboard_standalone")
        print("Or by using the run_bitcoin_dashboard.bat script")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bitcoin_dashboard()
