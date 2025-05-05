# Suppress progress messages
$ProgressPreference = 'SilentlyContinue'

# Install the WinGet PowerShell module
Write-Host "Installing WinGet PowerShell module from PSGallery..."
Install-PackageProvider -Name NuGet -Force | Out-Null
Install-Module -Name Microsoft.WinGet.Client -Scope AllUsers -Force -Repository PSGallery | Out-Null

# Repair WinGet Package Manager
Write-Host "Repairing WinGet Package Manager..."
Repair-WinGetPackageManager
Write-Host "WinGet setup completed."

# Install applications using WinGet
$Applications = @(
    "VideoLAN.VLC",
    "Notepad++.Notepad++",
    "Python.Python.3.12",
    "Microsoft.VisualStudio.2022.BuildTools"
)

foreach ($App in $Applications) {
    Write-Host "Installing $App..."
    winget install --id $App --silent --accept-package-agreements --accept-source-agreements
}
Write-Host "All applications installed successfully."# Suppress progress messages
# Suppress progress messages
$ProgressPreference = 'SilentlyContinue'

# Install applications using WinGet
$Applications = @(
    "VideoLAN.VLC",
    "Notepad++.Notepad++",
    "Python.Python.3.12",
    "Microsoft.VisualStudio.2022.BuildTools"
)

foreach ($App in $Applications) {
    Write-Host "Installing $App..."
    try {
        cmd.exe /c "winget install --id $App --silent --accept-package-agreements --accept-source-agreements"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install $App using winget. Exit code: $LASTEXITCODE" -ForegroundColor Red
        } else {
            Write-Host "$App installed successfully." -ForegroundColor Green
        }
    } catch {
        Write-Host "An error occurred while installing $App $_" -ForegroundColor Red
    }
}
Write-Host "All applications processed."