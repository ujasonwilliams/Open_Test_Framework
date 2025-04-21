@echo off
REM Batch file to execute the InstallPython.ps1 script

REM Define the path to the PowerShell script
set SCRIPT_PATH=InstallPython.ps1

REM Check if the script exists
if not exist "%SCRIPT_PATH%" (
    echo The script "%SCRIPT_PATH%" was not found.
    pause
    exit /b 1
)

REM Execute the PowerShell script
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"

REM Check the exit code of the PowerShell script
if %ERRORLEVEL% neq 0 (
    echo The PowerShell script encountered an error.
    pause
    exit /b %ERRORLEVEL%
)
