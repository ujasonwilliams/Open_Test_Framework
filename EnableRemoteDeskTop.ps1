# This script enables Remote Desktop on a Windows machine, checks if it is already enabled,
# configures the firewall to allow Remote Desktop connections, and optionally sets a new hostname.

function Enable-RemoteDesktop {
    # Check if Remote Desktop is already enabled
    Write-Host "Checking if Remote Desktop is enabled..."
    $RemoteDesktopEnabled = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections"

    if ($RemoteDesktopEnabled.fDenyTSConnections -eq 0) {
        Write-Host "Remote Desktop is already enabled."
    } else {
        Write-Host "Enabling Remote Desktop..."
        # Enable Remote Desktop
        Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0

        # Configure the firewall to allow Remote Desktop connections
        Write-Host "Configuring the firewall to allow Remote Desktop connections..."
        Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

        Write-Host "Remote Desktop has been enabled and firewall configured."
    }

    # Confirm the status of Remote Desktop
    $RemoteDesktopEnabled = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections"
    if ($RemoteDesktopEnabled.fDenyTSConnections -eq 0) {
        Write-Host "Remote Desktop is successfully enabled."
    } else {
        Write-Error "Failed to enable Remote Desktop."
    }
}

function Create-AdminUser {
    param (
        [string]$Username = "LabAdmin",
        [string]$Password = "P@ssw0rd"
    )

    Write-Host "Creating admin user account '$Username'..."

    # Check if the user already exists
    $UserExists = Get-LocalUser -Name $Username -ErrorAction SilentlyContinue
    if ($UserExists) {
        Write-Host "User '$Username' already exists. Skipping creation."
    } else {
        # Create the user account
        $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
        New-LocalUser -Name $Username -Password $SecurePassword -FullName "Lab Administrator" -Description "Admin account created by script"

        # Add the user to the Administrators group
        Add-LocalGroupMember -Group "Administrators" -Member $Username

        Write-Host "Admin user account '$Username' has been created and added to the Administrators group."
    }
}

function Set-NewHostname {
    # Create a new hostname for the computer. "LabMachine" + timestamp
    $timestamp = Get-Date -Format "mmss"
    $hostname = "LabMachine" + $timestamp

    Write-Host "Setting new hostname to $hostname..."
    # Set the new hostname
    Rename-Computer -NewName $hostname -Force

    # Restart the computer to apply the new hostname
    Write-Host "Restarting the computer to apply the new hostname..."
    Restart-Computer -Force
}

# Example usage of the functions
Create-AdminUser -Username "LabAdmin" -Password "P@ssw0rd"
Enable-RemoteDesktop
Set-NewHostname


