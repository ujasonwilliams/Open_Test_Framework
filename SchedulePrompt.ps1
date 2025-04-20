<#
.SYNOPSIS
    Schedules a task to open a command prompt at a specified directory after the system reboots.

.DESCRIPTION
    This script creates a scheduled task that triggers on system startup. The task opens a command prompt 
    with the working directory set to a specified directory.

.NOTES
    File Name: SchedulePrompt.ps1
    Author: Jaswi
    Date: 2025
    Version: 1.4
    Requires: PowerShell 5.1 or later
#>

function CreateSchEvent {
    param (
        [string]$TaskName,
        [string]$Execute,
        [string]$WorkingDirectory,
        [string]$Description,
        [string]$ScriptPath
    )

    Write-Host "Creating scheduled task..." -ForegroundColor Cyan

    # Define the task action, trigger, and settings
    $Action = New-ScheduledTaskAction -Execute $Execute -WorkingDirectory $WorkingDirectory -Argument "-NoExit  `"$WorkingDirectory\$ScriptPath`""
    $Trigger = New-ScheduledTaskTrigger -AtLogOn
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -DontStopOnIdleEnd

    # Register the scheduled task
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description $Description -RunLevel Highest -Settings $Settings

    Write-Host "Scheduled task '$TaskName' created successfully." -ForegroundColor Green
}

# Call the function with parameters
CreateSchEvent -TaskName "OpenCommandPromptAtC" `
               -Execute "powershell.exe" `
               -WorkingDirectory "C:\t" `
               -Description "Run DutStatus.ps1 at startup" `
               -ScriptPath "DutStatus.ps1"