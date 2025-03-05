@echo off
echo ===== Packaging Bitcoin Price Tracker =====
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Create a standalone executable
echo Creating standalone executable...
pyinstaller --name "Bitcoin_Price_Tracker" ^
            --onefile ^
            --windowed ^
            --add-data ".env.example;." ^
            --add-data "README.md;." ^
            --add-data "GETTING_STARTED.md;." ^
            --add-data "requirements.txt;." ^
            --add-data "docs;docs" ^
            --icon="resources\bitcoin.ico" ^
            bitcoin_dashboard_standalone.py

REM Copy additional files to the dist folder
echo Copying additional files...
copy setup_standalone.bat dist\setup.bat
copy .env.example dist\.env.example

echo.
echo Packaging complete! The standalone application is in the "dist" folder.
echo Share the entire "dist" folder with your friends.
echo.
pause
