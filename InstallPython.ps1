# This script automates downloading and installing Visual Studio Build Tools and Python.

$LogFile = Join-Path $PSScriptRoot "InstallEnvironment.log"
function Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # Get the calling script and line number
    $CallStack = Get-PSCallStack | Select-Object -Skip 1 -First 1  # Skip the Log function itself
    $ModuleName = $CallStack.ScriptName
    $LineNumber = $CallStack.ScriptLineNumber

    # Format the log message
    $LogMessage = "$Timestamp - Module: $ModuleName - Line: $LineNumber - $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

# Function to download a file
function Download-File {
    param (
        [string]$DownloadUrl,
        [string]$SavePath
    )

    if (-Not (Test-Path $SavePath)) {
        Log "Downloading from $DownloadUrl..."
        try {
            Invoke-WebRequest -Uri $DownloadUrl -OutFile $SavePath -UseBasicParsing
            Log "Downloaded successfully to $SavePath."
        } catch {
            Log "Failed to download from $DownloadUrl"
            exit 1
        }
    } else {
        Log "File already exists at $SavePath. Skipping download."
    }
}

# Function to install Visual Studio Build Tools
function Install-BuildTools {
    param (
        [string]$InstallerPath
    )

    # Check if Visual Studio Build Tools are already installed
    $VSPath = "C:\BuildTools\Common7\Tools\vsdevcmd.bat"
    if (Test-Path $VSPath) {
        Log "Visual Studio Build Tools are already installed. Skipping installation."
        return
    }

    if (-Not (Test-Path $InstallerPath)) {
        Log "Build Tools installer not found at $InstallerPath."
        exit 1
    }

    Log "Installing Visual Studio Build Tools silently from $InstallerPath..."

    # Install required components (C++ Build Tools, Windows 10 SDK, CMake)
    $Arguments = "--quiet --wait --norestart --nocache --installPath C:\BuildTools --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --includeOptional"

    # Start the process and capture the exit code
    $Process = Start-Process -FilePath $InstallerPath -ArgumentList $Arguments -Wait -PassThru
    $ExitCode = $Process.ExitCode
    Log "Build Tools installer exited with code $ExitCode."

    if ($ExitCode -ne 0) {
        Log "Build Tools installation failed with exit code $ExitCode."
        exit 1
    }

    Log "Visual Studio Build Tools installed successfully."
}

