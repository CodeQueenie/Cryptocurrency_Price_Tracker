@echo off
color 0A
title Bitcoin Dashboard

:menu
cls
echo =======================================
echo      BITCOIN PRICE TRACKER DASHBOARD
echo =======================================
echo.
echo  [1] View Current Bitcoin Price
echo  [2] View Bitcoin Price History
echo  [3] Update Bitcoin Prices
echo  [4] Export Bitcoin Data to Excel
echo  [5] Exit
echo.
echo =======================================
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto view_current
if "%choice%"=="2" goto view_history
if "%choice%"=="3" goto update_prices
if "%choice%"=="4" goto export_excel
if "%choice%"=="5" goto exit_app

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:view_current
cls
echo Loading current Bitcoin price...
cd /d "%~dp0"
call venv\Scripts\activate
python view_database_contents.py
echo.
echo Press any key to return to the menu...
pause >nul
goto menu

:view_history
cls
echo Loading Bitcoin price history...
cd /d "%~dp0"
call venv\Scripts\activate
python view_database_contents.py
echo.
echo Press any key to return to the menu...
pause >nul
goto menu

:update_prices
cls
echo Updating Bitcoin prices...
cd /d "%~dp0"
call venv\Scripts\activate
python crypto_tracker.py
timeout /t 5
echo.
echo Press any key to return to the menu...
pause >nul
goto menu

:export_excel
cls
echo Exporting Bitcoin data to Excel...
cd /d "%~dp0"
call venv\Scripts\activate
python export_for_visualization.py --format excel
echo.
echo Press any key to return to the menu...
pause >nul
goto menu

:exit_app
cls
echo Thank you for using the Bitcoin Price Tracker!
echo.
timeout /t 2 >nul
exit
