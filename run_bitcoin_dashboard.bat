@echo off
REM Run Bitcoin Dashboard using the virtual environment
REM -------------------------------------------------

echo Starting Bitcoin Dashboard...

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup_venv.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run the dashboard
call venv\Scripts\activate.bat
python -m bitcoin_tracker.bitcoin_dashboard_standalone

REM Deactivate virtual environment when done
call deactivate
