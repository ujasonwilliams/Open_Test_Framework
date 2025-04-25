@echo on
cls

REM Set PowerShell execution policy to Bypass
echo Setting PowerShell execution policy to Bypass...
Powershell Set-ExecutionPolicy Bypass -Scope LocalMachine -Force

REM Detect the USB drive (assumes only one removable drive is connected)
for /f "tokens=1,2 delims=:" %%A in ('wmic logicaldisk where "drivetype=2" get deviceid ^| find ":"') do (
    set USBDrive=%%A:
)

REM Check if a USB drive was detected
if "%USBDrive%"=="" (
    echo No USB drive detected. Please insert a USB drive and try again.
    pause
    exit /b 1
)

REM Notify the user of the detected USB drive
echo USB drive detected: %USBDrive%

REM Define the destination folder on the USB drive
set Destination=%USBDrive%\OpenFramework

REM Create the destination folder if it doesn't exist
if not exist "%Destination%" (
    echo Creating folder: %Destination%
    mkdir "%Destination%"
)

REM Copy all files and subfolders to the USB drive
echo Copying files to %Destination%...
xcopy * "%Destination%\" /E /H /C /I

REM Notify the user
echo All files have been copied to %Destination%.

REM Leave the user at the USB drive
cd /d "%USBDrive%"
cmd /k