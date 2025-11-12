# PowerShell script to run the evaluation
# Usage: .\run_eval.ps1

$ErrorActionPreference = "Stop"

# Check if OPENAI_API_KEY is set
if (-not $env:OPENAI_API_KEY) {
    Write-Host "ERROR: OPENAI_API_KEY environment variable is not set." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set it using:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY = "your-api-key-here"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or set it permanently in your system environment variables." -ForegroundColor Yellow
    exit 1
}

# Check if venv exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found at venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "Running evaluation with venv..." -ForegroundColor Green
Write-Host ""

# Run the evaluation using venv's Python directly
& "venv\Scripts\python.exe" run_eval.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Evaluation completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Evaluation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

