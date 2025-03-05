@echo off
echo ===== Cryptocurrency Price Tracker Setup =====
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Install dependencies using pip
echo Installing dependencies with pip...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit the .env file with your database credentials.
)

REM Create the database
echo Creating database...
python create_database.py

REM Test database connection
echo Testing database connection...
python test_db_connection.py

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit the .env file with your database credentials (if you haven't already)
echo 2. Activate the virtual environment with: venv\Scripts\activate
echo 3. Run the tracker with: python crypto_tracker.py
echo 4. Set up automatic updates by adding run_crypto_tracker.bat to Windows Task Scheduler
echo.
echo For visualization options:
echo - Export data for visualization: python export_for_visualization.py --format all
echo.
echo For more information, please refer to the README.md and docs/FAQ.md files.
echo.
pause
