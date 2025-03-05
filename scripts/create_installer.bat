@echo off
echo Creating Bitcoin Price Tracker Installer Package...
cd /d "%~dp0\.."

:: Activate virtual environment
call venv\Scripts\activate

:: Check if the dist directory exists
if not exist "dist\BitcoinTracker" (
    echo Error: You need to run scripts\package_app.bat first to create the application!
    pause
    exit /b 1
)

:: Create a temp directory for the installer
if not exist "installer" mkdir installer
if exist "installer\BitcoinTracker" rmdir /s /q "installer\BitcoinTracker"
mkdir "installer\BitcoinTracker"

:: Copy files to the installer directory
echo Copying application files...
xcopy /E /I /Y "dist\BitcoinTracker" "installer\BitcoinTracker"
copy "bitcoin_tracker\README.md" "installer\BitcoinTracker\README.md"

:: Create docs directory and copy only essential documentation
if not exist "installer\BitcoinTracker\docs" mkdir "installer\BitcoinTracker\docs"
copy "docs\*.ico" "installer\BitcoinTracker\docs\"

:: Create a sample .env file
echo Creating sample environment file...
echo # Database Configuration > "installer\BitcoinTracker\.env"
echo DB_TYPE=sqlite >> "installer\BitcoinTracker\.env"
echo DB_HOST=localhost >> "installer\BitcoinTracker\.env"
echo DB_PORT=0 >> "installer\BitcoinTracker\.env"
echo DB_NAME=crypto_tracker.db >> "installer\BitcoinTracker\.env"
echo DB_USER= >> "installer\BitcoinTracker\.env"
echo DB_PASSWORD= >> "installer\BitcoinTracker\.env"
echo # API Configuration >> "installer\BitcoinTracker\.env"
echo API_KEY= >> "installer\BitcoinTracker\.env"
echo API_RATE_LIMIT=50 >> "installer\BitcoinTracker\.env"

:: Create an installer script
echo Creating installer script...
echo @echo off > "installer\install.bat"
echo echo Installing Bitcoin Price Tracker... >> "installer\install.bat"
echo. >> "installer\install.bat"
echo :: Create program directory >> "installer\install.bat"
echo if not exist "%%PROGRAMFILES%%\BitcoinTracker" mkdir "%%PROGRAMFILES%%\BitcoinTracker" >> "installer\install.bat"
echo. >> "installer\install.bat"
echo :: Copy files >> "installer\install.bat"
echo xcopy /E /I /Y BitcoinTracker "%%PROGRAMFILES%%\BitcoinTracker" >> "installer\install.bat"
echo. >> "installer\install.bat"
echo :: Create desktop shortcut >> "installer\install.bat"
echo echo Set oWS = WScript.CreateObject("WScript.Shell") ^> CreateShortcut.vbs >> "installer\install.bat"
echo echo sLinkFile = "%%USERPROFILE%%\Desktop\Bitcoin Tracker.lnk" ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo Set oLink = oWS.CreateShortcut(sLinkFile) ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo oLink.TargetPath = "%%PROGRAMFILES%%\BitcoinTracker\BitcoinTracker.exe" ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo oLink.WorkingDirectory = "%%PROGRAMFILES%%\BitcoinTracker" ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo oLink.Description = "Bitcoin Price Tracker" ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo oLink.IconLocation = "%%PROGRAMFILES%%\BitcoinTracker\BitcoinTracker.exe,0" ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo echo oLink.Save ^>^> CreateShortcut.vbs >> "installer\install.bat"
echo cscript CreateShortcut.vbs >> "installer\install.bat"
echo del CreateShortcut.vbs >> "installer\install.bat"
echo. >> "installer\install.bat"
echo echo Installation complete! >> "installer\install.bat"
echo echo A shortcut has been created on your desktop. >> "installer\install.bat"
echo echo. >> "installer\install.bat"
echo pause >> "installer\install.bat"

:: Create a ZIP file
echo Creating ZIP archive...
powershell -Command "Compress-Archive -Path 'installer\*' -DestinationPath 'BitcoinTracker_Installer.zip' -Force"

echo.
echo Installer package created successfully!
echo The installer is available as BitcoinTracker_Installer.zip
echo.
echo To distribute, share the ZIP file with users.
echo.
pause
