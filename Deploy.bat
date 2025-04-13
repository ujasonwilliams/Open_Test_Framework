@echo on
cls

REM Set PowerShell execution policy to Bypass
echo Setting PowerShell execution policy to Bypass...
Powershell Set-ExecutionPolicy Bypass -Scope LocalMachine -Force

REM Check if C:\t exists
IF NOT EXIST "C:\t" (
    echo Creating C:\t directory...
    mkdir "C:\t"
)

REM Copy all files and subfolders to C:\t
echo Copying files to C:\t...
xcopy * "C:\t\" /E /H /C /I

REM Notify the user
echo All files have been copied to C:\t.

REM Change to C:\t directory
cd /d "C:\t"

REM Leave the user at C:\t
cmd /k