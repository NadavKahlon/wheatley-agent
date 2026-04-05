# -----------------
# Created by Gemini
# -----------------

# Setup Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Resolve-Path "$ScriptDir\.."
$ProtoSourceDir = Resolve-Path "$RootDir\proto"

# Define Output Destinations
$PythonOutDir = "$RootDir\server\src\wheatley_server\proto"
$CppOutDir    = "$RootDir\agent\WheatleyProto\proto"

# Force-delete output directories
Write-Host "Cleaning output directories..." -ForegroundColor Gray
foreach ($dir in @($PythonOutDir, $CppOutDir)) {
    if (Test-Path $dir) { 
        Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue 
    }
}

Write-Host "Clean successful." -ForegroundColor Green
