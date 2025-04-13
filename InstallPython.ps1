# This PowerShell script installs Python 3.13.3 on Windows, installs dependencies from Requirements.dat, and sets the Python path.

$LogFile = Join-Path $PSScriptRoot "InstallPython.log"
function Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $CallStack = Get-PSCallStack | Select-Object -Skip 1 -First 1  # Skip the Log function itself
    $LineNumber = $CallStack.ScriptLineNumber
    $LogMessage = "$Timestamp - Line $LineNumber - $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

# Function to install Python
function Install-Python {
    param (
        [string]$PythonInstallerPath,
        [string]$InstallDir
    )

    if (-Not $PythonInstallerPath) {
        Log "Testing Python installer path is not set. Please ensure the installer path is specified."
        Log "Nothing found at $PythonInstallerPath. Stopping script."
        exit 1
    }

    if (-Not (Test-Path $PythonInstallerPath)) {
        Log "Python installer not found at $PythonInstallerPath."
        Log "Please ensure the installer is present at the specified path."
        exit 1
    }

    if (-Not $InstallDir) {
        Log "InstallDir is not set. Please ensure the target installation directory is specified."
        Log "Nothing found at $InstallDir. Stopping script."
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
    $PythonExe = Join-Path $InstallDir "python.exe"
    if (Test-Path $PythonExe) {
        Log "Python installed successfully at $PythonExe."
    } else {
        Log "Python installation failed. Could not locate python.exe at $InstallDir."
        exit 1
    }
}

# Function to install dependencies from Requirements.dat
function Install-Dependencies {
    param (
        [string]$PythonExe,
        [string]$RequirementsFile
    )

    if (-Not (Test-Path $PythonExe)) {
        Log "Python executable not found at $PythonExe. Cannot install dependencies."
        exit 1
    }

    if (-Not (Test-Path $RequirementsFile)) {
        Log "Requirements file not found at $RequirementsFile. Skipping dependency installation."
        return
    }

    Log "Installing dependencies from $RequirementsFile..."
    & $PythonExe -m pip install -r $RequirementsFile --trusted-host pypi.org --trusted-host files.pythonhosted.org
    if ($LASTEXITCODE -ne 0) {
        Log "Failed to install dependencies from $RequirementsFile."
        exit 1
    }
    Log "Dependencies installed successfully from $RequirementsFile."
}


# Function to set Python path and verify it
function Set-PythonPath {
    param (
        [string]$InstallDir
    )

    $PythonPath = "$InstallDir;$InstallDir\Scripts"
    Log "Adding Python to the PATH environment variable: $PythonPath"

    # Update the PATH environment variable for the current session
    $env:Path = "$PythonPath;$env:Path"

    # Update the PATH environment variable permanently
    $CurrentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

    Log "Verifying if Python path is already in the PATH environment variable..."
    if ($CurrentPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$PythonPath;$CurrentPath", [EnvironmentVariableTarget]::Machine)
        Log "Python path added to the PATH environment variable permanently."
    } else {
        Log "Python path is already present in the PATH environment variable."
    }

}

# Main Execution
Log "Starting Python installation process..."

# Initialize required variables
$PythonInstallerPath = Join-Path $PSScriptRoot "Tools\python-3.13.3-amd64.exe"
Log "Python installer path: $PythonInstallerPath"
if (-Not (Test-Path $PythonInstallerPath)) {
    Log "Python installer not found at $PythonInstallerPath."
    exit 1
}

$InstallDir = "C:\Program Files\Python3.13.3"
Log "Installation directory: $InstallDir"
if (-Not (Test-Path $InstallDir)) {
    Log "Installation directory does not exist. Creating directory: $InstallDir"
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
} else {
    Log "Installation directory already exists: $InstallDir"
}

$RequirementsFile = Join-Path $PSScriptRoot "Requirement.dat"
Log "Requirements file path: $RequirementsFile"
if (-Not (Test-Path $RequirementsFile)) {
    Log "Requirements file not found at $RequirementsFile."
    exit 1
}

Log "Starting Python installation..."
Log "Calling Install-Python with parameters:"
Log "  PythonInstallerPath: $PythonInstallerPath"
Log "  InstallDir: $InstallDir"
Install-Python -PythonInstallerPath $PythonInstallerPath -InstallDir $InstallDir

# Install dependencies
$PythonExe = Join-Path $InstallDir "python.exe"
Log "Python executable path: $PythonExe"
if (-Not (Test-Path $PythonExe)) {
    Log "Python executable not found at $PythonExe. Cannot install dependencies."
    exit 1
} else {
    Log "Python executable found at $PythonExe."
}

Log "Calling Install-Dependencies with parameters:"
Log "  PythonExe: $PythonExe"
Log "  RequirementsFile: $RequirementsFile"
Install-Dependencies -PythonExe $PythonExe -RequirementsFile $RequirementsFile

# Set Python path
Log "Setting the Python path..."
Log "Calling Set-PythonPath with parameter:"
Log "  InstallDir: $InstallDir"
if (-Not (Test-Path $InstallDir)) {
    Log "Installation directory does not exist. Cannot set Python path."
    exit 1
} else {
    Log "Installation directory exists: $InstallDir"
}
Set-PythonPath -InstallDir $InstallDir

Log "Python installation process completed successfully."