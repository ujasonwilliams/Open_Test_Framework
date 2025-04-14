@echo off
cls

REM Check if an argument is provided
IF "%1"=="" (
    echo Usage: Make.bat [destination_path]
    echo Example: Make.bat E:\Frame
    exit /b
)

REM Set the destination path from the first argument
set drive=%1
echo Destination path: %drive%

REM Copy files to the specified destination
xcopy . %drive% /sid /exclude:exclude.list

REM Notify the user
echo Files have been copied to %drive%.