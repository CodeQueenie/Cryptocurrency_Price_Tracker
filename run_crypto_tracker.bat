@echo off
echo Starting Cryptocurrency Price Tracker...
cd /d "%~dp0"
call venv\Scripts\activate
python crypto_tracker.py
echo Cryptocurrency Price Tracker completed.
