# Install uv
irm https://astral.sh/uv/install.ps1 | iex

$url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/autosetup.py"
$output = "$env:USERPROFILE\.local\bin\autosetup.py"
Invoke-WebRequest -Uri $url -OutFile $output

# Define the target directory
$targetDir = "$env:USERPROFILE\.local\bin"

# Create the target directory if it doesn't exist
if (-Not (Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir
}

# Define the content of the new CMD script
$scriptContent = @"
@echo off
uv run --with "colorama,requests,readchar" --python 3.12.9 "%USERPROFILE%\.local\bin\autosetup.py"
"@

# Write the content to a new CMD script file in the target directory
$scriptName = "qproject"
$scriptPath = "$targetDir\$scriptName.cmd"

# Remove old version
if (Test-Path -Path $scriptPath) {
    Remove-Item -Path $scriptPath 
}
Set-Content -Path $scriptPath -Value $scriptContent
Write-Output "Installing to $targetDir"
Write-Output "  $scriptName"
Write-Output "To create a new quantum project reopen the terminal and run the command: qproject"
