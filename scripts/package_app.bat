@echo off
echo Creating standalone Bitcoin Price Tracker application...
cd /d "%~dp0\.."

:: Activate virtual environment
call venv\Scripts\activate

:: Install PyInstaller if not already installed
pip install pyinstaller

:: Create a dist directory if it doesn't exist
if not exist "dist" mkdir dist

:: Clean up any previous builds
if exist "build" rmdir /s /q build
if exist "dist\BitcoinTracker" rmdir /s /q "dist\BitcoinTracker"

:: Package the application with PyInstaller
pyinstaller --noconfirm --clean ^
    --name "BitcoinTracker" ^
    --windowed ^
    --add-data ".env;." ^
    --hidden-import="sqlalchemy.sql.default_comparator" ^
    --hidden-import="matplotlib" ^
    --hidden-import="pandas" ^
    --hidden-import="tkinter" ^
    --hidden-import="PIL" ^
    --icon="docs/bitcoin.ico" ^
    bitcoin_tracker\bitcoin_dashboard_standalone.py

:: Copy additional files
echo Copying additional files...
if not exist "dist\BitcoinTracker\docs" mkdir "dist\BitcoinTracker\docs"
copy "docs\*.md" "dist\BitcoinTracker\docs\"

:: Copy the Bitcoin README
copy "bitcoin_tracker\README.md" "dist\BitcoinTracker\README.md"

:: Create a sample .env file if it doesn't exist in the dist directory
if not exist "dist\BitcoinTracker\.env" (
    echo Creating sample environment file...
    echo # Database Configuration > "dist\BitcoinTracker\.env"
    echo DB_TYPE=sqlite >> "dist\BitcoinTracker\.env"
    echo DB_HOST=localhost >> "dist\BitcoinTracker\.env"
    echo DB_PORT=0 >> "dist\BitcoinTracker\.env"
    echo DB_NAME=crypto_tracker.db >> "dist\BitcoinTracker\.env"
    echo DB_USER= >> "dist\BitcoinTracker\.env"
    echo DB_PASSWORD= >> "dist\BitcoinTracker\.env"
    echo # API Configuration >> "dist\BitcoinTracker\.env"
    echo API_KEY= >> "dist\BitcoinTracker\.env"
    echo API_RATE_LIMIT=50 >> "dist\BitcoinTracker\.env"
)

echo.
echo Standalone application created successfully!
echo The application is located in the dist\BitcoinTracker directory.
echo.
echo To create an installer package, run create_installer.bat
echo.
pause
