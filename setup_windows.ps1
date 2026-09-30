# One-time setup for Windows.
# Run from the project folder:  powershell -ExecutionPolicy Bypass -File setup_windows.ps1
#
# It creates the virtual environment OUTSIDE OneDrive (in C:\Users\<you>\venvs)
# so OneDrive doesn't try to sync thousands of package files.

$venv = "$env:USERPROFILE\venvs\movie-search"

if (-not (Test-Path $venv)) {
    Write-Host "Creating virtual environment at $venv ..."
    py -3 -m venv $venv
}

Write-Host "Installing packages (first time takes 5-10 minutes)..."
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host ""
Write-Host "Done! Each time you open a new PowerShell window, activate the environment with:"
Write-Host "    & `"$venv\Scripts\Activate.ps1`""
