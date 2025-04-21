<#
.SYNOPSIS
    Embeds system information into an image and sets it as the desktop background.

.DESCRIPTION
    This script gathers system information, embeds it into an image, and sets the image as the desktop wallpaper.

.NOTES
    File Name: SetDesktopWatermark.ps1
    Author: Jaswi
    Date: 2025
    Version: 1.1
    Requires: PowerShell 5.1 or later
#>

# Load required .NET assemblies
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

# Retrieve system information
$SMBIOSName = (Get-CimInstance -ClassName Win32_ComputerSystemProduct).Name
$UEFIVersion = (Get-CimInstance -ClassName Win32_BIOS).SMBIOSBIOSVersion
$CPUType = (Get-CimInstance -ClassName Win32_Processor).Name
$SSDSize = (Get-CimInstance -ClassName Win32_DiskDrive | Where-Object { $_.MediaType -eq "Fixed hard disk media" }).Size
$SSDSizeGB = [math]::Round($SSDSize / 1GB, 2)
$RAMSize = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory
$RAMSizeGB = [math]::Round($RAMSize / 1GB, 2)

$LastBootUpTime = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
if ($LastBootUpTime) {
    try {
        $LastBootUpTimeFormatted = [Management.ManagementDateTimeConverter]::ToDateTime($LastBootUpTime)
    } catch {
        $LastBootUpTimeFormatted = "Invalid Date"
    }
} else {
    $LastBootUpTimeFormatted = "Unavailable"
}

$SecureBootStatus = (Get-CimInstance -Namespace "Root\CIMv2\Security\MicrosoftTpm" -ClassName Win32_Tpm).IsEnabled_InitialValue
$SecureBootStatusFormatted = if ($SecureBootStatus -eq $true) { "Enabled" } elseif ($SecureBootStatus -eq $false) { "Disabled" } else { "Unknown" }

# Create the watermark text
$WatermarkText = @"
SMBIOS Name       : $SMBIOSName
UEFI Version      : $UEFIVersion
CPU Type          : $CPUType
SSD Size          : $SSDSizeGB GB
RAM Size          : $RAMSizeGB GB
Last Reboot Time  : $LastBootUpTimeFormatted
Secure Boot Status: $SecureBootStatusFormatted
"@

# Define the output image path
$OutputImagePath = "$env:USERPROFILE\Desktop\WatermarkBackground.jpg"

# Get screen dimensions
$ScreenWidth = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$ScreenHeight = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height

# Create a blank image
$Bitmap = New-Object System.Drawing.Bitmap $ScreenWidth, $ScreenHeight
$Graphics = [System.Drawing.Graphics]::FromImage($Bitmap)

# Set background color
$BackgroundColor = [System.Drawing.Color]::Black
$Graphics.Clear($BackgroundColor)

# Define font and brush for the text
$Font = New-Object System.Drawing.Font("Consolas", 24, [System.Drawing.FontStyle]::Bold)
$Brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::Cyan)

# Draw the text on the image
$TextPosition = New-Object System.Drawing.PointF(50, 50)
$Graphics.DrawString($WatermarkText, $Font, $Brush, $TextPosition)

# Save the image
$Bitmap.Save($OutputImagePath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$Graphics.Dispose()
$Bitmap.Dispose()

# Set the image as the desktop background
function Set-Wallpaper {
    param (
        [string]$ImagePath
    )
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@
    [Wallpaper]::SystemParametersInfo(0x0014, 0, $ImagePath, 0x0001)
}

Set-Wallpaper -ImagePath $OutputImagePath

Write-Host "Desktop background updated with system information watermark." -ForegroundColor Green