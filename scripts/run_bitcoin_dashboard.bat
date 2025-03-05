@echo off
echo Running Bitcoin Dashboard...
cd /d "%~dp0\.."

REM Activate virtual environment
call venv\Scripts\activate

REM Run the Bitcoin dashboard
python bitcoin_tracker\bitcoin_dashboard_standalone.py

pause
