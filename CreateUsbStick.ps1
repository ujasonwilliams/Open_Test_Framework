<#
.SYNOPSIS
    Copies all files and subdirectories from the current folder to a USB stick into a folder named "OpenFramework".

.DESCRIPTION
    This script identifies the USB stick by its drive letter and copies all files and subdirectories 
    from the current folder and below to a folder named "OpenFramework" on the USB stick. Files matching 
    the skip list are excluded, except for the `__pycache__` folder, which is explicitly included.

.NOTES
    File Name: CreateUSBStick.ps1
    Author: Jaswi
    Date: 2025
    Version: 1.6
    Requires: PowerShell 5.1 or later
#>

# Function to get the drive letter of a removable USB stick
function Get-RemovableDrive {
    Get-CimInstance -ClassName Win32_LogicalDisk | Where-Object {
        $_.DriveType -eq 2  # DriveType 2 indicates a removable drive
    } | Select-Object -First 1
}

# Check for a removable USB stick
$RemovableDrive = Get-RemovableDrive
if (-not $RemovableDrive) {
    Write-Host "No removable USB stick detected. Please insert a USB stick and try again." -ForegroundColor Red
    exit
}

# Define the source and destination paths
$SourcePath = (Get-Location).Path.TrimEnd("\")  # Ensure no trailing backslash
$DestinationRoot = $RemovableDrive.DeviceID.TrimEnd("\")  # Ensure no trailing backslash
$DestinationPath = Join-Path -Path $DestinationRoot -ChildPath "OpenFramework"  # Create "OpenFramework" folder

# Create the "OpenFramework" folder if it doesn't exist
if (-not (Test-Path -Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath | Out-Null
    Write-Host "Created folder: $DestinationPath" -ForegroundColor Green
}

Write-Host "Detected USB drive: $DestinationRoot" -ForegroundColor Green

# Define the skip lists
$SkipExtensions = @(".log", ".txt", ".code-workspace", ".gitignore")  # File extensions to skip
$SkipFolders = @(".git", ".vscode", ".venv", "UnitTest")             # Folder names to skip

# Measure the time it takes to copy files
Write-Host "Copying files from $SourcePath to $DestinationPath, skipping specified files and folders..." -ForegroundColor Cyan
$ElapsedTime = Measure-Command {
    Get-ChildItem -Path $SourcePath -Recurse | Where-Object {
        # Skip folders in the skip list and their contents, but explicitly include __pycache__
        if ($_.PSIsContainer -and ($SkipFolders -contains $_.Name) -and ($_.Name -ne "__pycache__")) {
            Write-Host "Skipping folder and its contents: $($_.FullName)" -ForegroundColor Yellow
            $false
        }
        # Skip files under skipped folders
        elseif ($_.FullName -match "\\($($SkipFolders -join '|'))\\") {
            Write-Host "Skipping file under skipped folder: $($_.FullName)" -ForegroundColor Yellow
            $false
        }
        # Skip files with specified extensions
        elseif (-not $_.PSIsContainer -and ($SkipExtensions -contains $_.Extension)) {
            Write-Host "Skipping file: $($_.FullName)" -ForegroundColor Yellow
            $false
        }
        else {
            $true
        }
    } | ForEach-Object {
        $RelativePath = $_.FullName.Substring($SourcePath.Length).TrimStart("\")  # Calculate relative path correctly
        $DestinationFile = Join-Path -Path $DestinationPath -ChildPath $RelativePath

        if ($_.PSIsContainer) {
            # Create directories
            if (-not (Test-Path -Path $DestinationFile)) {
                New-Item -ItemType Directory -Path $DestinationFile | Out-Null
            }
        } else {
            # Copy files
            Write-Host "Copying file: $RelativePath" -ForegroundColor Green
            New-Item -ItemType Directory -Path (Split-Path $DestinationFile) -Force | Out-Null
            Copy-Item -Path $_.FullName -Destination $DestinationFile -Force
        }
    }
}

Write-Host "All files have been successfully copied to the USB drive in the 'OpenFramework' folder, excluding skipped files." -ForegroundColor Green
Write-Host "Time taken to copy files: $($ElapsedTime.TotalSeconds) seconds" -ForegroundColor Yellow