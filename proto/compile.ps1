# -----------------
# Created by Gemini
# -----------------

# 1. Setup Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Resolve-Path "$ScriptDir\.."
$ProtoSourceDir = Resolve-Path "$RootDir\proto"

# Define Output Destinations
$PythonOutDir = "$RootDir\server\src\wheatley_server\proto"
$CppOutDir    = "$RootDir\agent\WheatleyProto\proto"

# Ensure output directories exist
if (!(Test-Path $PythonOutDir)) { New-Item -ItemType Directory -Path $PythonOutDir -Force }
if (!(Test-Path $CppOutDir))    { New-Item -ItemType Directory -Path $CppOutDir -Force }

# 2. Find all .proto files recursively
$ProtoFiles = Get-ChildItem -Path $ProtoSourceDir -Filter *.proto -Recurse

if ($null -eq $ProtoFiles -or $ProtoFiles.Count -eq 0) {
    Write-Error "No .proto files found in $ProtoSourceDir"
    exit 1
}

Write-Host "Compiling $($ProtoFiles.Count) proto files..." -ForegroundColor Cyan

# 3. Execute protoc
foreach ($file in $ProtoFiles) {
    # Run protoc. Using --proto_path ensures internal imports resolve correctly.
    & protoc `
        --proto_path="$ProtoSourceDir" `
        --python_out="$PythonOutDir" `
        --mypy_out="$PythonOutDir" `
        --cpp_out="$CppOutDir" `
        "$($file.FullName)"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to compile: $($file.Name)"
        exit $LASTEXITCODE
    }
}

Write-Host "Success! Generated files." -ForegroundColor Green