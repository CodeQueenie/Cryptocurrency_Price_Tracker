@echo off
echo ===== Bitcoin Price History Viewer =====
echo.
echo This tool will show you Bitcoin's price history.
echo.
cd /d "%~dp0"
call venv\Scripts\activate

echo Loading Bitcoin price data...
echo.
python view_bitcoin_history.py

echo.
echo Press any key to exit...
pause > nul
