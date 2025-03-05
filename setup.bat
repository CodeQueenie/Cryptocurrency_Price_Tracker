@echo off
echo ===== Cryptocurrency Price Tracker Setup =====
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Anaconda or Miniconda from https://www.anaconda.com/download/
    echo Make sure to check "Add Anaconda to PATH" during installation.
    pause
    exit /b 1
)

REM Check if Conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Conda is not installed or not in PATH.
    echo Please install Anaconda or Miniconda from https://www.anaconda.com/download/
    echo Make sure to check "Add Anaconda to PATH" during installation.
    pause
    exit /b 1
)

REM Create conda environment
echo Creating Conda environment...
conda create -y -n crypto_tracker python=3.9
call conda activate crypto_tracker

REM Install dependencies using conda
echo Installing dependencies with Conda...
conda install -y -c conda-forge requests pandas sqlalchemy python-dotenv schedule psycopg2-binary pymysql cryptography openpyxl matplotlib

REM Install pycoingecko with pip (not available in conda)
echo Installing PyCoingecko with pip...
pip install pycoingecko==3.1.0

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit the .env file with your database credentials.
)

REM Test database connection
echo Testing database connection...
python test_db_connection.py

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit the .env file with your database credentials (if you haven't already)
echo 2. Run the tracker with: conda activate crypto_tracker ^&^& python crypto_tracker.py
echo 3. Set up automatic updates with: python setup_scheduler.py
echo.
echo For visualization options:
echo - Export data for visualization: python export_for_visualization.py --format all
echo.
echo For more information, please refer to the README.md and docs/FAQ.md files.
echo.
pause
