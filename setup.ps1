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
uv run --with "requests,colorama" "%USERPROFILE%\.local\bin\autosetup.py"
"@

# Write the content to a new CMD script file in the target directory
$scriptPath = "$targetDir\quantum_init.cmd"
Set-Content -Path $scriptPath -Value $scriptContent

Write-Output "Generated CMD script: $scriptPath"