# Function to install Python
function Install-Python {
    param (
        [string]$PythonInstallerPath,
        [string]$InstallDir
    )

    # Check if Python is already installed
    $PythonExe = Join-Path $InstallDir "python.exe"
    if (Test-Path $PythonExe) {
        Log "Python is already installed at $InstallDir. Skipping installation."
        return
    }

    if (-Not (Test-Path $PythonInstallerPath)) {
        Log "Python installer not found at $PythonInstallerPath."
        exit 1
    }

    Log "Installing Python silently from $PythonInstallerPath..."
    Log "Target installation directory: $InstallDir"

    # Start the process and capture the exit code
    $Process = Start-Process -FilePath $PythonInstallerPath -ArgumentList "/passive", "InstallAllUsers=1", "PrependPath=1", "TargetDir=`"$InstallDir`"" -Wait -PassThru
    $ExitCode = $Process.ExitCode
    Log "Python installer exited with code $ExitCode."

    if ($ExitCode -ne 0) {
        Log "Python installation failed with exit code $ExitCode."
        exit 1
    }

    Log "Checking if Python was installed at $InstallDir..."
    if (Test-Path $PythonExe) {
        Log "Python installed successfully at $PythonExe."
    } else {
        Log "Python installation failed. Could not locate python.exe at $InstallDir."
        exit 1
    }
}
function Install-VLC {
    param (
        [string]$VlcDownloadUrl = "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe",
        [string]$InstallerPath = "$PSScriptRoot\vlc-3.0.21-win64.exe"
    )

    # Check if VLC is already installed
    $VlcExePath = "C:\Program Files\VideoLAN\VLC\vlc.exe"
    if (Test-Path $VlcExePath) {
        Log "VLC Player is already installed at $VlcExePath. Skipping installation."
        return
    }

    # Download the VLC installer
    if (-Not (Test-Path $InstallerPath)) {
        Log "Downloading VLC installer from $VlcDownloadUrl..."
        try {
            # Use Start-BitsTransfer for reliable downloads
            Start-BitsTransfer -Source $VlcDownloadUrl -Destination $InstallerPath
            Log "VLC installer downloaded successfully to $InstallerPath."
        } catch {
            Log "Failed to download VLC installer: $_"
            exit 1
        }
    } else {
        Log "VLC installer already exists at $InstallerPath. Skipping download."
    }

    # Verify the downloaded file size
    if ((Get-Item $InstallerPath).Length -lt 1024) {
        Log "Downloaded file is too small. The download might have failed."
        exit 1
    }

    # Install VLC silently
    Log "Installing VLC Player silently from $InstallerPath..."
    $Process = Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait -PassThru
    $ExitCode = $Process.ExitCode
    Log "VLC installer exited with code $ExitCode."

    if ($ExitCode -ne 0) {
        Log "VLC installation failed with exit code $ExitCode."
        exit 1
    }

    # Verify installation
    if (Test-Path $VlcExePath) {
        Log "VLC Player installed successfully at $VlcExePath."
    } else {
        Log "VLC installation failed. Could not locate vlc.exe at $VlcExePath."
        exit 1
    }
}



# Main Execution
Log "Starting environment setup process..."

# Initialize required variables
$BuildToolsDownloadUrl = "https://aka.ms/vs/17/release/vs_buildtools.exe"
$BuildToolsInstallerPath = Join-Path $PSScriptRoot "vs_buildtools.exe"

$PythonDownloadUrl = "https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe"
$PythonInstallerPath = Join-Path $PSScriptRoot "Tools\python-3.13.3-amd64.exe"
$InstallDir = "C:\Program Files\Python3.13.3"
$RequirementsFile = Join-Path $PSScriptRoot "Requirement.dat"

# Download and install Visual Studio Build Tools
Download-File -DownloadUrl $BuildToolsDownloadUrl -SavePath $BuildToolsInstallerPath
Install-BuildTools -InstallerPath $BuildToolsInstallerPath

# Download and install Python
Download-File -DownloadUrl $PythonDownloadUrl -SavePath $PythonInstallerPath
Install-Python -PythonInstallerPath $PythonInstallerPath -InstallDir $InstallDir

# Add Python to the system PATH
Log "Adding Python to the system PATH..."
$PythonPath = "$InstallDir;$InstallDir\Scripts"
Log "Python path: $PythonPath"

# Update the system PATH
[Environment]::SetEnvironmentVariable("Path", "$PythonPath;$env:Path", [EnvironmentVariableTarget]::Machine)

# Verify the update
$UpdatedPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
Log "Updated system PATH: $UpdatedPath"

# Refresh PATH in the current session
$env:Path = $UpdatedPath
Log "Refreshed PATH in the current session: $env:Path"

# Install Python dependencies
$PythonExe = Join-Path $InstallDir "python.exe"
if (-Not (Test-Path $PythonExe)) {
    Log "Python executable not found at $PythonExe. Cannot install dependencies."
    exit 1
} else {
    Log "Python executable found at $PythonExe."
}

Log "Installing dependencies from $RequirementsFile..."
& $PythonExe -m pip install -r $RequirementsFile --trusted-host pypi.org --trusted-host files.pythonhosted.org
if ($LASTEXITCODE -ne 0) {
    Log "Failed to install dependencies from $RequirementsFile."
    exit 1
}
Log "Dependencies installed successfully from $RequirementsFile."

Log "Installing VLC Player..."
Install-VLC 

Log "Environment setup process completed successfully."