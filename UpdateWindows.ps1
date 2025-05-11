# Suppress progress messages
$ProgressPreference = 'SilentlyContinue'

# Remove the old log file if it exists
if (Test-Path $LogFile) {
    Remove-Item -Path $LogFile -Force
}
# Log file path
$LogFile = Join-Path $PSScriptRoot "UpdateLog.log"

# Function to log messages
function Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $CallStack = Get-PSCallStack | Select-Object -Skip 1 -First 1
    $ModuleName = $CallStack.ScriptName
    $LineNumber = $CallStack.ScriptLineNumber
    $LogMessage = "$Timestamp - Module: $ModuleName - Line: $LineNumber - $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

# Ensure the PSWindowsUpdate module is installed
function Ensure-PSWindowsUpdate {
    Log "Checking for PSWindowsUpdate module..."
    if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) {
        Log "PSWindowsUpdate module not found. Installing it..."
        Install-Module -Name PSWindowsUpdate -Force -Scope CurrentUser
        Log "PSWindowsUpdate module installed successfully."
    } else {
        Log "PSWindowsUpdate module is already installed."
    }
}

# Function to check for and install updates
function Install-PendingUpdates {
    Log "Checking for Windows updates..."
    Import-Module PSWindowsUpdate
    Log "Installing updates..."
    Install-WindowsUpdate -AcceptAll -AutoReboot -IgnoreReboot -Verbose
    Log "Updates installation completed."
}

# Function to create a scheduled task for rebooting and continuing the script
function Create-SchEvent {
    param (
        [string]$TaskName,
        [string]$Execute,
        [string]$WorkingDirectory,
        [string]$Description,
        [string]$ScriptPath
    )

    Write-Host "Creating scheduled task..." -ForegroundColor Cyan

    $Action = New-ScheduledTaskAction -Execute $Execute -WorkingDirectory $WorkingDirectory -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$WorkingDirectory\$ScriptPath`""
    $Trigger = New-ScheduledTaskTrigger -AtStartup -Delay "00:01:00"
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -DontStopOnIdleEnd

    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description $Description -RunLevel Highest -Settings $Settings

    Write-Host "Scheduled task '$TaskName' created successfully." -ForegroundColor Green
}

# Function to check if a reboot is pending
function Test-PendingReboot {
    Log "Checking if a reboot is pending..."
    $PendingRebootKeys = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired",
        "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations"
    )

    foreach ($Key in $PendingRebootKeys) {
        if (Test-Path $Key) {
            Log "Pending reboot detected at $Key."
            return $true
        }
    }

    Log "No pending reboot detected."
    return $false
}

# Function to remove the scheduled task
function Remove-UpdateScheduledTask {
    Log "Removing the scheduled task..."
    $TaskName = "WindowsUpdateTask"
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Log "Scheduled task removed successfully."
    } else {
        Log "No scheduled task found to remove."
    }
}


function Set-NeverSleep
{
    # Set the system to never sleep on AC power
    powercfg -change -standby-timeout-ac 0

    # Set the system to never sleep on battery power
    powercfg -change -standby-timeout-dc 0

    # Set the display to never turn off on AC power
    powercfg -change -monitor-timeout-ac 0

    # Set the display to never turn off on battery power
    powercfg -change -monitor-timeout-dc 0
}

# Function to install Python dependencies from a requirements file
function Install-Requirements {
    param (
        [string]$PythonExePath,
        [string]$RequirementsFilePath
    )

    # Check if the Python executable exists
    if (-Not (Test-Path $PythonExePath)) {
        Log "Python executable not found at $PythonExePath. Cannot install dependencies."
        exit 1
    }

    # Check if the requirements file exists
    if (-Not (Test-Path $RequirementsFilePath)) {
        Log "Requirements file not found at $RequirementsFilePath. Cannot install dependencies."
        exit 1
    }

    Log "Python executable found at $PythonExePath."
    Log "Installing dependencies from $RequirementsFilePath..."

    # Run the pip install command
    & $PythonExePath -m pip install -r $RequirementsFilePath --trusted-host pypi.org --trusted-host files.pythonhosted.org
    if ($LASTEXITCODE -ne 0) {
        Log "Failed to install dependencies from $RequirementsFilePath."
        exit 1
    }

    Log "Dependencies installed successfully from $RequirementsFilePath."
}



# Custom wrapper to retrieve updates safely
function Get-AvailableUpdates {
    Log "Retrieving available Windows updates..."
    Import-Module PSWindowsUpdate
    $Updates = Get-WindowsUpdate -AcceptAll -IgnoreReboot
    if ($Updates) {
        Log "$($Updates.Count) updates found."
        Log "Available updates: $($Updates | Out-String)"
    } else {
        Log "No updates found."
    }
    return $Updates
}

# Main logic
$ScriptPath = $MyInvocation.MyCommand.Path
Log "Starting the script: $ScriptPath"

Log "Setting the system to never sleep."
Set-NeverSleep

Log "Ensuring the PSWindowsUpdate module is installed..."
Ensure-PSWindowsUpdate

do {
    Log "Starting the update process..."
    Install-PendingUpdates

    Log "Check if a reboot is required"
    if (Test-PendingReboot) {
        Log "A reboot is required. Scheduling reboot and continuing the script..."
        Create-SchEvent -TaskName "WindowsUpdateTask" `
                        -Execute "powershell.exe" `
                        -WorkingDirectory (Split-Path -Path $ScriptPath) `
                        -Description "Continue Windows Update process after reboot" `
                        -ScriptPath (Split-Path -Leaf $ScriptPath)
        Restart-Computer -Force
        exit
    } else {
        Log "No reboot is required. Checking for additional updates..."
    }

    Log "Checking for available updates..."
    $AvailableUpdates = Get-AvailableUpdates
    if (-not $AvailableUpdates) {
        Log "No more updates available. Exiting the loop."
        break
    }

    Log "Waiting before checking for updates again..."
    Start-Sleep -Seconds 30
} while ($AvailableUpdates | Where-Object { $_.IsInstalled -eq $false })

Log "All updates have been installed. Cleaning up..."
Remove-UpdateScheduledTask
Log "Windows updates have been installed. Installing Python dependencies..."

Log "Installing Python"
Install-Apps

$DirectoryPath = Split-Path $ScriptPath
$PythonExe = Join-Path $DirectoryPath "python.exe"
Log "Python executable at $PythonExe."
$RequirementsFile = Join-Path "Requirement.dat"
Log
Install-Apps -PythonExePath $PythonExe -RequirementsFilePath $RequirementsFile

Log "Python dependencies installed successfully."
