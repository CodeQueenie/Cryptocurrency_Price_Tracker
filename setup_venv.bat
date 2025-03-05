@echo off
REM Setup Virtual Environment for Cryptocurrency Price Tracker
REM --------------------------------------------------------

echo Setting up virtual environment for Cryptocurrency Price Tracker...

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if virtual environment already exists
if exist venv (
    echo Virtual environment already exists. Do you want to recreate it? (y/n)
    set /p recreate=
    if /i "%recreate%"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q venv
    ) else (
        echo Using existing virtual environment.
        goto activate
    )
)

echo Creating virtual environment...
python -m venv venv

:activate
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo     venv\Scripts\activate.bat
echo.
echo To deactivate the virtual environment, run:
echo     deactivate
echo.

REM Keep the window open
pause
