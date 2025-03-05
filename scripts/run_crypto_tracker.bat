@echo off
echo Running Cryptocurrency Price Tracker...
cd /d "%~dp0\.."

REM Activate virtual environment
call venv\Scripts\activate

REM Run the crypto tracker
python core\crypto_tracker.py

pause
