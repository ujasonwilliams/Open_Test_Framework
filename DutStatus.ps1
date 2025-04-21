 <#
.SYNOPSIS
    Displays system information including SMBIOS name, UEFI version, CPU type, SSD size, RAM size, last reboot time, and secure boot status.

.DESCRIPTION
    This script gathers system information using WMI and CIM cmdlets and displays it in a readable format.

.NOTES
    File Name: DutStatus.ps1
    Author: Jaswi
    Date: 2025
    Version: 1.4
    Requires: PowerShell 5.1 or later
#>

# Retrieve SMBIOS name
$SMBIOSName = (Get-CimInstance -ClassName Win32_ComputerSystemProduct).Name

# Retrieve UEFI version
$UEFIVersion = (Get-CimInstance -ClassName Win32_BIOS).SMBIOSBIOSVersion

# Retrieve CPU type
$CPUType = (Get-CimInstance -ClassName Win32_Processor).Name

# Retrieve SSD size
$SSDSize = (Get-CimInstance -ClassName Win32_DiskDrive | Where-Object { $_.MediaType -eq "Fixed hard disk media" }).Size
$SSDSizeGB = [math]::Round($SSDSize / 1GB, 2)

# Retrieve RAM size
$RAMSize = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory
$RAMSizeGB = [math]::Round($RAMSize / 1GB, 2)

# Retrieve last reboot time
$LastBootUpTime = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
if ($LastBootUpTime -and $LastBootUpTime -match "^\d{14}\.\d{6}\+\d{3}$") {
    try {
        $LastBootUpTimeFormatted = [Management.ManagementDateTimeConverter]::ToDateTime($LastBootUpTime)
    } catch {
        $LastBootUpTimeFormatted = "Unable to retrieve last reboot time (conversion error)"
    }
} elseif ($LastBootUpTime) {
    try {
        # Alternative formatting if the value is not in DMTF format
        $LastBootUpTimeFormatted = Get-Date $LastBootUpTime
    } catch {
        $LastBootUpTimeFormatted = "Unable to retrieve last reboot time (alternative method failed)"
    }
} else {
    $LastBootUpTimeFormatted = "Unavailable"
}

# Retrieve Secure Boot Status
$SecureBootStatus = (Get-CimInstance -Namespace "Root\CIMv2\Security\MicrosoftTpm" -ClassName Win32_Tpm).IsEnabled_InitialValue
if ($SecureBootStatus -eq $true) {
    $SecureBootStatusFormatted = "Enabled"
} elseif ($SecureBootStatus -eq $false) {
    $SecureBootStatusFormatted = "Disabled"
} else {
    $SecureBootStatusFormatted = "Unknown"
}

# Display the information
Clear-Host
Write-Host "System Information:" -ForegroundColor Cyan
Write-Host "--------------------------------------"
Write-Host -NoNewline "SMBIOS Name       : " -ForegroundColor Cyan
Write-Host "$SMBIOSName" -ForegroundColor White
Write-Host -NoNewline "UEFI Version      : " -ForegroundColor Cyan
Write-Host "$UEFIVersion" -ForegroundColor White
Write-Host -NoNewline "CPU Type          : " -ForegroundColor Cyan
Write-Host "$CPUType" -ForegroundColor White
Write-Host -NoNewline "SSD Size          : " -ForegroundColor Cyan
Write-Host "$SSDSizeGB GB" -ForegroundColor White
Write-Host -NoNewline "RAM Size          : " -ForegroundColor Cyan
Write-Host "$RAMSizeGB GB" -ForegroundColor White
Write-Host -NoNewline "Last Reboot Time  : " -ForegroundColor Cyan
Write-Host "$LastBootUpTimeFormatted" -ForegroundColor White
Write-Host -NoNewline "Secure Boot Status: " -ForegroundColor Cyan
Write-Host "$SecureBootStatusFormatted" -ForegroundColor White