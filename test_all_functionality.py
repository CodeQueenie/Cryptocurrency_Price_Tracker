"""
Comprehensive test script for Cryptocurrency Price Tracker
This script tests all major functionality of the project
"""

import os
import sys
import time
import traceback
from datetime import datetime

# Set up colored output for better readability
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_result(test_name, success, message=""):
    if success:
        print(f"{Colors.GREEN}✓ {test_name}: PASSED{Colors.ENDC}")
        if message:
            print(f"  {message}")
    else:
        print(f"{Colors.RED}✗ {test_name}: FAILED{Colors.ENDC}")
        if message:
            print(f"  {message}")
    return success

def run_test(test_func, test_name):
    try:
        result, message = test_func()
        return print_result(test_name, result, message)
    except Exception as e:
        error_msg = f"Exception: {str(e)}\n{traceback.format_exc()}"
        return print_result(test_name, False, error_msg)

# Test 1: Check project structure
def test_project_structure():
    required_dirs = ['core', 'bitcoin_tracker', 'ethereum_tracker', 'scripts', 'docs']
    required_files = [
        'core/crypto_tracker.py', 
        'core/db_utils.py',
        'bitcoin_tracker/bitcoin_dashboard_standalone.py',
        'requirements.txt',
        '.env',
        'run_bitcoin_dashboard.bat',
        'setup_venv.bat'
    ]
    
    # Check directories
    missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
    
    # Check files
    missing_files = [f for f in required_files if not os.path.isfile(f)]
    
    if not missing_dirs and not missing_files:
        return True, "All required directories and files are present"
    else:
        msg = ""
        if missing_dirs:
            msg += f"Missing directories: {', '.join(missing_dirs)}\n"
        if missing_files:
            msg += f"Missing files: {', '.join(missing_files)}"
        return False, msg

# Test 2: Import core modules
def test_core_imports():
    try:
        from core.crypto_tracker import CryptoTracker
        from core.db_utils import create_db_engine, get_db_connection
        
        # Basic validation of the classes and functions
        assert hasattr(CryptoTracker, 'fetch_crypto_data'), "CryptoTracker missing fetch_crypto_data method"
        assert callable(create_db_engine), "db_utils missing create_db_engine function"
        assert callable(get_db_connection), "db_utils missing get_db_connection function"
        
        return True, "Core modules imported successfully"
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except AssertionError as e:
        return False, f"Validation error: {str(e)}"

# Test 3: Import Bitcoin tracker modules
def test_bitcoin_tracker_imports():
    try:
        from bitcoin_tracker.bitcoin_dashboard_standalone import main
        
        # Just check if the module has the main function
        assert callable(main), "bitcoin_dashboard_standalone.py missing main function"
        
        return True, "Bitcoin tracker modules imported successfully"
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except AssertionError as e:
        return False, f"Validation error: {str(e)}"

# Test 4: Test database connection
def test_database_connection():
    try:
        from core.db_utils import create_db_engine
        
        # Try to create a database engine
        try:
            engine = create_db_engine()
            connection_success = True
            message = "Database engine creation successful"
        except Exception as e:
            # If connection fails, it might be because the database isn't set up
            # This is expected in some environments, so we'll handle it gracefully
            connection_success = False
            message = f"Database engine creation failed: {str(e)}\nThis might be expected if the database isn't set up."
        
        # Test environment variables loading
        from dotenv import load_dotenv
        load_dotenv()
        
        env_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing_vars = [var for var in env_vars if not os.getenv(var)]
        
        if missing_vars:
            return False, f"Missing environment variables: {', '.join(missing_vars)}"
        
        return connection_success, message
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

# Test 5: Test CoinGecko API connection
def test_coingecko_api():
    try:
        from core.crypto_tracker import CryptoTracker
        
        tracker = CryptoTracker()
        
        # Try to ping the CoinGecko API
        from pycoingecko import CoinGeckoAPI
        cg = CoinGeckoAPI()
        ping_result = cg.ping()
        
        if ping_result and 'gecko_says' in ping_result:
            return True, f"Successfully connected to CoinGecko API: {ping_result['gecko_says']}"
        else:
            return False, f"Received invalid response from CoinGecko API: {ping_result}"
    except Exception as e:
        return False, f"API connection error: {str(e)}"

# Test 6: Test virtual environment
def test_virtual_environment():
    # Check if we're running in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        return True, "Running in a virtual environment"
    else:
        # Check if venv directory exists
        if os.path.isdir('venv'):
            return True, "Virtual environment directory exists (but not currently activated)"
        else:
            return False, "Virtual environment not set up"

# Main test runner
def run_all_tests():
    print_header("CRYPTOCURRENCY PRICE TRACKER - FUNCTIONALITY TEST")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {os.getcwd()}")
    
    tests = [
        (test_project_structure, "Project Structure"),
        (test_core_imports, "Core Module Imports"),
        (test_bitcoin_tracker_imports, "Bitcoin Tracker Imports"),
        (test_database_connection, "Database Connection"),
        (test_coingecko_api, "CoinGecko API Connection"),
        (test_virtual_environment, "Virtual Environment")
    ]
    
    results = []
    for test_func, test_name in tests:
        results.append(run_test(test_func, test_name))
        time.sleep(0.5)  # Small delay between tests for readability
    
    # Summary
    passed = results.count(True)
    total = len(results)
    
    print_header(f"TEST SUMMARY: {passed}/{total} TESTS PASSED")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests passed! The project is functioning correctly.{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}Some tests failed. Review the output above for details.{Colors.ENDC}")

if __name__ == "__main__":
    run_all_tests()
